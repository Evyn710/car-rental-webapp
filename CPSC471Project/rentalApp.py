from flask import Flask, render_template, url_for

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
