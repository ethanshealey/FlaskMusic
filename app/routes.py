from app import app, db
import requests
from bs4 import BeautifulSoup
from flask import render_template, flash, redirect, url_for
from app.form import LoginForm, RegisterForm, SearchSongForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Song

@app.route('/', methods=['GET', 'POST'])
def index():
    songs = db.session.query(Song).order_by(Song.date_added).limit(10).all()
    return render_template('index.html', songs=songs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        u = User(username=form.username.data, fname=form.fname.data, lname=form.lname.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Congratulations! You have been registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))