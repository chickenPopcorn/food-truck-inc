from flask import Flask, request, session, jsonify
from flask_pymongo import PyMongo
from server.data_access.user_data_access import UserDataAccess
import bcrypt
from functools import wraps




app = Flask(__name__)
app.secret_key = 'mysecret'
app.config['MONGO_DBNAME'] = 'cloudlogin'
app.config['MONGO_URI'] = 'mongodb://user:user@ds055626.mlab.com:55626/cloudlogin'
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
# http://stackoverflow.com/questions/16499023/why-the-flask-teardown-request-can-not-get-exception-object-under-debug-mode-al

mongo = PyMongo(app)

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
