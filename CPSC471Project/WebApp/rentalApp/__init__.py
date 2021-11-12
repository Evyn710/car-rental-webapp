from flask import Flask
from rentalApp.forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cb839c3c5d3d87f7e7b6e85220a6ab6f'
bcrypt = Bcrypt(app)


from rentalApp import routes
