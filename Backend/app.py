import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bcrypt import Bcrypt


app = Flask(__name__, template_folder='../Frontend/html' ,  static_folder='../Frontend/css')
app.config.from_object(Config)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, '../Frontend/images')