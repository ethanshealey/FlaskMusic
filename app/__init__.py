from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:######@127.0.0.1/flask_music_app"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

from app import routes