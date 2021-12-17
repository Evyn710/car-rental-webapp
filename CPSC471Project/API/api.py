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
        num = cursor.execute("SELECT Make, Model, Color, City, Address FROM rental WHERE Status = 'available' and RegNo = " + str(RegNo))
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
        if keys[0] != 'Username' or keys[1] != 'Password' or len(keys) > 2:
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

#Endpoint 15
class AgentGetInsurancePlans(Resource):
    def get(self):
        validation = validate_user(request.json['Username'], request.json['Password'])
        print(username)
        if validation != 'agent' and validation != 401:
            # SELECT IP.Plan#, IP.Price, IP.Coverage
            # FROM Insurance_Plan as IP
            cursor = con.cursor(dictionary=True)
            num = cursor.execute(
                "SELECT IP.Plan#, IP.Price, IP.Coverage FROM Insurance_Plan as IP")
            data = cursor.fetchall()
            cursor.close()
            return data
        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401

#Endpoint 16
class AgentGetActiveInsurancePlans(Resource):
    def get(self, clientID):
        validation = validate_user(request.json['Username'], request.json['Password'])
        print(username)
        if validation != 'agent' and validation != 401:
            # SELECT IP.Plan#, IP.Price, IP.Coverage
            # FROM Insurance_Plan as IP, Customer_Account as CA
            # WHERE IP.Plan# = IT.Plan# and IT.Customer_id = CA.Customer_id and CA.Customer_id = %s
            cursor = con.cursor(dictionary=True)
            num = cursor.execute(
            "SELECT IP.Plan#, IP.Price, IP.Coverage"
            "FROM Insurance_Plan as IP, Insurance_Transaction as IT, Customer_Account as CA"
            "WHERE IP.Plan# = IT.Plan# and IT.Customer_id = CA.Customer_id and CA.Customer_id = %s", clientID)
            data = cursor.fetchall()
            cursor.close()
            return data
        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401

#Endpoint 19
class MechanicGetWorks(Resource):
    def get(self, Mechanic_SSN):
        validation = validate_user(request.json['Username'], request.json['Password'])
        print(username)
        if validation != 'agent' and validation != 401:
            # SELECT WI.City, WI.Address, WI.Garage#, WI.Hours
            # FROM Mechanic as M, Works_in as WI
            # WHERE M.Mechanic_SSN = WI.Mechanic_SSN and Mechanic_SSN = %s
            cursor = con.cursor(dictionary=True)
            num = cursor.execute(
            "SELECT WI.City, WI.Address, WI.Garage#, WI.Hours"
            "FROM Mechanic as M, Works_in as WI"
            "WHERE M.Mechanic_SSN = WI.Mechanic_SSN and Mechanic_SSN = %s", (Mechanic_SSN))
            data = cursor.fetchall()
            cursor.close()
            return data
        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401
#Endpoint 20
class MechanicGetAllServices(Resource):
    def get(self):
        validation = validate_user(request.json['Username'], request.json['Password'])
        print(username)
        if validation != 'mechanic' and validation != 401:
            # SELECT RS.Reg#, RS.Date, RS.Hours
            # FROM Rental_Service as RS
            cursor = con.cursor(dictionary=True)
            num = cursor.execute(
            "SELECT RS.Reg#, RS.Date, RS.Hours FROM Rental_Service as RS")
            data = cursor.fetchall()
            cursor.close()
            return data
        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401

#Endpoint 21
class MechanicGetAllRegnoServices(Resource):
    def get(self, RegNo):
        validation = validate_user(request.json['Username'], request.json['Password'])
        print(username)
        if validation != 'mechanic' and validation != 401:
            # SELECT RS.Reg#, RS.Date, RS.Hours
            # FROM Rental_Service as RS, Rental as R
            # WHERE RS.Reg# = %s (RegNo)
            cursor = con.cursor(dictionary=True)
            num = cursor.execute(
            "SELECT RS.Reg#, RS.Date, RS.Hours "
            "FROM Rental_Service as RS, Rental as R"
            "WHERE RS.Reg# = %s and RS.Reg# = R.Reg#", (RegNo))
            data = cursor.fetchall()
            cursor.close()
            return data
        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401

#Endpoint 22
class MechanicGetAllShuttleServices(Resource):
    def get(self, RegNo):
        validation = validate_user(request.json['Username'], request.json['Password'])
        print(username)
        if validation != 'mechanic' and validation != 401:
            # SELECT SServ.Shuttle#, SServ.Date, SServ.Hours
            # FROM Shuttle_Service as Sserv
            cursor = con.cursor(dictionary=True)
            num = cursor.execute( 
            "SELECT SServ.Shuttle#, SServ.Date, SServ.Hours FROM Shuttle_Service as SServ")
            data = cursor.fetchall()
            cursor.close()
            return data
        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401

#Endpont 24
class EmployeeUpdateRentalStatus(Resource):
    def put(self, ShuttleNo, Airport, Schedule):
      try:
        updated_shuttle = request.json

        #check input
        validation = validate_user(request.json['Username'], request.json['Password'])
        if validation != 'agent' and validation != 401:
            # UPDATE Shuttle
            #   SET Airport_name='%s', Schedule='%s'
            #       WHERE Shuttle#=%s
            cursor = con.cursor()
            num = cursor.execute("UPDATE Shuttle SET Airport_name='%s', Schedule='%s' WHERE Shuttle#=%s", (updated_shuttle['Airport']), updated_shuttle['Schedule'], ShuttleNo)
            con.commit()
            cursor.close()
            return f"Shuttle Aiport, Schedule updated at {ShuttleNo}"
        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401
      except:
         return 'Invalid input', 400

#Endpoint 25
class MechanicGetAllShuttlenoServices(Resource):
    def get(self, ShuttleNo):
        validation = validate_user(request.json['Username'], request.json['Password'])
        print(username)
        if validation != 'mechanic' and validation != 401:
            # SELECT SServ.Shuttle#, SServ.Date, SServ.Hours
            # FROM Shuttle_Service as Sserv, Shuttle as S
            # WHERE SServ.Shuttle# = %s and SServ.Shuttle# = S.Shuttle#
            cursor = con.cursor(dictionary=True)
            num = cursor.execute( 
            "SELECT SServ.Shuttle#, SServ.Date, SServ.Hours"
            "FROM Shuttle_Service as Sserv, Shuttle as S"
            "WHERE SServ.Shuttle# = %s and SServ.Shuttle# = S.Shuttle#)", (ShuttleNo))
            data = cursor.fetchall()
            cursor.close()
            return data
        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401


# adding each resource as an endpoint
api.add_resource(AvailableRentals, "/api/rentals")
api.add_resource(AvailableRentalCar, "/api/rentals/<int:RegNo>")
api.add_resource(AvailableRentalsCity, "/api/<city>/rentals")
api.add_resource(CurrentRentalsClient, "/api/user/rentals")
api.add_resource(NewUser, "/api/newuser")
api.add_resource(AgentGetInsurancePlans, "/api/insuranceplans")
api.add_resource(AgentGetActiveInsurancePlans, "api/<int:customerid>/insuranceplans")
api.add_resource(MechanicGetWorks, "api/mechanic/work")
api.add_resource(MechanicGetAllServices, "api/rentalservices")
api.add_resource(MechanicGetAllRegnoServices, "rentalservices/<int:regNo>")
api.add_resource(MechanicGetAllShuttleServices, "api/shuttleservices")
api.add_resource(EmployeeUpdateRentalStatus, "api/shuttles/<int:shuttleNo>")
api.add_resource(MechanicGetAllShuttlenoServices, "api/shuttleservices/<int:shuttleNo>")

@app.route('/')
@app.route('/api')
def root():
    return "<h1>API Page Version 0.1</h1>"


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)

