from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

db = 'show_watchlist_db'

class Show:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['url']