from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Admin:

    db = "eCommerce"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.admin_tier = data['admin_tier']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO admins (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM admins LEFT JOIN trees ON trees.user_id = id;"
        results = connectToMySQL(cls.db).query_db(query) 
        admins = []
        for u in results:
            admins.append(cls(u))
        return admins

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM admins WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) == 0:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM admins WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) == 0:
            return False
        return cls(results[0])


    @staticmethod
    def validate_registration(data):
        is_valid = True
        # for names
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid=False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid=False
        # for email
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!", "register")
            is_valid=False
        query = "SELECT * FROM admins WHERE email = %(email)s;"
        results = connectToMySQL(Admin.db).query_db(query, data)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid=False
        # for passwords
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long", "register")
            is_valid=False
        if data['password'] != data['confirm_password']:
            flash("Passwords don't match.", "register")
            is_valid=False
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        query = "SELECT * FROM admins WHERE email = %(email)s;"
        results = connectToMySQL(Admin.db).query_db(query, data)
        if len(results) == 0:
            flash("Email does not exist.", "login")
            is_valid=False
        if len(data['email']) == 0:
            flash("Email field cannot be empty", "login")
            is_valid=False
        if len(data['password']) == 0:
            flash("Password field cannot be empty", "login")
            is_valid=False
        return is_valid