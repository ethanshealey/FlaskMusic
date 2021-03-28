from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class SearchSongForm(FlaskForm):
    song = StringField('Song Name', validators=[DataRequired()])
    submit = SubmitField('Search')

class AddSongForm(FlaskForm):
    song_url = StringField('YouTube URL', validators=[DataRequired()], render_kw={'placeholder': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
    song_name = StringField('Song Name', validators=[DataRequired()], render_kw={'placeholder': 'Never Give You Up'})
    song_artist = StringField('Song Artist', validators=[DataRequired()], render_kw={'placeholder': 'Rick Astley'})
    song_album = StringField('Song Album', render_kw={'placeholder': 'Never Give You Up'})
    song_album_art = FileField('Album Art Upload')
    submit = SubmitField('Add Song')