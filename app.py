from flask import Flask
import json
from random import choice, randint
from .datatypes import Person#, Quotary

app = Flask(__name__)

dataset = []
for i in range(0, 1000):
	dataset.append(Person({'id':i, 'name':chr(i)*10, 'age':randint(0,120), 'sex':'NullPointerException', 'location':'in your walls'}))

@app.route("/")
def hello_world():
	rez = choice(dataset)
	return json.dumps(rez.get(), indent=2)

@app.route("/name")
def n_return():
	rez = choice(dataset).get()['name']
	return json.dumps({'name':rez})
