from wtforms import Form, BooleanField, TextField, PasswordField, IntegerField, FileField, FloatField, DateTimeField, FieldList, StringField, FormField
from wtforms import validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
import imghdr

class LoginForm(Form):
    username = TextField(
        u'Username', [DataRequired(), Length(min=4, max=25)]
    )
    password = PasswordField(
        u'Password',
        [DataRequired(), Length(min=6, max=25)]
    )

class DeleteForm(Form):
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
        u'Last Name',
        [DataRequired()]
    )
    firstname = TextField(
        u'First Name',
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
        u'Repeat Password',
        [
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )


class CustomerRegisterForm(RegisterForm):
    cell = TextField(
        u'Cellphone',
        [DataRequired(), Length(min=10, max=10)]
    )


class VendorRegisterForm(RegisterForm):
    storeName = TextField(
        u'Store Name',
        [DataRequired()]
    )


class ChangePasswordForm(Form):
    oldpassword = PasswordField(
        u'Old password',
        [DataRequired(), Length(min=6, max=25)]
    )
    newpassword = PasswordField(
        u'New password',
        [DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        u'Confirm',
        [
            DataRequired(),
            EqualTo('newpassword')
        ]
    )


class UpdateProfileForm(Form):
    lastname = TextField(
        u'Last Name',
        [DataRequired()]
    )
    firstname = TextField(
        u'First Name',
        [DataRequired()]
    )
    email = TextField(
        u'Email',
        [DataRequired(), Email(message="Incorrect email format")]
    )


class VendorAddMenuItem(Form):
    itemname = TextField(
        u'Item Name',
        [DataRequired()]
    )

    price = FloatField(
        u'Price',
        [DataRequired(), NumberRange(min=0, message="Price must be non-negative")]
    )

    '''
    img = FileField(
        u'Image',
        [DataRequired(), ImageFileRequired()]
    )
    '''


class ItemForm(Form):
    itemname = StringField(
        u'Item Name',
        [DataRequired()]
    )

    price = FloatField(
        u'Price',
        [DataRequired(), NumberRange(min=0, message="Price must be non-negative")]
    )

    quantity = IntegerField(
        u'Quantity',
        [DataRequired(), NumberRange(min=0, message="Quantity must be non-negative")]
    )


class CustomerOrderForm(Form):
    vendor = TextField(
        u'Vendor',
        [DataRequired()]
    )

    items = FieldList(FormField(ItemForm))

    # timestamp = DateTimeField(
    #     u'Timestamp',
    #     [DataRequired()],
    #     format='%Y-%m-%d %H:%M:%S')


class UpdateOrderStatusForm(Form):
    id = StringField(
        u'Id',
        [DataRequired()]
    )


class ImageFileRequired(object):
    """
    Validates that an uploaded file from a flask_wtf FileField is, in fact an
    image.  Better than checking the file extension, examines the header of
    the image using Python's built in imghdr module.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        if field.data is None:
            message = self.message or 'An image file is required'
            raise validators.StopValidation(message)
        if imghdr.what('unused', field.data.read()) not in ALLOWED_EXTENSIONS:
            raise ValidationError("image file type not supported")
        field.data.seek(0)


class VendorDeleteMenuItem(Form):
    itemname = TextField(
        u'Item Name',
        [DataRequired()]
    )
