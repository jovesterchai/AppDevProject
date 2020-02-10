from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, SelectMultipleField, DecimalField, IntegerField, PasswordField, FileField

class CreateUserFeedback(Form):
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')

    
class CreateUserForm(Form):
    firstName = StringField("First Name", [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField("Last Name", [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField("Username",[validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.   DataRequired()])
    gender = SelectField("Gender", [validators.DataRequired()], choices=[("", "Select"), ("F", "Female"), ("M", "Male")], default = "")
    country = StringField("Country", [validators.Length(min=1, max=150), validators.DataRequired()])
    address = StringField ("Address", [validators.Length(min=1, max=150), validators.DataRequired()])
    number = IntegerField("Phone Number", [validators.NumberRange(min=10000000, message='Invalid Phone Number.'), validators.DataRequired()])

class LoginForm(Form):
    username = StringField("Username",[validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])


    
class CreateProduct(Form):
    itemID = IntegerField('Item ID', [validators.NumberRange(min=100000, max=999999, message='Invalid Item ID.')])
    name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    color = SelectMultipleField('Colors', [validators.DataRequired()], choices=[('Red Wine', 'Red Wine'), ('Black', 'Black'), ('Blue', 'Blue'), ('Firebrick', 'Firebrick'), ('Green', 'Green'), ('Light Blue', 'Light Blue'), ('Orange Gold', 'Orange Gold'), ('Pink', 'Pink'), ('Warm White', 'Warm White')], default='Red Wine')
    size = RadioField('Sizes', choices=[('S', 'S'), ('M', 'M'), ('L', 'L')], default='S')
    gender = SelectField('Gender', choices=[('', 'Select'), ('M', 'Male'), ('F', 'Female')], default='')
    price = DecimalField('Price', [validators.NumberRange(min=1, max=1000, message='Invalid Price.')])
    quantity = IntegerField('Quantity', [validators.NumberRange(min=1, max=500, message='Invalid Quantity.')])
    description = TextAreaField('Description', [validators.Optional()])


class AddToCart(Form):
    name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    color = SelectMultipleField('Colors', [validators.DataRequired()], choices=[('Red Wine', 'Red Wine'), ('Black', 'Black'), ('Blue', 'Blue'), ('Firebrick', 'Firebrick'), ('Green', 'Green'), ('Light Blue', 'Light Blue'), ('Orange Gold', 'Orange Gold'), ('Pink', 'Pink'), ('Warm White', 'Warm White')], default='Red Wine')
    size = RadioField('Sizes', choices=[('S', 'S'), ('M', 'M'), ('L', 'L')], default='S')
    gender = SelectField('Gender', choices=[('', 'Select'), ('M', 'Male'), ('F', 'Female')], default='')
    price = DecimalField('Price', [validators.NumberRange(min=1, max=1000, message='Invalid Price.')])
    quantity = IntegerField('Quantity', [validators.NumberRange(min=1, max=500, message='Invalid Quantity.')])
    description = TextAreaField('Description', [validators.Optional()])


class R(Form):
    name = StringField('name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('email', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = StringField('address', [validators.Length(min=1, max=150), validators.DataRequired()])
    city = StringField('city', [validators.Length(min=1, max=150), validators.DataRequired()])
    zip = IntegerField('zip', [validators.NumberRange(min=1000, max=10000000, message='Invalid Quantity.')])

class CreateFeedback(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    country = StringField('Country', [validators.Length(min=1, max=150), validators.DataRequired()])
    feedbackZ = TextAreaField('Feedback', [validators.Optional()])
