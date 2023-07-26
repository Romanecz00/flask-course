from flask import Flask, request, json, g
#import sqlite3 #json,
from flask_sqlalchemy import SQLAlchemy
from random import choice, randint
from pathlib import Path 

app = Flask(__name__)
BASE_APP_DIR = Path(__file__).parent
TEST_DB_DIR = BASE_APP_DIR / "test.db"
DB_DIR = BASE_APP_DIR / 'main.db'
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_DIR}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)

class QuoteModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(32), unique=False)
	text = db.Column(db.String(255), unique=False)
	
	def __init__(self, author, text):
		self.author = author
		self.text  = text
