from ..config.mysqlconnection import connectToMySQL
from flask import flash
from ..models import user, admin

class Product:
    db = "eCommerce"

    def __init__(self, db_data) -> None:
        self.id = db_data["id"]
        self.name = db_data["name"]
        self.price = db_data["price"]
        self.in_stock = db_data["in_stock"]
        self.user_id = db_data["user_id"]
        self.category_id = db_data["category_id"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]

    @classmethod
    def get_all_by_category(cls, category):
        query = f"SELECT * FROM products WHERE category = {category};"
        results = connectToMySQL(cls.db).query_db(query)
        products_in_this_category = []
        for row in results:
            products_in_this_category.append(cls(row))
        return products_in_this_category

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM products;"
        results = connectToMySQL(cls.db).query_db(query)
        products = []
        for row in results:
            products.append(cls(row))
        return products

    @classmethod
    def get_by_id(cls, form_data):
        query = "SELECT * FROM products WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def get_all_by_user(cls, form_data):
        # get all products purchased by this user
        query = "SELECT * FROM products LEFT JOIN users ON products.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)
        user_purchases = []
        for row in results:
            user_purchases.append(cls(row))
        return user_purchases 

    @classmethod
    def get_all_by_product(cls, form_data):
        # get all users who bought this product
        query = "SELECT * FROM users LEFT JOIN products ON products.user_id = users.id WHERE product.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, form_data)
        user_purchases = []
        for row in results:
            user_purchases.append(cls(row))
        return user_purchases