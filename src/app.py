from flask import Flask, request, session, jsonify, url_for, redirect, abort
from flask_pymongo import PyMongo
from server.data_access.user_data_access import UserDataAccess
import bcrypt
from functools import wraps
from werkzeug.utils import secure_filename
from os.path import join, dirname
from dotenv import load_dotenv
import os
import braintree
import boto


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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():

    if not session or 'logged_in' not in session:
        return abort(403)
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
            path = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])
            # for testing saved locally
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            file.save(os.path.join(path, filename))

            '''
            conn = boto.connect_s3(app.config['S3_ACCESS_KEY'], app.config['S3_SECRET_KEY'])
            bucket = conn.get_bucket(bucketName, validate=False)
            # create our file on s3
            sml = bucket.new_key('/'.join([session['username'], filename]))
            # save the file contents
            sml.set_contents_from_string(file.read())
            # set appropriate ACL
            sml.set_acl('public-read')
            '''
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

# log in API post only
@app.route('/login', methods=['POST'])
def login():
    uda = UserDataAccess(mongo.db.customeruserlogin)
    output = uda.authorize(request.form)
    if output['status']:
        session['logged_in'] = True
        session['username'] = output['result']['user']['username']
    return jsonify(output)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({"status": True, "message": "You logged out!"})

# register in API post only
@app.route('/register', methods=['POST'])
def register():
    uda = UserDataAccess(mongo.db.customeruserlogin)
    output = uda.register(request.form)
    return jsonify(output)

# testing use
@app.route('/delete', methods=['POST'])
def deleteUser():
    uda = UserDataAccess(mongo.db.customeruserlogin)
    output = uda.delete(request.form)
    return jsonify(output)

@app.route('/changePassword', methods=['POST'])
@login_required
def changePassword():
    uda = UserDataAccess(mongo.db.customeruserlogin)
    output = uda.change_password(request.form, session['username'])
    return jsonify(output)

@app.route('/updateProfile', methods=['POST'])
@login_required
def updateProfile():
    uda = UserDataAccess(mongo.db.customeruserlogin)
    output = uda.update_profile(request.form)
    return jsonify(output)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
