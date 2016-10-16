import bcrypt
from forms import LoginForm, RegisterForm, ChangePasswordForm, UpdateProfileForm, DeleteForm

class UserDataAccess:
    def __init__(self, users):
        self.users = users

    def authorize(self, requestForm):
        user, status, message = UserDataAccess.init_output()
        form = LoginForm(requestForm)
        if form.validate():
            login_user = self.users.find_one({
                'username' : form.username.data,
                })

            if login_user and UserDataAccess.check_ps(login_user, form.password.data):
                    status = True
                    message = 'Login successful!'
                    user = UserDataAccess.return_user(login_user)
            else:
                message = 'The username and password does not match!'
        else:
            message = "Invalide form"
        return UserDataAccess.return_output(status, message, user)

    @staticmethod
    def check_ps(login_user, password):
        return bcrypt.hashpw(password.encode('utf-8'), \
        login_user["password"].encode('utf-8')) \
        == login_user["password"].encode('utf-8')

    def register(self, requestForm):
        user, status, message = UserDataAccess.init_output()
        form = RegisterForm(requestForm)

        if form.validate():
            is_unique, message = self.__is_unique(form.username.data, form.email.data)
            if not is_unique:
                message = "email or username already registered"
                return UserDataAccess.return_output(status, message, {})
            else:
                status = True
                hashpass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
                self.users.insert({
                    "email": form.email.data,
                    "password": hashpass,
                    "firstname": form.firstname.data,
                    "lastname": form.lastname.data,
                    "username": form.username.data

                })
                # TODO add creationdate
                # user['creationdate'] = creationdate
                login_user = self.users.find_one({
                    'username' : form.username.data,
                })
                message = 'The registration is successful!'
                user = UserDataAccess.return_user(login_user)
        else:
            message = "Invalide form"
        return UserDataAccess.return_output(status, message, user)

    def __is_unique(self, username, email):
        message = 'You can use this username and email!'
        status = True
        if self.users.find_one({'username' : username}):
            status = False
            message = 'The username has been taken!'
        if status:
            if self.users.find_one({'email' : email}):
                status = False
                message = 'The email has been taken!'
        return status, message

    @staticmethod
    def init_output():
        return {}, False, ""

    @staticmethod
    def return_user(user_info):
        return {
            'username': user_info["username"],
            'lastname': user_info["lastname"],
            'firstname': user_info["firstname"],
            'email': user_info["email"]
        }

    @staticmethod
    def return_output(status, message, user):
        return {
            'status': status,
            'message': message,
            'result': {
                'user': user
            }
        }

    def __is_your_email_unique(self, email):
        if self.users.find_one({'email':email}):
            return False, 'The email has been taken!'
        return True, 'You can use this email!'

    def update_profile(self, requestForm):
        user, status, message = UserDataAccess.init_output()
        form = UpdateProfileForm(requestForm)
        if form.validate():
            status, message = self.__is_your_email_unique(form.email.data)
            if status:
                message = 'You have successfully updated your profile!'
                self.users.update(
                    {'username': username},
                    {"email": email, "firsname": fistname, "lastname": lastname},
                    { upsert: True }
                )
        return UserDataAccess.return_output(status, message, {})

    def change_password(self, requestForm, username):
        user, status, message = UserDataAccess.init_output()
        form = ChangePasswordForm(requestForm)
        if form.validate():
            login_user = self.users.find_one({
                'username' : username,
            })
            if login_user and UserDataAccess.check_ps(login_user, form.oldpassword.data):
                self.users.update_one(
                    {'username': login_user["username"]},
                    {'$set': {"password":
                        bcrypt.hashpw(form.newpassword.data.encode('utf-8'), bcrypt.gensalt())
                    }}
                )
                status = True
                message = 'Your password has been changed!'
            else:
                message = 'The old password is NOT correct!'
        else:
            message = "Invalide form"
        return UserDataAccess.return_output(status, message, {})

    def delete(self, requestForm):
        user, status, message = UserDataAccess.init_output()
        form = DeleteForm(requestForm)
        if form.validate():
            login_user = self.users.find_one({
                'username' : form.username.data,
            })

            if UserDataAccess.check_ps(login_user, form.password.data):
                self.users.delete_one(
                    { 'username': form.username.data}
                )
                status = True
                message = 'Your account has been deleted!'
        else:
            message = 'Missing info!'
        return UserDataAccess.return_output(status, message, {})
    '''

    def get_user(self, user_id):
        output = {'result': {}, 'status': False, 'message': ''}
        user = {}
        cursor = self.conn.execute('select u.* from users u where u.uid=%s', user_id)
        for row in cursor:
            user = dict(row)
            del user['password']
        cursor.close()

        output['status'] = True
        output['result']['user'] = user

        return output
    '''
