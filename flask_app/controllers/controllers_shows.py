from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_user import User
from flask_app.models.models_show import Show
import requests
import re
from pprint import pprint

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    shows = Show.get_all()
    return render_template('dashboard.html', user = user, shows = shows)

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
        show = [result['show']['name'], result['show']['image'], result['show']['summary'], result['show']['genres']]
        shows.append(show)
    
    session['shows'] = shows

    return redirect('/add_show')

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    data = {
        'name' : request.form['name'],
        'image' : request.form['image'],
        'summary' : request.form['summary'],
        'genres' : request.form['genres'],
        'user_id' : session['user_id'],
    }
    Show.add_to_watchlist(data)
    return redirect('/dashboard')

@app.route('/show_details/<int:show_id>')
def show_details(show_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : show_id
    }
    show = Show.get_one(data)
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    return render_template('view_show.html', show = show, user = user)

@app.route('/delete_show/<int:show_id>')
def delete_show(show_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : show_id
    }
    Show.delete_show(data)
    return redirect('/dashboard')


