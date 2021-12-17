from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from rentalApp import con


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=40)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(min=8, max=40), EqualTo('password')])
    name = StringField("Name", validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        # check if username is unique
        cursor = con.cursor(dictionary=True)
        username_check_query = "SELECT Username FROM account WHERE Username = %s"
        cursor.execute(username_check_query, (str(username.data),))
        account = cursor.fetchall()
        cursor.close()
        if account:
            raise ValidationError('Username is taken. Try another.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_username(self, username):
        # check if username is unique
        cursor = con.cursor(dictionary=True)
        username_check_query = "SELECT Username FROM account WHERE Username = %s"
        cursor.execute(username_check_query, (str(username.data),))
        account = cursor.fetchall()
        cursor.close()
        if not account:
            raise ValidationError('No account exists with that username')


class AddRentalForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired(), Length(min=1)])

    model = StringField('Model', validators=[DataRequired(), Length(min=1)])

    color = StringField('Color', validators=[DataRequired(), Length(min=1)])

    price = StringField('Price', validators=[DataRequired()])

    cursor = con.cursor(dictionary=True)
    location_query = "SELECT City, Address FROM location"
    cursor.execute(location_query)
    locations = cursor.fetchall()

    location_choices = []
    for loc in locations:
        city = loc['City']
        address = loc['Address']
        full_loc = address + ', ' + city
        location_choices += (full_loc,)

    location = SelectField('Location', choices=location_choices)

    submit = SubmitField('Add')

    def validate_price(self, price):
        try:
            num = float(price.data)
            if num < 0:
                raise ValidationError("Price must be positive")
        except:
            raise ValidationError("Price must be a number")


class RentalForm(FlaskForm):
    days = StringField("Number of days to rent", validators=[DataRequired()])

    insurance_type = SelectField("Insurance Type", choices=["partial", "full"])

    submit = SubmitField('Rent!')

    def validate_days(self, days):
        try:
            num = int(days.data)
            if num <= 0:
                raise ValidationError("Days must be equal or greater than one.")
        except:
            raise ValidationError("Days must be a number")


class AddHours(FlaskForm):
    hours = StringField("Hours", validators=[DataRequired()])

    submit = SubmitField('Add')

    def validate_hours(self, hours):
        try:
            num = int(hours.data)
            if num <= 0:
                raise ValidationError("Hours must be equal or greater than one.")
        except:
            raise ValidationError("Hours must be a number")