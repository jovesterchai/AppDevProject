from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, SelectMultipleField, DecimalField, IntegerField

class CreateUserFeedback(Form):
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')


class CreateProduct(Form):
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
