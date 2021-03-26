from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    lname = db.Column(db.String(120), index=True, unique=True)
    fname = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100))
    song_artist = db.Column(db.String(100))
    song_album = db.Column(db.String(100))
    song_path = db.Column(db.String(100))
    date_added = db.Column(db.String(100))
    song_album_art = db.Column(db.String(100))

@login.user_loader
def load_user(id):
   return User.query.get(int(id))