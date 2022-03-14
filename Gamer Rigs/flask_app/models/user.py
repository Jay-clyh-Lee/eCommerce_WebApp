from ..config.mysqlconnection import connectToMySQL
from flask import flash
from ..models import order

import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')
ADDRESS_REGEX = re.compile(r'^[0-9]+ [a-zA-Z]')

class User:
    db = "eCommerce"

    def __init__(self, db_data):
        self.id = db_data['id']
        # self.title = db_data['title']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.birthday = db_data['birthday']
        self.address = db_data['address']
        # self.shipping_address = db_data['shipping_address']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.orders = []

    @classmethod
    def create_user(cls, form_data):
        query = "INSERT INTO users (first_name, last_name, email, password, birthday, address) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(birthday)s, %(address)s);"
        return connectToMySQL(cls.db).query_db(query,form_data)
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users LEFT JOIN orders ON orders.user_id = users.id LEFT JOIN products ON products.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query) 
        users = []
        for u in results:
            users.append(cls(u))
        return users

    @classmethod
    def get_by_email(cls,form_data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,form_data)
        if len(results) == 0:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,form_data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,form_data)
        if len(results) == 0:
            return False
        return cls(results[0])

    @classmethod
    def update_user(cls, form_data):
        query = "UDPATE users SET title=%(title)s, first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, title=%(title)s, password=%(password)s, birthday=%(birthday)s, address=%(address)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def delete_user(cls, form_data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        # for names
        if len(form_data['first_name']) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid=False
        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid=False
        # for email
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid Email!", "register")
            is_valid=False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, form_data)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid=False
        # for passwords
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters long", "register")
            is_valid=False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords don't match.", "register")
            is_valid=False
        return is_valid
    
    @staticmethod
    def validate_login(form_data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, form_data)
        if len(results) == 0:
            flash("Email does not exist.", "login")
            is_valid=False
        if len(form_data['email']) == 0:
            flash("Email field cannot be empty", "login")
            is_valid=False
        if len(form_data['password']) == 0:
            flash("Password field cannot be empty", "login")
            is_valid=False
        return is_valid