from flask_login import UserMixin
from rentalApp import con, bcrypt


class User(UserMixin):
    def __init__(self, username, password):
        self.usertype = validate_user(username, password)
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

    @staticmethod
    def get(username):
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT Username, Password FROM account WHERE Username = %s", (username,))
        data = cursor.fetchone()
        cursor.close()
        if data:
            return User(data["Username"], data["Password"])

        return None;


# helper function to return what kind of user the user is
def validate_user(username, password):
    cursor = con.cursor(dictionary=True)

    # find out if they are a user
    cursor.execute("SELECT Username, Password FROM account WHERE Username = %s", (username,))
    user = cursor.fetchone()
    if user and user['Password'] == password:
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
            SSN = cursor.fetchone()
            cursor.execute("SELECT * FROM employee as e WHERE e.Mgr_ssn = %s", (SSN,))
            manages = cursor.fetchone()
            if manages:
                return "manager"

            return "employee"
        else:
            return "user"
    else:
        return 401