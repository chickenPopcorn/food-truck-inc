from flask import Flask, request, session, jsonify, url_for, redirect, abort, flash, render_template
from flask_pymongo import PyMongo
from server.data_access.vendor_data_access import VendorDataAccess
from server.data_access.user_data_access import UserDataAccess
import bcrypt
from functools import wraps
from werkzeug.utils import secure_filename
from os.path import join, dirname
from dotenv import load_dotenv
import os
import braintree
import boto
import boto.s3
from boto.s3.key import Key

app = Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app.secret_key = os.environ['APP_SECRET_KEY']
# mongodb database
app.config['MONGO_DBNAME'] = os.environ['MONGO_DBNAME']
app.config['MONGO_URI'] = os.environ['MONGO_URI']
# file upload
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
app.config['DEBUG'] = True

app.config['S3_ACCESS_KEY'] = os.environ['S3_ACCESS_KEY']
app.config['S3_SECRET_KEY'] = os.environ['S3_SECRET_KEY']
bucketName = 'vendors-6998'

mongo = PyMongo(app)

braintree.Configuration.configure(
    os.environ.get('BT_ENVIRONMENT'),
    os.environ.get('BT_MERCHANT_ID'),
    os.environ.get('BT_PUBLIC_KEY'),
    os.environ.get('BT_PRIVATE_KEY')
)

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]


def get_mongodb_collection(database, role):
    if role == "customer":
        return UserDataAccess(database.db.customerLogin)
    elif role == "vendor":
        return UserDataAccess(database.db.vendorLogin)
    else:
        return null


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def upload_to_s3(aws_access_key_id, aws_secret_access_key, file, bucket, key, callback=None, md5=None, reduced_redundancy=False, content_type=None):
    """
    Uploads the given file to the AWS S3
    bucket and key specified.

    callback is a function of the form:

    def callback(complete, total)

    The callback should accept two integer parameters,
    the first representing the number of bytes that
    have been successfully transmitted to S3 and the
    second representing the size of the to be transmitted
    object.

    Returns boolean indicating success/failure of upload.
    """
    try:
        size = os.fstat(file.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucket, validate=True)
    k = Key(bucket)
    k.key = key
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)
    # set appropriate ACL
    k.set_acl('public-read')

    # Rewind for later use
    file.seek(0)

    if sent == size:
        return True
    return False


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if not session or session['logged_in'] != "vendor":
        return abort(403)
    #username = "tianci"
    username = session['username']
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return abort(400)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return abort(400)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], username)
            # for testing saved locally
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            file.save(os.path.join(path, filename))

            file = open(os.path.join(path, filename), 'r+')
            key = '/'.join([username, filename])

            if upload_to_s3(app.config['S3_ACCESS_KEY'], app.config['S3_SECRET_KEY'], file, bucketName, key):
                print 'It worked!'
            else:
                print 'The upload failed...'
            file.close()

            return '''   <!doctype html>
                            <title>Uploaded a File</title>
                            <h1>Upload Successful</h1>

                            '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({"status": True})
    return wrap

# testing route
@app.route('/')
def hello_world():
    return 'Hello, World!'

# user info management routes
@app.route('/login/<role>', methods=['POST'])
def login(role):
    uda = get_mongodb_collection(mongo, role)
    if not uda:
        return abort(403)
    output = uda.authorize(request.form)
    if output['status']:
        session['logged_in'] = role
        session['username'] = output['result']['user']['username']
    return jsonify(output)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({"status": True, "message": "You logged out!"})

# register in API post only
@app.route('/register/<role>', methods=['POST'])
def register(role):
    uda = get_mongodb_collection(mongo, role)
    if not uda:
        return abort(403)
    output = uda.register(request.form)
    return jsonify(output)

# testing use
@app.route('/delete', methods=['POST'])
@login_required
def delete_user():
    uda = get_mongodb_collection(mongo, session['logged_in'])
    if not uda:
        return abort(403)
    output = uda.delete(request.form)
    return jsonify(output)

@app.route('/changePassword', methods=['POST'])
@login_required
def change_password():
    uda = get_mongodb_collection(mongo, session['logged_in'])
    if not uda:
        return abort(403)
    output = uda.change_password(request.form, session['username'])
    return jsonify(output)

@app.route('/updateProfile', methods=['POST'])
@login_required
def update_profile():
    uda = get_mongodb_collection(mongo, session['logged_in'])
    if not uda:
        return abort(403)
    output = uda.update_profile(request.form)
    return jsonify(output)




# vendor upload info
@app.route('/addMenuItem', methods=['POST'])
@login_required
def add_menu_item():
    if session['logged_in'] != "vendor":
        return abort(403)
    vda = VendorDataAccess(mongo.db.vendors, session['username'])
    output = vda.add_menu_item(request.form)
    return jsonify(output)

# vendor upload info
@app.route('/deleteMenuItem', methods=['POST'])
# @login_required
def delete_menu_item():
    '''
    if session['logged_in'] != "vendor":
        return abort(403)
    '''
    vda = VendorDataAccess(mongo.db.vendors, "testing")
    output = vda.delete_menu_item(request.form)
    return jsonify(output)








# pmt routes
@app.route('/checkouts/new', methods=['GET'])
def new_checkout():
    client_token = braintree.ClientToken.generate()
    return render_template('checkouts/new.html', client_token=client_token)

@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = braintree.Transaction.find(transaction_id)
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('checkouts/show.html', transaction=transaction, result=result)

@app.route('/checkouts', methods=['POST'])
def create_checkout():
    result = braintree.Transaction.sale({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('new_checkout'))





if __name__ == '__main__':
    app.run(host="0.0.0.0")
