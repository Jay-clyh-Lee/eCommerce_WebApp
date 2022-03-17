from config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
states = []

class User:
    db = "pizza_time"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.address = db_data['address']
        self.city = db_data['city']
        self.state = db_data['state']
        self.cart = db_data['cart'] #init empty
        self.fave = db_data['fave'] #init empty

        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.orders = []

    @classmethod
    def create_user(cls, form_data):
        query = "INSERT INTO users (first_name, last_name, email, password, address, city, state) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(address)s, %(city)s, %(state)s);"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users LEFT JOIN orders ON orders.user_id = users.id;"
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
    def add_to_cart():
        query = "UPDATE users VALUE () WHERE id = %(id)s;"
        return 
    
    @classmethod
    def check_out():
        query = ";"
        return "UPDATE users SET orders = %(order)s WHERE id = %(id)s;"

    @classmethod
    def get_orders_by_user_id(cls,form_data):
        query = "SELECT * FROM users JOIN orders ON orders.user_id = users.id WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query,form_data)
        for row in results:
            this_user = cls(row)
            order_form_data = {
                "method" : row['method'],
                "size" : row['size'],
                "crust": row["crust"],
                "toppings": row["toppings"],
                "quantity": row["quantity"],
                "favorite": row["favorite"],
            }
            order_form_data = {
                "id": row["orders.id"],
                'name': row['name'],
                'description': row['description'],
                'price': row['price'],  
                'quantity': row['quantity'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            this_user.orderd_orders.append(order_form_data)
        if len(results) == 0:
            return False
        return cls(results[0])
    
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
        # address, city, state

        # city.  USE API to validate address and city
        if len(form_data['city']) < 1:
            flash("City cannot be empty", "register")
            is_valid=False
        if len(form_data['city']) > 17:
            flash("City name must be valid", "register")
            is_valid=False
        if len(form_data['state']) == 0:
            flash("State cannot be empty", "register")
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

    @staticmethod
    def validate_update(form_data):
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
        # address, city, state
        # city.  USE API to validate address and city
        if len(form_data['city']) < 1:
            flash("City cannot be empty", "register")
            is_valid=False
        if len(form_data['city']) > 17:
            flash("City name must be valid", "register")
            is_valid=False
        if len(form_data['state']) == 0:
            flash("State cannot be empty", "register")
            is_valid=False
        # for passwords
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters long", "register")
            is_valid=False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords don't match.", "register")
            is_valid=False
        return is_valid