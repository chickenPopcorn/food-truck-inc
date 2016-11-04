from flask import Flask, request, session, jsonify, url_for, redirect, abort
from flask_pymongo import PyMongo
from server.data_access.user_data_access import UserDataAccess
import bcrypt
from functools import wraps
from werkzeug.utils import secure_filename
import os
import braintree
from config import *
import tinys3


app = Flask(__name__)
app.config.from_object(config['default'])
config['default'].init_app(app)

mongo = PyMongo(app)

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="2yffqc6bmkqftb94",
                                  public_key="u6jkwvx3r6hj883x6",
                                  private_key="17d6d7c7473dc28eef407eb2d2c7abbe")

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

            f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
            conn = tinys3.Connection(S3_ACCESS_KEY, S3_SECRET_KEY, tls=True, endpoint='s3-eu-west-1.amazonaws.com')
            conn.upload(filename, f, 'cuisines')

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
@app.route('/upload/', methods=['GET', 'POST'])
def upload():

    if not session or 'uid' not in session:
        return abort(403)
    else:
        photo_file = request.files['file']
        bid = int()
        if photo_file and allowed_file(photo_file.filename):
            filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
            conn = tinys3.Connection(S3_ACCESS_KEY, S3_SECRET_KEY, tls=True, endpoint='s3-us-west-2.amazonaws.com')
            conn.upload(filename, f, 'cuisines-6998')

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
    app.run(host="0.0.0.0", debug=True)
