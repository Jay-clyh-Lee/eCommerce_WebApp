from ..config.mysqlconnection import connectToMySQL
from flask import flash

class Order:

    def __init__(self, data) -> None:
        self.name = data["name"]
        self.returnable = data["returnable"]
        self.user_id = data["user_id"]
        self.purchased_date = data["purchased_date"]