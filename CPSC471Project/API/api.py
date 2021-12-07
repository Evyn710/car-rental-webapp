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
def validateUser(username, password):
    cursor = con.cursor(dictionary=True)

    # find out if they are user
    cursor.execute("SELECT Username, Password FROM account WHERE Username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    if user and bcrypt.check_password_hash(user['Password'], password):
        # We're just going to assume that this returns a string that represents the user's position
        return "user"
    else:
        return 401

# EP1
class AvailableRentals(Resource):
    def get(self):  # get method for getting all rentals that are available
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT Make, Model, Color, City, Address FROM rental WHERE Status = 'available'")
        data = cursor.fetchall()
        cursor.close()
        return data

# EP3
class AvailableRentalCar(Resource):
    def get(self, RegNo):
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT Make, Model, Color, City, Address FROM rental WHERE Status = 'available' and RegNo = " + str(RegNo))
        data = cursor.fetchone()
        cursor.close()
        return data

# EP2
class AvailableRentalsCity(Resource):
    def get(self, city):
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT Make, Model, Color, City, Address FROM rental WHERE City = %s", (city,))
        data = cursor.fetchall()
        cursor.close()
        return data

# This looks unfinished, need to verify what this is meant to do
# So far it looks like EP5, but only for current rentals. Could be an Agent endpoint
class CurrentRentalsClient(Resource):
    def get(self):
        # check input
        keys = list(dict(request.json).keys())
        if keys[0] != 'Username' or keys[1] != 'Password' or len(keys) > 2:
            return 'Invalid input', 400

        validation = validateUser(request.json['Username'], request.json['Password'])
        if validation == 401:
            # return authorization error
            return 'Invalid user', 401
        else:
            pass

# EP4
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

# EP5
class ClientRentHistory(Resource):
    def get(self,customer_id):
        # TODO, insert user verification with ID
        # I'm not entirely familiar with how to get input from user, this may need to be fixed
        
        cursor = con.cursor(dictionary=True)
        # SELECT Make, Model, Color, City, Address
        #   FROM Rents
        #       WHERE Customer_id = %s (customer_id,)
        num = cursor.execute("SELECT Make, Model, Color, City, Address FROM RENTS WHERE Customer_id = %s", (customer_id,))
        data = cursor.fetchall()
        cursor.close()
        return data

# EP6
class ClientInsurancePlans(Resource):
    def get(self,customer_id):
        # TODO, insert user verification with ID
        
        # SELECT IP.Plan#, IT.Price, IP.Coverage, A.Agent_name
        #   FROM Insurance_plan as IP, Insurance_transaction as IT, agent as A  -- Aliases needed, as there are 2 instances of Plan#
        #       WHERE IT.Customer_id = %s (customer_id,) and
        #               IP.Plan# = IT.Plan#
        #               IT.Agent_SSN = -- TODO This is going to need to be fixed, ot else I can't access agent's name
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT IP.Plan#, IT.Price, IP.Coverage, A.Agent_name FROM Insurance_plan as IP, Insurance_transaction as IT, agent as A WHERE ", (customer_id,))
        data = cursor.fetchall()
        cursor.close()
        return data

# EP7
class AgentGetRentalStatuses(Resource):
    def get(self):
        # TODO, insert user verification with ID

        # SELECT *  -- Looks like the output is just the entire Rental table at the moment. Maybe we could reduce it to just Reg# and Status?
        #   FROM Rental
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT * FROM Rental")
        data = cursor.fetchall()
        cursor.close()
        return data

# EP8
class AgentGetRentalStatus(Resource):
    def get(self, RegNo):
        # TODO, insert user verification with ID

        # SELECT *  -- Same as EP7, I think this just needs to return a status?
        #   FROM Rental
        #       WHERE Reg# = %s (RegNo,)
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT * FROM Rental WHERE Reg# = %s", (RegNo,))
        data = cursor.fetchall()
        cursor.close()
        return data

# EP9

# adding each resource as an endpoint
api.add_resource(AvailableRentals, "/api/rentals")
api.add_resource(AvailableRentalCar, "/api/rentals/<int:RegNo>")
api.add_resource(AvailableRentalsCity, "/api/<city>/rentals")
api.add_resource(CurrentRentalsClient, "/api/user/rentals")
api.add_resource(NewUser, "/api/newuser")
api.add_resource(ClientRentHistory, "/api/user/rentals")
api.add_resource(ClientInsurancePlans, "/api/user/plans")
api.add_resource(AgentGetRentalStatuses, "/api/rentals_status")
api.add_resource(AgentGetRentalStatus, "/api/rentals_status/<int:RegNo>")


@app.route('/')
@app.route('/api')
def root():
    return "<h1>API Page Version 0.1</h1>"


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)

