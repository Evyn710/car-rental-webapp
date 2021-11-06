from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

# Web app developed with reference to Corey Schafer's video series
# on Flask at https://www.youtube.com/watch?v=MwZwr5Tvyxo

app.config['SECRET_KEY'] = 'cb839c3c5d3d87f7e7b6e85220a6ab6f'

rentals = [
    {
        'brand': 'Ford',
        'model': 'Escape ST',
        'year': '2019'
    },
    {
        'brand': 'Hyundai',
        'model': 'Santa Fe',
        'year': '2013'
    }
]


@app.route("/")
@app.route("/home")  # Our main page for the app
def home():
    return render_template('home.html', rentals=rentals)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/rent")
def rent():
    return render_template('rent.html', title='Rent')


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


if __name__ == '__main__':
    app.run(debug=True)
