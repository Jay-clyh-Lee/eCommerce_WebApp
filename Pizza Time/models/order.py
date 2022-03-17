from config.mysqlconnection import connectToMySQL
from flask import flash
from models import user

class Order:
    db = "pizza_time"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.method = db_data['method']
        self.size = db_data['size']
        self.crust = db_data['crust']
        self.toppings = db_data['toppings'] #list
        self.price = db_data['price'] #float    d
        self.quantity = db_data['quantity'] #int
        self.favorite = db_data['favorite'] #boolean
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']

    def single_item_price(self, *items):
        self.price = 0
        price_tags = {"pick_up": 0, "delivery": 5, "large": 12, "medium": 8, "small": 5, "pepperoni": 3, "sausage": 3.5, "steak": 5, "pineapple": 4, "chicken": 4.5, "veggies": 4, "extra_cheese": 3, "extra_meat": 5, "regular": 0, "thin": 2, "stuffed": 5}
        for item in items:
            self.price += price_tags[item]
        return self.price

    def apply_tax(self, tax_rate):
        tax_rate /= 100
        self.price = self.price * (1 + tax_rate) 
        return self.price

    def calculate_final_price(self, quantity):
        self.price = self.price * quantity
        return self.price

    @classmethod
    def create_order(cls, form_data):
        query = "INSERT INTO orders (method, size, crust, toppings, price, quantity, favorite, user_id) VALUES (%(method)s, %(size)s, %(crust)s, %(toppings)s, %(price)s ,%(quantity)s, %(favorite)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_order_by_id(cls, form_data):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def update_order(cls, form_data):
        query = "UPDATE orders SET name=%(name)s, description=%(description)s, price=%(price)s, quantity=%(quantity)s, user_id=%(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def destroy_order(cls, form_data):
        query = "DELETE FROM orders WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_user_orders(cls, form_data):
        query = "SELECT * FROM orders LEFT JOIN users ON users.id = orders.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)
        user_orders = []
        for row in results:
            user_orders.append(cls(row))
        return user_orders

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders LEFT JOIN users ON users.id = orders.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        all_orders = []
        for row in results:
            this_order = cls(row)
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
            this_order.user = this_user
            all_orders.append(this_order)
        return all_orders

    @classmethod
    def get_all_detailed(cls):
        query = "SELECT * FROM orders LEFT JOIN users ON users.id = orders.user_id LEFT JOIN orders ON orders.id = orders.order_id LEFT JOIN users AS buyers ON buyers.id = orders.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        all_orders = []
        for row in results:
            this_order = cls(row)
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
            this_order.user = this_user
            this_buyer = user.User(buyer_form_data)
            this_order.buyers.append(this_buyer)
            # if row['buyers.id'] is not None:
                
            all_orders.append(this_order)
        return all_orders

    @classmethod
    def get_by_id(cls, form_data):
        query = "SELECT DISTINCT * FROM orders LEFT JOIN users ON users.id = orders.user_id LEFT JOIN orders ON orders.id = orders.order_id LEFT JOIN users AS buyers ON buyers.id = orders.user_id WHERE orders.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)    
        this_order = cls(results[0])
        artist_form_data = { 
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at'],
        }
        this_order.user = user.User(artist_form_data)
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
            this_order.buyers.append(buyer_form_data)
        return this_order

    @classmethod
    def buy_order(cls, form_data):
        query = "INSERT INTO orders (order_id, user_id) VALUES (%(order_id)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_my_purchased_orders(cls, form_data):
        purchased_orders = []
        query = "SELECT * FROM users JOIN orders ON orders.user_id = users.id JOIN orders ON orders.order_id = orders.id WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)
        if len(results) < 1:
            return False 
        for row in results:
            purchased_orders.append(cls(row))
        return purchased_orders

    @staticmethod
    def validate_order(form_data):
        is_valid = True
        if len(form_data["method"]) == 0:
            flash("Choose an option", "order")
            is_valid=False
        if len(form_data["size"]) == 0:
            flash("Choose an option", "order")
            is_valid=False
        if len(form_data["crust"]) == 0:
            flash("Choose an option", "order")
            is_valid=False
        if len(form_data["toppings"]) < 1 or len(form_data["toppings"]) > 5:
            flash("Toppings cannot be empty or exceed 5", "order")
            is_valid=False
        if len(form_data["quantity"]) == 0 or int(form_data["quantity"]) < 1:
            flash("Quantity should be greater than 0.", "order")
            is_valid=False
        return is_valid