from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_user import User
from flask_app.models.models_game import Show
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
    session.pop('list', None)
    return render_template('dashboard.html', user = user)

@app.route('/add_show')
def add_show():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    return render_template('add_show.html', user=user)

@app.route('/find_shows', methods=['POST'])
def find_shows():
    show = request.form['name']
    url = (f"https://api.tvmaze.com/search/shows?q={show}")

    response = requests.get(url)

    results = response.json()

    shows = []
    for result in results:
        show = [result['show']['name'], result['show']['image'], result['show']['summary'], result['show']['url']]
        shows.append(show)
    
    session['shows'] = shows

    return redirect('/add_show')


