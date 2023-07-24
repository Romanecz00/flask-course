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

@app.route("/<field>")
def f_return(field):
	if field.lower() in ['id', 'name', 'age', 'sex', 'location']:
		rez = choice(dataset).get()[field.lower()]
		return json.dumps({field:rez})
	else:
		return "Error: no such field exists!\n", 404

@app.route("/person/<int:_id>")
def id_search(_id):
	for i in dataset:
		if i.get()['id'] == _id:
			return i.get()
	return "Error:No entity found with such ID!\n", 404
	

@app.route("/count")
def get_count():
	return len(dataset)


