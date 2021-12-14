import requests
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

# initializing mysql
con = mysql.connector.connect(user='user', password='password', host='127.0.0.1', database='rentalcompany')

rental_put_args = reqparse.RequestParser()
rental_put_args.add_argument("RegNo", type=int, help="Should be null for new, regNo to overwrite")


# helper function to return what kind of user the user is
# helper function to return what kind of user the user is
def validate_user(username, password):
    cursor = con.cursor(dictionary=True)

    # find out if they are a user
    cursor.execute("SELECT Username, Password FROM account WHERE Username = %s", (username,))
    user = cursor.fetchone()
    if user and bcrypt.check_password_hash(password, user["Password"]):
        # check if they are an employee
        cursor.execute("SELECT Username FROM employee WHERE Username = %s", (username,))
        user = cursor.fetchone()
        if user:  # they are an employee
            # check if they are an agent
            cursor.execute("SELECT Agent_SSN FROM agent as a, employee as e WHERE " +
                           "a.Agent_SSN = e.SSN and e.Username = %s", (username,))
            agent = cursor.fetchone()
            if agent:
                return "agent"

            # check if they are a mechanic
            cursor.execute("SELECT Mechanic_SSN FROM mechanic as m, employee as e WHERE " +
                           "m.Mechanic_SSN = e.SSN and e.Username = %s", (username,))
            mechanic = cursor.fetchone()
            if mechanic:
                return "mechanic"

            # check if they are a manager
            cursor.execute("SELECT SSN FROM employee as e WHERE e.Username = %s", (username,))
            ssn = cursor.fetchone()
            cursor.execute("SELECT * FROM employee as e WHERE e.Mgr_ssn = %s", (ssn["SSN"],))
            manages = cursor.fetchone()
            if manages:
                return "manager"

            return "employee"
        else:
            return "user"
    else:
        return 401


class AvailableRentals(Resource):
    def get(self):  # get method for getting all rentals that are available
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT Make, Model, Color, City, Address FROM rental WHERE Status = 'available'")
        data = cursor.fetchall()
        cursor.close()
        return data


class AvailableRentalCar(Resource):
    def get(self, RegNo):
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT Make, Model, Color, City, Address FROM rental WHERE Status = 'available' and RegNo = %s", (RegNo,))
        data = cursor.fetchone()
        cursor.close()
        return data


class AvailableRentalsCity(Resource):
    def get(self, city):
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT Make, Model, Color, City, Address FROM rental WHERE City = %s", (city,))
        data = cursor.fetchall()
        cursor.close()
        return data


class CurrentRentalsClient(Resource):
    def get(self):
        # check input
        keys = list(dict(request.json).keys())
        if keys[0] != 'Username' or keys[1] != 'Password' or len(keys) != 2:
            return 'Invalid input', 400

        validation = validateUser(request.json['Username'], request.json['Password'])
        if validation == 401:
            # return authorization error
            return 'Invalid user', 401
        else:
            pass


class NewUser(Resource):
    def post(self):
        new_user = request.json

        # check input
        keys = list(dict(request.json).keys())
        if keys[0] != 'Username' or keys[1] != 'Password' or len(keys) > 2:
            return 'Invalid input', 400

        username = new_user['Username']
        password = new_user['Password']

        # check if username is taken
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * from account WHERE Username = %s", (username,))
        users = cursor.fetchall()
        if users:
            cursor.close()
            return "Username taken.", 400
        elif len(password) < 8 or len(password) > 40 or len(username) > 20 or len(username) < 5:
            cursor.close()
            return "Username must be between 5-20 characters, password must be 8-40.", 400
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
            cursor.execute("INSERT INTO account (Username, Password) VALUES (%s, %s)", (username, hashed_password))
            con.commit()
            return f"Account created successfully with username {username}"


# adding each resource as an endpoint
api.add_resource(AvailableRentals, "/api/rentals")
api.add_resource(AvailableRentalCar, "/api/rentals/<int:RegNo>")
api.add_resource(AvailableRentalsCity, "/api/<city>/rentals")
api.add_resource(CurrentRentalsClient, "/api/user/rentals")
api.add_resource(NewUser, "/api/newuser")


@app.route('/')
@app.route('/api')
def root():
    return "<h1>API Page Version 0.1</h1>"


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)

