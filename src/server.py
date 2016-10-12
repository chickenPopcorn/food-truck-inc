from flask import Flask, request, session, jsonify
from flask_pymongo import PyMongo
import bcrypt


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'cloudlogin'
app.config['MONGO_URI'] = 'mongodb://user:user@ds055626.mlab.com:55626/cloudlogin'

mongo = PyMongo(app)

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username' : request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return jsonify({'status': 200})
            # login successful

    return jsonify({'status': 400})
    # login failed

@app.route('/register', methods=['POST'])
def register():
    users = mongo.db.users
    existing_user = users.find_one({'name' : request.form['username']})
    if existing_user is None:
        hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        users.insert({'username' : request.form['username'], 'password' : hashpass})
        session['username'] = request.form['username']
        return jsonify({'status': 202})
        # registraton accepted

    return jsonify({'status': 404})
    # user already exist


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
