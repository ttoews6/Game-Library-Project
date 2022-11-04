from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_user import User
from flask_app.models.models_game import Game
import requests
from pprint import pprint

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
    game = request.form['name']
    url = (f"https://rawg-video-games-database.p.rapidapi.com/games?search={game}&page=1&page_size=6&key=")

    headers = {
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": ""
    }

    response = requests.request("GET", url, headers=headers)

    # First Game Result
    session['name_1'] = response.json()['results'][0]['name']
    session['platform_pc_1'] = response.json()['results'][0]['platforms'][0]['platform']['name']
    session['platform_xbox_1'] = response.json()['results'][0]['platforms'][1]['platform']['name']
    session['platform_playstation_1'] = response.json()['results'][0]['platforms'][2]['platform']['name']
    session['platform_nintendo_1'] = response.json()['results'][0]['platforms'][3]['platform']['name']
    session['background_img_1'] = response.json()['results'][0]['background_image']

    # Second Game Result
    session['name_2'] = response.json()['results'][1]['name']
    session['background_img_2'] = response.json()['results'][1]['background_image']

    # Third Game Result
    session['name_3'] = response.json()['results'][2]['name']
    session['background_img_3'] = response.json()['results'][2]['background_image']
    return redirect('/add_game')
