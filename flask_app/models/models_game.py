from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

db = 'game_library_db'

class Game:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.size = data['size']