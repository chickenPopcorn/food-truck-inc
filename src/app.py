from flask import Flask, request, session, jsonify
from flask_pymongo import PyMongo
from server.data_access.user_data_access import UserDataAccess
import bcrypt


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'cloudlogin'
app.config['MONGO_URI'] = 'mongodb://user:user@ds055626.mlab.com:55626/cloudlogin'

mongo = PyMongo(app)

# testing route
@app.route('/')
def hello_world():
    return 'Hello, World!'


# log in API post only
@app.route('/login', methods=['POST'])
def login():
    uda = UserDataAccess(mongo.db.customeruserlogin)
    output = uda.authorize(request.form)
    return jsonify(output)

# register in API post only
@app.route('/register', methods=['POST'])
def register():
    uda = UserDataAccess(mongo.db.customeruserlogin)
    output = uda.register(request.form)
    return jsonify(output)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host="0.0.0.0", debug=False)
