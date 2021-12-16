from flask import render_template, url_for, flash, redirect, request
from rentalApp import app, bcrypt
from rentalApp.forms import RegistrationForm, LoginForm, RentalForm
from rentalApp import con, login_manager
from rentalApp.user import User, validate_user
from flask_login import login_user, logout_user, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
@app.route("/home")  # Our main page for the app
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/rentals")
def rentals():
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rental WHERE Status = 'available'")
    data = cursor.fetchall()
    cursor.close()
    return render_template('rentals.html', title='Rentals', response=data)


@app.route("/rentals/<int:rentalid>", methods=["GET", "POST"])
def rentCar(rentalid):
    if request and request.method == "POST":
        if not current_user.is_authenticated:
            flash('You must make an account to rent!', "danger")
            return redirect(url_for('home'))

        cursor = con.cursor(dictionary=True)
        cursor.execute("UPDATE rental SET Status = 'rented' WHERE RegNo = %s", (str(rentalid),))
        con.commit()
        cursor.close()
        flash('Succesively rented the car!', "success")
        return redirect(url_for('rent'))

    cursor = con.cursor(dictionary=True)
    num = cursor.execute(
        "SELECT Make, Model, Color, City, Address FROM rental WHERE Status = 'available' and RegNo = %s", (str(rentalid),))
    data = cursor.fetchone()
    cursor.close()
    if data is None:
        flash('No existing rental', 'danger')
        return redirect(url_for('rentals'))

    return render_template('individualrental.html', title='Rentals', response=data, regNo=rentalid)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        cursor = con.cursor()
        account_query = "INSERT INTO account VALUES (%s, %s)"
        account_info = (str(form.username.data), hash_pw)
        cursor.execute(account_query, account_info)
        con.commit()
        cursor.close()

        flash('Account created successfully! You can now login any time!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(str(form.username.data))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash("Username or password doesn't match", 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/manage')
def manage():
    username = current_user.get_id()
    if current_user.is_authenticated:
        user = current_user.get(username)
        usertype = validate_user(username, user.password)
    else:
        flash("You do not have permissions for that.", 'danger')
        return redirect(url_for('home'))

    if usertype != "user":
        return render_template('manage.html')
    else:
        flash("You do not have permissions for that.", 'danger')
        return redirect(url_for('home'))


@app.route('/account')
def account():
    if not current_user.is_authenticated: # make sure user is logged in
        flash("You must log in first.", 'danger')
        return redirect(url_for('login'))

    return render_template('account.html')

@app.route('/addrental', methods=['GET', 'POST'])
def addrental():
    username = current_user.get_id()
    if current_user.is_authenticated:
        user = current_user.get(username)
        usertype = validate_user(username, user.password)
    else:
        flash("You do not have permissions for that.", 'danger')
        return redirect(url_for('home'))

    if usertype != "user":
        form = RentalForm()
        if form.validate_on_submit():
            print("submitted")
            cursor = con.cursor(dictionary=True)
            query = "INSERT INTO rental(Color, Status, Make, Model, City, Address)" \
                    "values(%s,%s,%s,%s,%s,%s)"
            location = form.location.data.split(', ')
            rental_info = (form.color.data, "available", form.make.data,
                           form.model.data, location[1], location[0])
            cursor.execute(query, rental_info)
            con.commit()
            cursor.close()

            flash('Rental added successfully!', 'success')
            return redirect(url_for('manage'))

        return render_template('addrental.html', form=form)
    else:
        flash("You do not have permissions for that.", 'danger')
        return redirect(url_for('home'))

