from flask import Flask, request, session, jsonify, url_for, redirect
from flask_pymongo import PyMongo
from server.data_access.user_data_access import UserDataAccess
import bcrypt
from functools import wraps
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'mysecret'
# mongodb database
app.config['MONGO_DBNAME'] = 'cloudlogin'
app.config['MONGO_URI'] = 'mongodb://user:user@ds055626.mlab.com:55626/cloudlogin'
# file upload
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = 'uploads/'

app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
# http://stackoverflow.com/questions/16499023/why-the-flask-teardown-request-can-not-get-exception-object-under-debug-mode-al

mongo = PyMongo(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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

'''
@application.route('/upload/<bid>', methods=['POST'])
def upload(bid):
    if not session or 'uid' not in session:
        return abort(403)
    else:
        photo_file = request.files['file']
        bid = int(bid)
        if photo_file and allowed_file(photo_file.filename):
            filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))

            f = open(os.path.join(application.config['UPLOAD_FOLDER'], filename), 'rb')
            conn = tinys3.Connection(S3_ACCESS_KEY, S3_SECRET_KEY, tls=True, endpoint='s3-us-west-2.amazonaws.com')
            conn.upload(filename, f, 'bike-share-comse6998')

            url = S3_BUCKET_URL + filename
            bda = BikeDataAccess(g.conn)
            output = bda.add_photo(url, bid)

            return jsonify(output)
        else:
            output = {
                'message': 'Unsupported file format',
                'status': False
            }

            return jsonify(output)
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
    session.pop(loggged_in, None)
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
    app.run(host="0.0.0.0", debug=False)
