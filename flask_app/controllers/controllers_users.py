from flask_app import app
from flask import render_template, redirect, session, request, flash, url_for
from flask_app.models.models_user import User
from flask_app.models.models_show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password'],
    }
    valid = User.user_validator(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data['pw_hash'] = pw_hash
        user = User.create_user(data)
        session['user_id'] = user
        print('You got it, you are a new user')
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : user_id
    }
    user = User.get_one(user_data)
    return render_template('profile.html', user=user)

@app.route('/update_email/<int:user_id>', methods=['POST'])
def update_email(user_id):
    data = {
        'email' : request.form['email'],
    }
    user_data = {
        'id' : user_id
    }
    user = User.get_one(user_data)
    valid = User.email_validator(data)
    if valid:
        User.update_email(request.form, user_id)
        flash('Email Address Updated', 'update')
        return redirect (f'/profile/{user.id}')
    return render_template('profile.html', user = user)

