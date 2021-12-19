from ..config.mysqlconnection import connectToMySQL
from flask import flash

class Order:

    def __init__(self, data) -> None:
        self.id = data["id"]
        self.order_price = data["order_price"]
        self.date_order_placed = data["date_order_placed"]
        self.billing_address = data["billing_address"]
        self.shipping_address = data["shipping_address"]
        self.cancelled = data["cancelled"]
        self.date_cancelled = data["date_cancelled"]
        self.returned = data["returned"]
        self.date_returned = data["date_returned"]
        self.user_id = data["user_id"]
        self.product_id = data["product_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.items = []
        self.user = None

    @classmethod
    def create_order(cls, form_data):
        query = "INSERT INTO products (name, order_price, date_order_placed, billing_address, shipping_address, category_id VALUES (%(name)s, %(price)s, %(in_stock)s, %(user_id)s, %(category_id)s);"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def cancel_order(cls, form_data):
        query = "DELETE FROM orders WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)