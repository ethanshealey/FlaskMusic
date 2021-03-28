from app import app, db
import requests
import datetime
from bs4 import BeautifulSoup
import os
from flask import render_template, flash, redirect, url_for, request
from app.form import LoginForm, RegisterForm, SearchSongForm, AddSongForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Song
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the newest 5 songs from the database
    songs = db.session.query(Song).order_by(Song.date_added.desc()).limit(5).all()
    return render_template('index.html', title='Homepage', songs=songs)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form=AddSongForm()
    if form.validate_on_submit():

        try:
            # Get the song from YouTube
            SongName = form.song_url.data
            SongFileName = form.song_name.data.replace(' ', '')
            os.system('youtube-dl --extract-audio --audio-format mp3 -o "' + SongFileName + '.mp3" ' + SongName)
            os.system('mv ' + SongFileName + '.mp3 app/static/music')
        except:
            flash('ERROR: Error getting youtube video. Please try again.')
            return redirect(url_for('add'))

        f = form.song_album_art.data
        if(form.song_album_art.data):
            # Save the image
            filename = secure_filename(f.filename)
            filename = '/Users/ethanshealey/Documents/GitHub/FlaskMusic/app/static/images/' + filename
            f.save(filename)
        else:
            f.filename = 'pic05.jpg'

        # Add to database
        s = Song(song_name=form.song_name.data, song_artist=form.song_artist.data, song_album=form.song_album.data, song_path='music/' + SongFileName + '.mp3', song_album_art='images/' + secure_filename(f.filename), date_added=datetime.date.today())
        db.session.add(s)
        db.session.commit()

        # Inform user song had been added successfully 
        flash(form.song_name.data + ' added successfully!')
        return redirect(url_for('all_songs'))
    
    return render_template('add.html', title='Add a new song', form=form)

@app.route('/songs')
def all_songs():
    songs = db.session.query(Song).order_by(Song.song_name).all()
    return render_template('songs.html', title='All Songs', songs=songs)

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
        flash('Welcome back, ' + current_user.fname + '!')
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'), title='Register')

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
    flash('You have been logged out.')
    return redirect(url_for('index'))