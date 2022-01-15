from ..config.mysqlconnection import connectToMySQL
from flask import flash
from ..models import user

class Tree:
    db = "arbortrary"

    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.locations = data['locations']
        self.reasons = data['reasons']
        self.date_planted = data['date_planted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.visitors = []

    # def __str__(self):
    #     return self.first_name

    # def __repr__(self):
    #     return self.first_name

    @classmethod
    def create_tree(cls, data):
        query = "INSERT INTO trees (species, locations, reasons, date_planted, user_id) VALUES (%(species)s, %(locations)s, %(reasons)s, %(date_planted)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_tree_by_id(cls, data):
        query = "SELECT * FROM trees WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all_by_id(cls,data):
        query = "SELECT * FROM trees LEFT JOIN users ON users.id = user_id WHERE trees.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data) 
        for row in results:
            new_tree = cls(row)
            user_data = { 
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],  
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            new_tree.user = user.User(user_data)
        return new_tree
        
    @classmethod
    def get_my_trees(cls, data):
        query = "SELECT * FROM trees LEFT JOIN users ON users.id = trees.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        my_trees = []
        for row in results:
            my_trees.append(cls(row))
        return my_trees

    @classmethod
    def update_tree(cls,data):
        query = "UPDATE trees SET species = %(species)s, locations=%(locations)s, reasons = %(reasons)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy_tree(cls,data):
        query = "DELETE FROM trees WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trees LEFT JOIN users ON users.id = trees.user_id LEFT JOIN visits ON  trees.id = visits.tree_id LEFT JOIN users AS visitors ON visitors.id = visits.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        all_trees = []
        for row in results:
            # make a new instance of the tree
            new_tree = True
            #attn: it is a joint table and these below are class User Attributes
                # it is a dictionary of the user's info
            visitor_data = { 
                'id': row['visitors.id'],
                'first_name': row['visitors.first_name'],
                'last_name': row['visitors.last_name'],
                'email': row['visitors.email'],  
                'password': row['visitors.password'],
                'created_at': row['visitors.created_at'],
                'updated_at': row['visitors.updated_at'],
            }
            # if there's more visitors on the last visit, then it's not a new visit
            if len(all_trees) > 0 and all_trees[-1].id == row['id']:
                all_trees[-1].visitors.append(user.User(visitor_data))
                new_tree = False
            if new_tree:
                # make a new user visit object 
                this_tree = cls(row)
                user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],  
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                # create a user instance for this creator
                this_user = user.User(user_data)
                this_tree.user = this_user
                #Q: is there still a person who visits this post?
                if row['visitors.id'] is not None:
                    this_visitor = user.User(visitor_data)
                    this_tree.visitors.append(this_visitor)
                all_trees.append(this_tree)
        return all_trees



    # @classmethod
    # def get_all_by_id(cls,data):
    #     query = "SELECT * FROM trees LEFT JOIN users ON users.id = trees.user_id LEFT JOIN visits ON  trees.id = visits.tree_id LEFT JOIN users AS visitors ON visitors.id = visits.user_id WHERE trees.id = %(id)s;"
    #     results = connectToMySQL(cls.db).query_db(query,data) 
    #     all_trees = []
    #     for row in results:
    #         # make a new instance of the tree
    #         new_tree = True
    #         #attn: it is a joint table and these below are class User Attributes
    #             # it is a dictionary of the user's info
    #         visitor_data = { 
    #             'id': row['visitors.id'],
    #             'first_name': row['visitors.first_name'],
    #             'last_name': row['visitors.last_name'],
    #             'email': row['visitors.email'],  
    #             'password': row['visitors.password'],
    #             'created_at': row['visitors.created_at'],
    #             'updated_at': row['visitors.updated_at'],
    #         }
    #         # if there's more visitors on the last visit, then it's not a new visit
    #         if len(all_trees) > 0 and all_trees[-1].id == row['id']:
    #             all_trees[-1].visitors.append(user.User(visitor_data))
    #             new_tree = False
    #         if new_tree:
    #             # make a new user visit object 
    #             this_tree = cls(row)
    #             user_data = {
    #                 'id': row['users.id'],
    #                 'first_name': row['first_name'],
    #                 'last_name': row['last_name'],
    #                 'email': row['email'],  
    #                 'password': row['password'],
    #                 'created_at': row['users.created_at'],
    #                 'updated_at': row['users.updated_at'],
    #             }
    #             # create a user instance for this creator
    #             this_user = user.User(user_data)
    #             this_tree.user = this_user
    #             #Q: is there still a person who visits this post?
    #             if row['visitors.id'] is not None:
    #                 this_visitor = user.User(visitor_data)
    #                 this_tree.visitors.append(this_visitor)
    #             all_trees.append(this_tree)
    #     return all_trees

    @classmethod
    def visit_tree(cls, data):
        query = "INSERT INTO visits (user_id, tree_id) VALUES (%(user_id)s, %(tree_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    # @classmethod
    # def unvisit_tree(cls, data):
    #     query = "DELETE FROM visits WHERE tree_id = %(tree_id)s AND user_id = %(user_id)s);"
    #     return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_visited_trees(cls, data):
        visited_trees = []
        query = "SELECT tree_id FROM visits JOIN users ON users.id = user_id WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            visited_trees.append(row['post_id'])
        return visited_trees


    @staticmethod
    def validate_tree(data):
        is_valid = True
        if len(data["species"]) < 5:
            flash("Species must be at least 5 characters.", "tree")
            is_valid=False
        if len(data["locations"]) < 2:
            flash("Locations must be at least 2 characters.", "tree")
            is_valid=False
        if len(data["reasons"]) > 50:
            flash("Reasons cannot exceed 50 characters.", "tree")
            is_valid=False
        # if len(data["reasons"]) == 0:
        #     flash("Reasons cannot be empty.", "tree")
        #     is_valid=False
        if data["date_planted"] == "":
            flash("Select a date.", "tree")
            is_valid=False
        return is_valid