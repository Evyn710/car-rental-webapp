import datetime
import random

from flask import render_template, url_for, flash, redirect, request
from rentalApp import app, bcrypt
from rentalApp.forms import RegistrationForm, LoginForm, AddRentalForm, RentalForm, AddHours
from rentalApp import con, login_manager
from rentalApp.user import User, validate_user
from flask_login import login_user, logout_user, current_user
from datetime import date


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
    form = RentalForm()
    if not current_user.is_authenticated:
        flash('You must make an account to rent!', "danger")
        return redirect(url_for('home'))

    if form.validate_on_submit():
        cursor = con.cursor(dictionary=True)
        cursor.execute("UPDATE rental SET Status = 'rented' WHERE RegNo = %s", (str(rentalid),))
        con.commit()

        cursor.execute("SELECT * FROM rental WHERE RegNo = %s", (str(rentalid),))
        result = cursor.fetchone()

        price = result["Price"]
        coverage = form.insurance_type.data
        insurance_price = 0
        if coverage == "partial":
            insurance_price = price * 0.05 * int(form.days.data)
        else:
            insurance_price = price * 0.10 * int(form.days.data)

        cursor.execute("INSERT INTO insurance_plan (Price, Coverage) VALUES (%s,%s)", (insurance_price, coverage))
        con.commit()

        cursor.execute("SELECT last_insert_id()")
        plan_no = cursor.fetchone()["last_insert_id()"]

        cursor.execute("SELECT * FROM agent")
        agent_list = cursor.fetchall()
        agents = []
        for a in agent_list:
            agents.append(a["Agent_SSN"])

        agent = random.choice(agents)

        cursor.execute("SELECT ID FROM customer WHERE Username = %s", (current_user.get_id(),))
        cust = cursor.fetchone()["ID"]

        cursor.execute("INSERT INTO insurance_transaction VALUES (%s,%s,%s);", (int(cust), int(plan_no), int(agent)))
        con.commit()

        today = date.today()
        start_date = today.strftime("%Y-%m-%d")
        end_date = today + datetime.timedelta(days=int(form.days.data))

        cursor.execute("INSERT INTO rents VALUES(%s,%s,%s,%s,%s)",
                       (int(cust), int(rentalid), float(price) * int(form.days.data), start_date, end_date))
        con.commit()

        cursor.close()
        flash('Successfully rented the car!', "success")
        return redirect(url_for('home'))

    cursor = con.cursor(dictionary=True)
    num = cursor.execute(
        "SELECT Make, Model, Color, City, Address, Price FROM rental WHERE Status = 'available' and RegNo = %s",
        (str(rentalid),))
    data = cursor.fetchone()
    cursor.close()
    if data is None:
        flash('No existing rental', 'danger')
        return redirect(url_for('rentals'))

    return render_template('individualrental.html', title='Rentals', response=data, regNo=rentalid, form=form)


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

        cursor.execute("INSERT INTO customer (Username, Name) VALUES (%s, %s)", (form.username.data, form.name.data))
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


@app.route('/manage', methods=['GET', 'POST'])
def manage():
    form = AddHours()
    username = current_user.get_id()
    if current_user.is_authenticated:
        user = current_user.get(username)
        usertype = validate_user(username, user.password)
    else:
        flash("You do not have permissions for that.", 'danger')
        return redirect(url_for('home'))

    if usertype != "user" and usertype != 401:
        if form.validate_on_submit():
            cursor = con.cursor(dictionary=True)
            cursor.execute("SELECT Hours FROM employee WHERE Username = %s", (username,))
            hours = cursor.fetchone()['Hours']
            new_hours = hours + int(form.hours.data)

            cursor.execute("UPDATE employee SET Hours = %s WHERE Username = %s", (new_hours, username))
            con.commit()
            cursor.close()

        return render_template('manage.html', form=form)
    else:
        flash("You do not have permissions for that.", 'danger')
        return redirect(url_for('home'))


@app.route('/account')
def account():
    if not current_user.is_authenticated:  # make sure user is logged in
        flash("You must log in first.", 'danger')
        return redirect(url_for('login'))

    username = current_user.get_id()
    user = current_user.get(username)
    usertype = validate_user(username, user.password)

    cursor = con.cursor(dictionary=True)
    query = "SELECT r.Model, r.Make, t.Price, t.Start_date, t.End_date" \
            " FROM rents as t, rental as r, customer as c WHERE c.Username = %s" \
            " and c.ID = t.Customer_id and r.RegNo = t.RegNo"
    cursor.execute(query, (username,))
    rentals = cursor.fetchall()
    cursor.close()

    if usertype != "user" and usertype != 401:  # display for employees
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT Hours FROM employee WHERE Username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        hours = result["Hours"]
        return render_template('account.html', hours=hours, rentals=rentals)

    return render_template('account.html', rentals=rentals)


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
        form = AddRentalForm()
        if form.validate_on_submit():
            print("rental submitted")
            cursor = con.cursor(dictionary=True)
            query = "INSERT INTO rental(Color, Status, Make, Model, City, Address, Price)" \
                    "values(%s,%s,%s,%s,%s,%s,%s)"
            location = form.location.data.split(', ')
            rental_info = (form.color.data, "available", form.make.data,
                           form.model.data, location[1], location[0], float(form.price.data))
            cursor.execute(query, rental_info)
            con.commit()
            cursor.close()

            flash('Rental added successfully!', 'success')
            return redirect(url_for('manage'))

        return render_template('addrental.html', form=form)
    else:
        flash("You do not have permissions for that.", 'danger')
        return redirect(url_for('home'))
