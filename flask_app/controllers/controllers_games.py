from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_user import User
from flask_app.models.models_game import Game
import requests

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    return render_template('dashboard.html', user = user)

@app.route('/add_game')
def add_game():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add_game.html')

@app.route('/get_games', methods=['POST'])
def get_games():
    response = requests.get("https://api.rawg.io/api/gameskey=0ec2c3dffd054b1c9f7cfff9bb16a902")
    print(response.json())