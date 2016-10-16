from wtforms import Form, BooleanField, TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(Form):
    username = TextField(
        u'Username', [DataRequired(), Length(min=4, max=25)]
    )
    password = PasswordField(
        u'Password',
        [DataRequired(), Length(min=6, max=25)]
    )

class RegisterForm(Form):
    username = TextField(
        u'Username',
        [DataRequired(), Length(min=4, max=25)]
    )
    lastname = TextField(
        u'Lastname',
        [DataRequired()]
    )
    firstname = TextField(
        u'Firstname',
        [DataRequired()]
    )
    email = TextField(
        u'Email',
        [DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        u'Password',
        [DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        u'Repeat password',
        [
            DataRequired(),
            EqualTo('Password', message='Passwords must match.')
        ]
    )

class ChangePasswordForm(Form):
    old_password = PasswordField(
        u'Old password',
        [DataRequired(), Length(min=6, max=25)]
    )
    new_password = PasswordField(
        u'New password',
        [DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        u'Repeat password',
        [
            DataRequired(),
            EqualTo('New password', message='Passwords must match.')
        ]
    )

class UpdateProfileForm(Form):
    lastname = TextField(
        u'Lastname',
        [DataRequired()]
    )
    firstname = TextField(
        u'Firstname',
        [DataRequired()]
    )
    email = TextField(
        u'Email',
        [DataRequired(), Email(message=None), Length(min=6, max=40)]
    )

