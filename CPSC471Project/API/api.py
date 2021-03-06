import requests
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import mysql.connector
from flask_bcrypt import Bcrypt
from datetime import date, datetime

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

# initializing mysql
con = mysql.connector.connect(user='user', password='password', host='127.0.0.1', database='rentalcompany',
                              buffered=True)

rental_put_args = reqparse.RequestParser()
rental_put_args.add_argument("RegNo", type=int, help="Should be null for new, regNo to overwrite")


# helper function to return what kind of user the user is
def validate_user(username, password):
    cursor = con.cursor(dictionary=True)

    # find out if they are a user
    cursor.execute("SELECT Username, Password FROM account WHERE Username = %s", (username,))
    user = cursor.fetchone()
    if user and bcrypt.check_password_hash(user["Password"], password):
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
        num = cursor.execute(
            "SELECT Make, Model, Color, City, Address FROM rental WHERE Status = 'available' and RegNo = %s", (RegNo,))
        data = cursor.fetchone()
        cursor.close()
        return data


# EP2
class AvailableRentalsCity(Resource):
    def get(self, city):
        cursor = con.cursor(dictionary=True)
        num = cursor.execute(
            "SELECT Make, Model, Color, City, Address FROM rental WHERE City = %s and Status = 'available'", (city,))
        data = cursor.fetchall()
        cursor.close()
        return data


# EP4
class NewUser(Resource):
    def post(self):
        try:
            new_user = request.json
            username = new_user['Username']
            password = new_user['Password']
            name = new_user['Name']

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

                cursor.execute("INSERT INTO customer (Username, Name) VALUES (%s, %s)", (username, name))
                return f"Account created successfully with username {username}"
        except:
            return "Invalid input", 401


# EP5
class ClientRentHistory(Resource):
    def get(self):
        # This query needs to be updated due to how input is taken
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])
            if validation != 401:
                cursor = con.cursor(dictionary=True)
                # SELECT R.Make, R.Model, R.Color, R.City, R.Address
                #   FROM Rents as C, Rental as R, Customer_Account as CA
                #       WHERE   CA.username = %s and
                #               C.Customer_id = CA.ID and
                #               R.RegNo = C.RegNo
                num = cursor.execute(
                    "SELECT R.Make, R.Model, R.Color, R.City, R.Address FROM Rents as C, Rental as R, "
                    "Customer as CA WHERE CA.username = %s and C.Customer_id = CA.ID and R.RegNo = C.RegNo",
                    (request.json['Username'],))
                data = cursor.fetchall()
                cursor.close()
                return data
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# EP6
class ClientInsurancePlans(Resource):
    def get(self):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation != 401:
                # SELECT IP.Plan#, IT.Price, IP.Coverage, E.Agent_name
                #   FROM Insurance_plan as IP, Insurance_transaction as IT, employee as E  -- Aliases needed, as there are 2 instances of Plan#
                #       WHERE IT.Customer_id = %s (customer_id,) and
                #               IP.PlanNo = IT.PlanNo
                #               IT.Agent_SSN = -- TODO This is going to need to be fixed, ot else I can't access agent's name
                cursor = con.cursor(dictionary=True)
                num = cursor.execute(
                    "SELECT IP.PlanNo, IP.Price, IP.Coverage, E.Name FROM Insurance_plan as IP, "
                    "insurance_transaction as IT, Customer as CA, employee as E WHERE IP.PlanNo = IT.PlanNo and "
                    "IT.Agent_SSN = E.SSN and CA.ID = IT.Customer_id and CA.Username = %s",
                    (request.json['Username'],))
                data = cursor.fetchall()
                cursor.close()
                return data
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# EP7
class EmployeeGetRentalStatuses(Resource):
    def get(self):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation != "user" and validation != 401:
                # SELECT *  -- Looks like the output is just the entire Rental table at the moment. Maybe we could reduce it to just Reg# and Status?
                #   FROM Rental
                cursor = con.cursor(dictionary=True)
                num = cursor.execute("SELECT RegNo, Status FROM Rental")
                data = cursor.fetchall()
                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# EP8
class EmployeeGetRentalStatus(Resource):
    def get(self, RegNo):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation != "user" and validation != 401:
                # SELECT *  -- Same as EP7, I think this just needs to return a status?
                #   FROM Rental
                #       WHERE Reg# = %s (RegNo,)
                cursor = con.cursor(dictionary=True)
                num = cursor.execute("SELECT RegNo, Status FROM Rental WHERE RegNo = %s", (RegNo,))
                data = cursor.fetchone()
                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# EP9
class EmployeeGetAllGarages(Resource):
    def get(self):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation != 'user' and validation != 401:
                # SELECT *  -- Pretty much the same as EP7, but I think this is fine as it is
                #   FROM Garage
                cursor = con.cursor(dictionary=True)
                num = cursor.execute("SELECT * FROM Garage")
                data = cursor.fetchall()
                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# EP10
class EmployeeGetAllShuttles(Resource):
    def get(self, garageNo):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation != "user" and validation != 401:
                # Capacities refer to the Shuttle capacities
                # SELECT GS.Shuttle#, G.City, G.Address, COUNT(GS.Shuttle#), G.Capacity -- Idk about this count, it's says current capacity and total capacity but I'm a bit confused with which is stored in Garage
                #   FROM Garage_Shuttle as GS, Garage as G
                #       WHERE GS.Garage# = G.Garage#
                cursor = con.cursor(dictionary=True)
                num = cursor.execute(
                    "SELECT G.GarageNo, G.City, G.Address, COUNT(GS.Shuttle_no) as Current_capacity, "
                    "G.Capacity as Total_capacity FROM Garage_Shuttle as GS, "
                    "Garage as G WHERE G.GarageNo = %s and GS.GarageNo = G.GarageNo", (garageNo,))
                data = cursor.fetchone()
                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# EP11
class EmployeeAddRental(Resource):
    def post(self):
        try:
            new_rental = request.json

            # Checks the employee's input
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation != 'user' and validation != 401:
                # It seems there's a constraint with the city and address of the rental, where they need to exist at a location
                # So just need to check that
                # SELECT City, Address
                #   FROM Location
                #       WHERE City = '%s' and Address = '%s' (new_rental['City'],new_rental['Address'])
                cursor = con.cursor(dictionary=True)
                cursor.execute("SELECT City, Address FROM Location WHERE City = %s and Address = %s",
                               (new_rental['City'], new_rental['Address']))
                check = cursor.fetchall()

                if check:
                    # INSERT INTO RENTAL (Color, Status, Make, Model, City, Address)
                    #   VALUES (%s, %s, %s, %s, %s, %s) (you get the idea, this is new_rental's keys)
                    # Defined the tuple here to ensure the line wasn't too long
                    atts = (new_rental['Color'], new_rental['Status'], new_rental['Make'], new_rental['Model'],
                            new_rental['Price'], new_rental['City'], new_rental['Address'])
                    cursor.execute(
                        "INSERT INTO RENTAL (Color, Status, Make, Model, Price, City, Address) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        atts)
                    con.commit()
                    cursor.close()  # Not sure if this needs to be closed after a commit, but adding just in case
                    return "Rental added"
                else:
                    cursor.close()
                    return "Location is not valid.", 400
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# EP12
class EmployeeUpdateRentalStatus(Resource):
    def put(self, RegNo):
        try:
            updated_rental = request.json

            # Checks the employee's input
            validation = validate_user(request.json['Username'], request.json['Password'])
            if validation != 'user' and validation != 401:
                # UPDATE Rental
                #   SET Status='%s'
                #       WHERE Reg#=%s
                cursor = con.cursor()
                num = cursor.execute("UPDATE rental SET Status = %s WHERE RegNo = %s",
                                     (updated_rental['Status'], RegNo))
                con.commit()
                cursor.close()
                return f"Rental status updated at {RegNo}"
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# EP13
class EmployeeGetCustomerRental(Resource):
    def get(self, username):
        # try:
        # Checks the employee's input
        validation = validate_user(request.json['Username'], request.json['Password'])
        print(username)
        if validation != 'user' and validation != 401:
            # SELECT R.Reg#, R.Make, R.Model, R.Color, R.City, R.Address, R.Status
            #   FROM Rental as R, Rents as C
            #       WHERE   C.Customer_id='%s' and
            #               C.Reg# = R.Reg# (customer_id,)
            cursor = con.cursor(dictionary=True)
            num = cursor.execute(
                "SELECT R.RegNo, R.Make, R.Model, R.Color, R.City, R.Address, R.Status "
                "FROM Rental as R, Rents as C, Customer as CA"
                " WHERE CA.Username = %s and C.Customer_id = CA.ID and C.RegNo = R.RegNo", (username,))
            data = cursor.fetchall()
            cursor.close()
            return data
        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401
    #  except:
    #     return 'Invalid input', 400


# EP14
class EmployeeGetHours(Resource):
    def get(self):
        try:
            # Checks the employee's input
            validation = validate_user(request.json['Username'], request.json['Password'])
            if validation != 'user' and validation != 401:
                # SELECT E.Hours
                #   FROM Employee as E, Account as A    -- Going to assume that the account username is accessable
                #       WHERE E.Username = A.Username and
                #               E.SSN = ''-- I'm not sure how to get this data just yet
                cursor = con.cursor(dictionary=True)
                num = cursor.execute("SELECT Hours FROM employee WHERE Username = %s",
                                     (request.json['Username'],))
                data = cursor.fetchone()
                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 15
class AgentGetInsurancePlans(Resource):
    def get(self):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])
            if validation == 'agent' or validation == 'manager' and validation != 401:
                # SELECT IP.Plan#, IP.Price, IP.Coverage
                # FROM Insurance_Plan as IP
                cursor = con.cursor(dictionary=True)
                num = cursor.execute(
                    "SELECT IP.PlanNo, IP.Price, IP.Coverage FROM Insurance_Plan as IP")
                data = cursor.fetchall()
                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 16
class AgentGetActiveInsurancePlans(Resource):
    def get(self, clientID):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation == 'agent' or validation == 'manager' and validation != 401:
                # SELECT IP.Plan#, IP.Price, IP.Coverage
                # FROM Insurance_Plan as IP, Customer_Account as CA
                # WHERE IP.Plan# = IT.Plan# and IT.Customer_id = CA.Customer_id and CA.Customer_id = %s
                cursor = con.cursor(dictionary=True)
                num = cursor.execute(
                    "SELECT IP.PlanNo, IP.Price, IP.Coverage"
                    " FROM Insurance_Plan as IP, Insurance_Transaction as IT, Customer as C"
                    " WHERE IP.PlanNo = IT.PlanNo and IT.Customer_id = C.ID and C.ID = %s", (int(clientID),))
                data = cursor.fetchall()
                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 18
class AgentReturnRental(Resource):
    def post(self):
      try:
        validation = validate_user(request.json['Username'], request.json['Password'])

        if validation == 'agent' or validation == 'manager':
            # SELECT City, Address
            #   FROM Location
            #       WHERE City = '%s' and Address = '%s' (new_rental['City'],new_rental['Address'])
            cursor = con.cursor(dictionary=True)
            cursor.execute("SELECT City, Address FROM Location WHERE City = %s and Address = %s",
                           (request.json['City'], request.json['Address']))
            check = cursor.fetchall()

            if check:
                cursor = con.cursor(dictionary=True)
                today = date.today()
                today_format = today.strftime('%Y-%m-%d')
                time = datetime.now().time()
                time_format = time.strftime('%H:%M:%S')

                num = cursor.execute(
                    "INSERT INTO rental_return "
                    "(Customer_id, RegNo, City, Address, Date, Time) "
                    "VALUES (%s,%s,%s,%s,%s,%s)", (request.json["Customer_id"],
                                                   request.json['RegNo'], request.json['City'],
                                                   request.json['Address'], today_format, time_format))
                con.commit()

                cursor.execute("UPDATE rental SET Status = 'available', City = %s, Address = %s "
                               "WHERE RegNo = %s", (request.json['City'], request.json['Address'], request.json['RegNo']))
                con.commit()

                cursor.close()
                return "Rental successfully returned", 200
            else:
                return "Invalid Location", 400

        elif validation == 401:
            return "Invalid login credentials", 401
        else:
            return 'Unauthorized User', 401
      except:
        return 'Invalid input', 400


# Endpoint 19
class MechanicGetWorks(Resource):
    def get(self):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation == 'mechanic':
                # SELECT WI.City, WI.Address, WI.Garage#, WI.Hours
                # FROM Mechanic as M, Works_in as WI
                # WHERE M.Mechanic_SSN = WI.Mechanic_SSN and Mechanic_SSN = %s
                cursor = con.cursor(dictionary=True)
                num = cursor.execute(
                    "SELECT WI.City, WI.Address, WI.GarageNo, WI.Hours "
                    "FROM Mechanic as M, Works_in as WI, Employee as E"
                    " WHERE M.Mechanic_SSN = WI.Mechanic_SSN and "
                    "M.Mechanic_SSN = E.SSN and E.Username = %s", (request.json['Username'],))
                data = cursor.fetchall()
                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 20
class MechanicGetAllServices(Resource):
    def get(self):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation == 'mechanic' or validation == 'manager':
                # SELECT RS.Reg#, RS.Date, RS.Hours
                # FROM Rental_Service as RS
                cursor = con.cursor(dictionary=True)
                num = cursor.execute(
                    "SELECT RS.RegNo, RS.Date, RS.Hours FROM Rental_Service as RS")
                data = cursor.fetchall()

                # convert datetime objects to string
                for d in data:
                    d['Date'] = d['Date'].strftime('%Y-%m-%d')

                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 21
class MechanicGetAllRegNoServices(Resource):
    def get(self, RegNo):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation == 'mechanic' or validation == 'manager':
                # SELECT RS.Reg#, RS.Date, RS.Hours
                # FROM Rental_Service as RS, Rental as R
                # WHERE RS.Reg# = %s (RegNo)
                cursor = con.cursor(dictionary=True)
                num = cursor.execute(
                    "SELECT RS.RegNo, RS.Date, RS.Hours "
                    "FROM Rental_Service as RS, Rental as R "
                    "WHERE RS.RegNo = %s and RS.RegNo = R.RegNo", (RegNo,))
                data = cursor.fetchall()

                # convert date time objects to strings
                for d in data:
                    d['Date'] = d['Date'].strftime('%Y-%m-%d')

                cursor.close()
                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 22
class MechanicGetAllShuttleServices(Resource):
    def get(self):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation == 'mechanic' or validation == 'manager':
                # SELECT SServ.Shuttle#, SServ.Date, SServ.Hours
                # FROM Shuttle_Service as Sserv
                cursor = con.cursor(dictionary=True)
                num = cursor.execute(
                    "SELECT SServ.ShuttleNo, SServ.Date, SServ.Hours FROM Shuttle_Service as SServ")
                data = cursor.fetchall()
                cursor.close()

                # convert date time objects to strings
                for d in data:
                    d['Date'] = d['Date'].strftime('%Y-%m-%d')

                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 23
class MechanicAddShuttle(Resource):
    def post(self):
        try:
            new_shuttle = request.json

            # Checks the employee's input
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation == 'mechanic' or validation == 'manager':
                cursor = con.cursor(dictionary=True)
                cursor.execute("SELECT City, Address FROM Location WHERE City = %s and Address = %s",
                               (new_shuttle['City'], new_shuttle['Address']))
                check1 = cursor.fetchall()

                cursor.execute("SELECT GarageNo FROM garage WHERE City = %s and Address = %s and GarageNo = %s",
                               (new_shuttle['City'], new_shuttle['Address'], new_shuttle['GarageNo']))
                check2 = cursor.fetchall()

                if check1 and check2:
                    atts = (new_shuttle["Capacity"],)
                    cursor.execute(
                        "INSERT INTO shuttle (Capacity) VALUES (%s)",
                        atts)
                    con.commit()

                    cursor.execute("SELECT last_insert_id() as ShuttleNo")
                    shuttle_no = cursor.fetchone()

                    atts = (shuttle_no['ShuttleNo'], new_shuttle['City'],
                            new_shuttle['Address'], new_shuttle['GarageNo'])
                    cursor.execute(
                        "INSERT INTO garage_shuttle (Shuttle_no, City, Address, GarageNo) "
                        "VALUES (%s,%s,%s,%s)",
                        atts)
                    con.commit()
                    cursor.close()
                    return shuttle_no
                else:
                    cursor.close()
                    return "Location and/or garage number is not valid.", 400
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 24
class MechanicUpdateShuttle(Resource):
    def put(self, shuttleNo):
        try:
            updated_shuttle = request.json

            # check input
            validation = validate_user(request.json['Username'], request.json['Password'])
            if validation == 'mechanic' or validation == 'manager':
                # UPDATE Shuttle
                #   SET Airport_name='%s', Schedule='%s'
                #       WHERE Shuttle#=%s
                cursor = con.cursor()

                cursor.execute("SELECT * FROM Airport WHERE Name = %s",
                               (updated_shuttle['Airport'],))
                check = cursor.fetchall()

                if check:
                    num = cursor.execute("UPDATE Shuttle SET Airport_name=%s, Schedule=%s WHERE Number=%s",
                                     (updated_shuttle['Airport'], updated_shuttle['Schedule'], shuttleNo))
                    con.commit()
                    cursor.close()
                    return f"Shuttle Airport, Schedule updated at Shuttle #{shuttleNo}"
                else:
                    return "Airport does not exist.", 400
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 25
class MechanicGetAllShuttleNoServices(Resource):
    def get(self, shuttleNo):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation == 'mechanic' or validation == 'manager':
                # SELECT SServ.Shuttle#, SServ.Date, SServ.Hours
                # FROM Shuttle_Service as Sserv, Shuttle as S
                # WHERE SServ.Shuttle# = %s and SServ.Shuttle# = S.Shuttle#
                cursor = con.cursor(dictionary=True)
                num = cursor.execute(
                    "SELECT SServ.ShuttleNo, SServ.Date, SServ.Hours "
                    "FROM Shuttle_Service as Sserv "
                    "WHERE SServ.ShuttleNo = %s", (shuttleNo,))
                data = cursor.fetchall()
                cursor.close()

                # converting date objects to strings
                for d in data:
                    d['Date'] = d['Date'].strftime('%Y-%m-%d')

                return data
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 26
class ManagerFireEmployee(Resource):
    def delete(self):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation == 'manager':
                #DELETE FROM Employee as E
                #WHERE E.SSN = %s
                cursor = con.cursor(dictionary=True)
                cursor.execute("DELETE FROM Employee as E WHERE E.SSN = %s", (request.json['SSN'],))
                con.commit()
                cursor.close()
                return {"SSN": int(request.json['SSN'])}, 200
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# Endpoint 27
class ManagerRemoveRental(Resource):
    def delete(self, RegNo):
        try:
            validation = validate_user(request.json['Username'], request.json['Password'])

            if validation == 'manager' and validation != 401:
                #DELETE FROM Rental as R
                #WHERE R.RegNo = %s
                cursor = con.cursor(dictionary=True)
                cursor.execute("DELETE FROM Rental as R WHERE R.RegNo = %s", (RegNo,))
                con.commit()
                cursor.close()
                return {"RegNo": RegNo}
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except mysql.connector.errors.IntegrityError:
            return "Violates key constraint, someone may be renting that rental.", 400
        except:
            return 'Invalid input', 400


# Endpoint 28
class ManagerHireEmployee(Resource):
    def post(self):
        try:
            new_employee = request.json
            validation = validate_user(request.json['Manager_username'], request.json['Manager_password'])

            if validation == 'manager':
                cursor = con.cursor(dictionary=True)
                cursor.execute("SELECT * FROM location WHERE City = %s and Address = %s",
                               (new_employee['City'], new_employee['Address']))
                check = cursor.fetchall()

                if check:
                    args = (new_employee['Employee_SSN'], new_employee['Name'], new_employee['DOB'], new_employee['Sex'],
                            new_employee['Salary'], new_employee['Employee_username'], new_employee['City'], new_employee['Address'])
                    cursor.execute("INSERT INTO employee (SSN, Name, DOB, Sex, Salary, Username, City, Address) "
                                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", args)
                    con.commit()
                    cursor.close()
                    return {"SSN": new_employee['Employee_SSN']}, 200
                else:
                    "No location with that city and address.", 400
            elif validation == 401:
                return "Invalid login credentials", 401
            else:
                return 'Unauthorized User', 401
        except:
            return 'Invalid input', 400


# adding each resource as an endpoint
api.add_resource(AvailableRentals, "/api/rentals")
api.add_resource(AvailableRentalCar, "/api/rentals/<int:RegNo>")
api.add_resource(AvailableRentalsCity, "/api/<city>/rentals")
api.add_resource(NewUser, "/api/users")
api.add_resource(ClientRentHistory, "/api/user/rentals")
api.add_resource(ClientInsurancePlans, "/api/user/plans")
api.add_resource(EmployeeGetRentalStatuses, "/api/rentals_status")
api.add_resource(EmployeeGetRentalStatus, "/api/rentals_status/<int:RegNo>")
api.add_resource(EmployeeGetAllGarages, "/api/garages")
api.add_resource(EmployeeGetAllShuttles, "/api/garages/<int:garageNo>")
api.add_resource(EmployeeAddRental, "/api/rentals")
api.add_resource(EmployeeUpdateRentalStatus, "/api/rentals/<int:RegNo>")
api.add_resource(EmployeeGetCustomerRental, "/api/rentals/<string:username>")
api.add_resource(EmployeeGetHours, "/api/employee/hours")
api.add_resource(AgentGetInsurancePlans, "/api/insuranceplans")
api.add_resource(AgentGetActiveInsurancePlans, "/api/<int:clientID>/insuranceplans")
api.add_resource(MechanicGetWorks, "/api/mechanic/work")
api.add_resource(MechanicGetAllServices, "/api/rentalservices")
api.add_resource(MechanicGetAllRegNoServices, "/api/rentalservices/<int:RegNo>")
api.add_resource(MechanicGetAllShuttleServices, "/api/shuttleservices")
api.add_resource(MechanicUpdateShuttle, "/api/shuttles/<int:shuttleNo>")
api.add_resource(MechanicGetAllShuttleNoServices, "/api/shuttleservices/<int:shuttleNo>")
api.add_resource(AgentReturnRental, "/api/rentalreturn")
api.add_resource(MechanicAddShuttle, "/api/shuttles")
api.add_resource(ManagerFireEmployee, "/api/employees")
api.add_resource(ManagerRemoveRental, "/api/rentals/<int:RegNo>")
api.add_resource(ManagerHireEmployee, "/api/employees")

@app.route('/')
@app.route('/api')
def root():
    return "<h1>API Page Version 0.1</h1>"


if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=5001)
