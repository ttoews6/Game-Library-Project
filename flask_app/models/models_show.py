from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_user import User

db = 'show_watchlist_db'

class Show:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.image = data['image']
        self.summary = data['summary']
        self.genres = data['genres']
        self.user_id = data['user_id']
        self.users = None
        self.user = None

    @classmethod
    def add_to_watchlist(cls, data):
        query = """
                INSERT INTO shows (name, image, summary, genres, user_id)
                VALUES ( %(name)s, %(image)s, %(summary)s, %(genres)s, %(user_id)s )
                """
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM shows
                JOIN users ON shows.user_id = users.id
                """
        results = connectToMySQL(db).query_db(query)
        all = []
        for result in results:
            shows = cls(result)
            user_data = {
                'id' : result['users.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'email' : result['email'],
                'password' : result['password'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at'],
            }
            shows.users = User(user_data)
            all.append(shows)
        return all
    
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM shows
                WHERE id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        show = cls(results[0])
        return show

    
    @classmethod
    def delete_show(cls, data):
        query = """
                DELETE FROM shows WHERE id = %(id)s
                """
        return connectToMySQL(db).query_db(query, data)
