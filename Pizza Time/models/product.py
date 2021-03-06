from config.mysqlconnection import connectToMySQL
from flask import flash
from models import user

class Product:
    db = "pizza_time"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.method = db_data['method']
        self.size = db_data['size']
        self.crust = db_data['crust']
        self.toppings = db_data['toppings'] #list
        self.favorite = db_data['favorite'] #boolean
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def create_product(cls, form_data):
        # this would be for admin use in eCom app and not applied the same way as here
        query = "INSERT INTO products (method, size, crust, toppings, favorite) VALUES (%(method)s, %(size)s, %(crust)s, %(toppings)s, %(favorite)s);"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_product_by_id(cls, form_data):
        query = "SELECT * FROM products WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def update_product(cls, form_data):
        # na
        query = "UPDATE products SET name=%(name)s, description=%(description)s, price=%(price)s, quantity=%(quantity)s, user_id=%(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def destroy_product(cls, form_data):
        # na
        query = "DELETE FROM products WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_user_orders(cls, form_data):
        # na
        query = "SELECT * FROM users LEFT JOIN orders ON users.id = orders.user_id LEFT JOIN products ON orders.product_id = products.id  WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)
        user_orders = []
        for row in results:
            user_orders.append(cls(row))
        return user_orders

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM products LEFT JOIN users ON users.id = products.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        all_products = []
        for row in results:
            this_product = cls(row)
            user_form_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'address': row['address'],
                'city': row['city'],
                'state': row['state'],
                'cart': row['cart'],
            }
            # create a user instance for this creator
            this_user = user.User(user_form_data)
            this_product.user = this_user
            all_products.append(this_product)
        return all_products

    @classmethod
    def get_all_detailed(cls):
        query = "SELECT * FROM products LEFT JOIN users ON users.id = products.user_id LEFT JOIN products ON products.id = products.product_id LEFT JOIN users AS buyers ON buyers.id = products.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        all_products = []
        for row in results:
            this_product = cls(row)
            buyer_form_data = { 
                'id': row['buyers.id'],
                'first_name': row['buyers.first_name'],
                'last_name': row['buyers.last_name'],
                'email': row['buyers.email'],  
                'password': row['buyers.password'],
                'created_at': row['buyers.created_at'],
                'updated_at': row['buyers.updated_at'],
            }
            user_form_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'address': row['address'],
                'city': row['city'],
                'state': row['state'],
                'cart': row['cart'],
            }
            this_user = user.User(user_form_data)
            this_product.user = this_user
            this_buyer = user.User(buyer_form_data)
            this_product.buyers.append(this_buyer)
                
            all_products.append(this_product)
        return all_products

    @classmethod
    def get_by_id(cls, form_data):
        query = "SELECT DISTINCT * FROM products LEFT JOIN users ON users.id = products.user_id LEFT JOIN products ON products.id = products.product_id LEFT JOIN users AS buyers ON buyers.id = products.user_id WHERE products.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)    
        this_product = cls(results[0])
        artist_form_data = { 
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at'],
        }
        this_product.user = user.User(artist_form_data)
        for row in results:
            buyer_form_data = { 
                'id': row['buyers.id'],
                'first_name': row['buyers.first_name'],
                'last_name': row['buyers.last_name'],
                'email': row['buyers.email'],  
                'password': row['buyers.password'],
                'created_at': row['buyers.created_at'],
                'updated_at': row['buyers.updated_at'],
            }
            this_product.buyers.append(buyer_form_data)
        return this_product

    @classmethod
    def buy_product(cls, form_data):
        query = "INSERT INTO products (product_id, user_id) VALUES (%(product_id)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_my_purchased_products(cls, form_data):
        purchased_products = []
        query = "SELECT * FROM users JOIN products ON products.user_id = users.id JOIN products ON products.product_id = products.id WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)
        if len(results) < 1:
            return False 
        for row in results:
            purchased_products.append(cls(row))
        return purchased_products

    @staticmethod
    def validate_product(form_data):
        is_valid = True
        if len(form_data["method"]) == 0:
            flash("Choose an option", "product")
            is_valid=False
        if len(form_data["size"]) == 0:
            flash("Choose an option", "product")
            is_valid=False
        if len(form_data["crust"]) == 0:
            flash("Choose an option", "product")
            is_valid=False
        if len(form_data["toppings"]) < 1 or len(form_data["toppings"]) > 5:
            flash("Toppings cannot be empty or exceed 5", "product")
            is_valid=False
        return is_valid