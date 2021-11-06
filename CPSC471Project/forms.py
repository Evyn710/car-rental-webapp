from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=40)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(min=8, max=32), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
