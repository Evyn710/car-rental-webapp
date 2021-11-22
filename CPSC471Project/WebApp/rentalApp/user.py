from flask_login import UserMixin
from rentalApp import con


class User(UserMixin):
    def __init__(self, username, password):
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