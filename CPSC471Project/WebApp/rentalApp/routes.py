from flask import render_template, url_for, flash, redirect
from rentalApp import app
from rentalApp.forms import RegistrationForm, LoginForm
import requests
import json

API = "http://127.0.0.1:5001"


@app.route("/")
@app.route("/home")  # Our main page for the app
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/rentals")
def rentals():
    response = requests.get(API + "/rentals")
    return render_template('rentals.html', title='Rentals', response=json.loads(response.text))


@app.route("/rentals/<rentalid>")
def rentCar(rentalid):
    response = requests.get(API + "/rentals/" + rentalid)
    if json.loads(response.text) == None:
        flash('No existing rental', 'danger')
        return redirect(url_for('rentals'))

    return render_template('individualrental.html', title='Rentals', response=json.loads(response.text))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)