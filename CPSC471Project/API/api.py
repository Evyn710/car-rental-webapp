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
        # SELECT R.Make, R.Model, R.Color, R.City, R.Address
        #   FROM Rents as C, Rental as R
        #       WHERE C.Customer_id = %s (customer_id,) and
        #               R.Reg# = C.Reg#
        num = cursor.execute("SELECT R.Make, R.Model, R.Color, R.City, R.Address FROM Rents as C, Rental as R WHERE C.Customer_id = %s and R.Reg# = C.Reg#", (customer_id,))
        data = cursor.fetchall()
        cursor.close()
        return data

# EP6
class ClientInsurancePlans(Resource):
    def get(self):
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
class EmployeeGetRentalStatuses(Resource):
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
class EmployeeGetRentalStatus(Resource):
    def get(self, RegNo):
        # TODO, insert user verification with ID

        # SELECT *  -- Same as EP7, I think this just needs to return a status?
        #   FROM Rental
        #       WHERE Reg# = %s (RegNo,)
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT * FROM Rental WHERE Reg# = %s", (RegNo,))
        data = cursor.fetchone()
        cursor.close()
        return data

# EP9
class EmployeeGetAllGarages(Resource):
    def get(self):
        # TODO, insert user verification with ID

        # SELECT *  -- Pretty much the same as EP7, but I think this is fine as it is
        #   FROM Garage
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT * FROM Garage")
        data = cursor.fetchall()
        cursor.close()
        return data

# EP10
class EmployeeGetAllShuttles(Resource):
    def get(self,GarageNo):
        # TODO, insert user verification with ID

        # I need to clarify which capacity the end point is referring to
        # SELECT GS.Shuttle#, G.City, G.Address, COUNT(GS.Shuttle#), G.Capacity -- Idk about this count, it's says current capacity and total capacity but I'm a bit confused with which is stored in Garage
        #   FROM Garage_Shuttle as GS, Garage as G
        #       WHERE GS.Garage# = G.Garage#
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("")
        data = cursor.fetchall()
        cursor.close()
        return data
    
# EP11
class EmployeeAddRental(Resource):
    def post(self):
        new_rental = request.json

        # Checks the agent's input
        # I think I still need to check ALL the keys, but we can add that later
        keys = list(dict(request.json).keys())
        if keys[0] != 'Username' or keys[1] != 'Password' or len(keys) > 2:
            return 'Invalid input', 400

        # It seems there's a constraint with the city and address of the rental, where they need to exist at a location
        # So just need to check that
        # SELECT City, Address
        #   FROM Location
        #       WHERE City = '%s' and Address = '%s' (new_rental['City'],new_rental['Address'])
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT City, Address FROM Location WHERE City = '%s' and Address = '%s'", (new_rental['City'],new_rental['Address']))
        check = cursor.fetchall()

        if check:
            # INSERT INTO RENTAL (Color, Status, Make, Model, City, Address)
            #   VALUES (%s, %s, %s, %s, %s, %s) (you get the idea, this is new_rental's keys)
            # Defined the tuple here to ensure the line wasn't too long
            atts = (new_rental['Color'], new_rental['Status'], new_rental['Make'], new_rental['Model'], new_rental['City'], new_rental['Address'])
            cursor.execute("INSERT INTO RENTAL (Color, Status, Make, Model, City, Address) VALUES (%s, %s, %s, %s, %s, %s)", atts)
            cursor.commit()
            cursor.close()  # Not sure if this needs to be closed after a commit, but adding just in case
            return "Rental added"
        else:
            cursor.close()
            return "Location is not valid.", 400

# EP12
class EmployeeUpdateRentalStatus(Resource):
    def put(self):
        updated_rental = request.json

        # Checks the agent's input
        # I think I still need to check ALL the keys, but we can add that later
        keys = list(dict(request.json).keys())
        if keys[0] != 'Username' or keys[1] != 'Password' or len(keys) > 2:
            return 'Invalid input', 400

        # UPDATE Rental
        #   SET Status='%s'
        #       WHERE Reg#=%s
        cursor = con.cursor(dictionary=True)
        cursor.execute("UPDATE Rental SET Status='%s' WHERE Reg#=%s")
        cursor.close()
        return "Rental status updated"

# EP13
class EmployeeGetCustomerRental(Resource):
    def get(self, customer_id):
        # TODO, insert user verification with ID

        # SELECT R.Reg#, R.Make, R.Model, R.Color, R.City, R.Address, R.Status
        #   FROM Rental as R, Rents as C
        #       WHERE   C.Customer_id='%s' and
        #               C.Reg# = R.Reg# (customer_id,)
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("SELECT R.Reg#, R.Make, R.Model, R.Color, R.City, R.Address, R.Status FROM Rental as R, Rents as C WHERE   C.Customer_id='%s' and C.Reg# = R.Reg#")
        data = cursor.fetchall()
        cursor.close()
        return data

# EP14
class EmployeeGetHours(Resource):
    def get(self):
        # TODO, insert user verification with ID

        # SELECT E.Hours
        #   FROM Employee as E, Account as A    -- Going to assume that the account username is accessable
        #       WHERE E.Username = A.Username and
        #               E.SSN = ''-- I'm not sure how to get this data just yet
        cursor = con.cursor(dictionary=True)
        num = cursor.execute("")
        data = cursor.fetchall()
        cursor.close()
        return data

# adding each resource as an endpoint
api.add_resource(AvailableRentals, "/api/rentals")
api.add_resource(AvailableRentalCar, "/api/rentals/<int:RegNo>")
api.add_resource(AvailableRentalsCity, "/api/<city>/rentals")
api.add_resource(CurrentRentalsClient, "/api/user/rentals")
api.add_resource(NewUser, "/api/newuser")
api.add_resource(ClientRentHistory, "/api/user/rentals")
api.add_resource(ClientInsurancePlans, "/api/user/plans")
api.add_resource(EmployeeGetRentalStatuses, "/api/rentals_status")
api.add_resource(EmployeeGetRentalStatus, "/api/rentals_status/<int:RegNo>")
api.add_resource(EmployeeGetAllGarages, "/api/garages")
api.add_resource(EmployeeGetAllShuttles, "/api/garages/<int:garageNo>")
api.add_resource(EmployeeAddRental, "/api/rentals")
api.add_resource(EmployeeUpdateRentalStatus, "/api/rentals/<int:RegNo>")

@app.route('/')
@app.route('/api')
def root():
    return "<h1>API Page Version 0.1</h1>"


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)

