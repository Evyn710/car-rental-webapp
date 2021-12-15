from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import mysql.connector
con = mysql.connector.connect(user='user', password='password', host='127.0.0.1', database='rentalcompany')

from rentalApp.forms import RegistrationForm, LoginForm, RentalForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cb839c3c5d3d87f7e7b6e85220a6ab6f'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from rentalApp import routes
