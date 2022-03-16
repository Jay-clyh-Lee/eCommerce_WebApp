from config.mysqlconnection import connectToMySQL
from flask import flash
from models import user

class Painting:
    db = "pizza_time"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.method = db_data['method']
        self.size = db_data['size']
        self.crust = db_data['crust']
        self.toppings = db_data['toppings']
        self.price = db_data['price']
        self.quantity = db_data['quantity']
        self.date_of_purchase = db_data['date_of_purchase']
        self.favorite = db_data['favorite']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.user = None
        self.buyers = []


    @classmethod
    def create_painting(cls, form_data):
        query = "INSERT INTO paintings (method, size, crust, toppings, price, quantity, date_of_purchase, favorite, user_id) VALUES (%(method)s, %(size)s, %(crust)s, %(toppings)s, %(price)s,%(quantity)s,%(date_of_purchase)s, %(favorite)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_painting_by_id(cls, form_data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,form_data)
        
    @classmethod
    def get_my_paintings(cls, form_data):
        query = "SELECT * FROM paintings LEFT JOIN users ON users.id = paintings.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,form_data)
        my_paintings = []
        for row in results:
            my_paintings.append(cls(row))
        return my_paintings

    @classmethod
    def update_painting(cls,form_data):
        query = "UPDATE paintings SET name=%(name)s, description=%(description)s, price=%(price)s, quantity=%(quantity)s, user_id=%(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,form_data)

    @classmethod
    def destroy_painting(cls,form_data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,form_data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings LEFT JOIN users ON users.id = paintings.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        all_paintings = []
        for row in results:
            this_painting = cls(row)
            user_form_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],  
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
                # create a user instance for this creator
            this_user = user.User(user_form_data)
            this_painting.user = this_user
            all_paintings.append(this_painting)
        return all_paintings

    @classmethod
    def get_all_detailed(cls):
        query = "SELECT * FROM paintings LEFT JOIN users ON users.id = paintings.user_id LEFT JOIN purchases ON paintings.id = purchases.painting_id LEFT JOIN users AS buyers ON buyers.id = purchases.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        all_paintings = []
        for row in results:
            this_painting = cls(row)
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
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            this_user = user.User(user_form_data)
            this_painting.user = this_user
            this_buyer = user.User(buyer_form_data)
            this_painting.buyers.append(this_buyer)
            # if row['buyers.id'] is not None:
                
            all_paintings.append(this_painting)
        return all_paintings

    @classmethod
    def get_by_id(cls, form_data):
        query = "SELECT DISTINCT * FROM paintings LEFT JOIN users ON users.id = paintings.user_id LEFT JOIN purchases ON paintings.id = purchases.painting_id LEFT JOIN users AS buyers ON buyers.id = purchases.user_id WHERE paintings.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)    
        this_painting = cls(results[0])
        artist_form_data = { 
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at'],
        }
        this_painting.user = user.User(artist_form_data)
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
            this_painting.buyers.append(buyer_form_data)
        return this_painting

    @classmethod
    def buy_painting(cls, form_data):
        query = "INSERT INTO purchases (painting_id, user_id) VALUES (%(painting_id)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_my_purchased_paintings(cls, form_data):
        purchased_paintings = []
        query = "SELECT * FROM users JOIN purchases ON purchases.user_id = users.id JOIN paintings ON purchases.painting_id = paintings.id WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)
        if len(results) < 1:
            return False 
        for row in results:
            purchased_paintings.append(cls(row))
        return purchased_paintings


    @staticmethod
    def validate_painting(form_data):
        is_valid = True
        if len(form_data["name"]) < 2:
            flash("Title should be at least 2 characters long.", "painting")
            is_valid=False
        if len(form_data["description"]) < 10:
            flash("Descriptoin should be at least 10 characters long.", "painting")
            is_valid=False
        if len(form_data["price"]) == 0 or float(form_data["price"]) <= 0:
            flash("Price should be greater than 0.", "painting")
            is_valid=False
        if len(form_data["quantity"]) == 0 or int(form_data["quantity"]) < 1:
            flash("Quantity should be greater than 0.", "painting")
            is_valid=False
        return is_valid