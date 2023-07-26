from flask import Flask, request, json, g
import sqlite3 #json,
from flask_sqlalchemy import SQLAlchemy
from random import choice, randint
from pathlib import Path
from .datatypes import Person#, Quotary

app = Flask(__name__)
BASE_APP_DIR = Path(__file__).parent
DB_DIR = BASE_APP_DIR / "test.db"
json.provider.DefaultJSONProvider.ensure_ascii = False

# dataset = []
# for i in range(0, 1000):
# 	dataset.append(Person({'id':i, 'name':chr(i)*10, 'age':randint(0,120), 'sex':'NullPointerException', 'location':'in your walls'}))
# 
# @app.route("/")
# def hello_world():
# 	rez = choice(dataset)
# 	return json.dumps(rez.get(), indent=2)
# 
# @app.route("/<field>")
# def f_return(field):
# 	if field.lower() in Person().get().keys():
# 		rez = choice(dataset).get()[field.lower()]
# 		return json.dumps({field:rez})
# 	else:
# 		return "Error: no such field exists!\n", 404
# 
# @app.route("/person", methods=['POST'])
# def field_search():
# 	data = request.json
# 	for k,v in data.items():
# 		if k in Person().fields and type(v) in (int, str, float):
# 			for p in dataset:
# 				if str(p.get()[k]) == str(v):
# 					return json.dumps(p.get())
# 			return f"Error: person with {k} of \"{v}\" was not found", 404
# 		else:
# 			return f"Error: incorrect query parameter {k}", 400
# 	
# @app.route('/edit/<int:_id>', methods=['PUT'])
# def edit_person(_id):
# 	data = request.json
# 	for p in dataset:
# 		if p.get()['id'] == _id:
# 			for k,v in data.items():
# 				if not k in p.fields:
# 					return f"Error: wrong data field {k}", 400
# 				try:
# 					p._set(k, v)
# 				except Exception as e:
# 					return f"Internal Server Error", 500
# 			return json.dumps(p.get())
# 	return f"Error: no person with {_id} id found!\n", 404
# 
# @app.route('/birth', methods=['POST', 'PUT']) #because birth is the /create-person for those of us who aren't psychopaths
# def create_person():
# 	data = request.json
# 	flag = True
# 	for i in ['name', 'age', 'sex', 'location']:
# 		if not i in data.keys():
# 			flag = False
# 		elif type(data[i]) not in (int, str, float):
# 			flag = False
# 	if flag:
# 		dataset.append(Person({'id':len(dataset)+1, 'name':data['name'], 'age':data['age'], 'sex':data['sex'], 'location':data['location']}))
# 		return json.dumps({'id':len(dataset), 'name':data['name'], 'age':data['age'], 'sex':data['sex'], 'location':data['location']})
# 	return f'Error: invalid data. data: {data}\n', 400
# 
# @app.route("/count")
# def get_count():
# 	return {'count':len(dataset)}


def validate(quote):
	flag = True
	if len(quote) == 3 and type(quote)==dict:
		for k,v in quote.items():
			if not type(v) in [dict, str, float]:
				flag = False
			if not k in ['name', 'id', 'quote']:
				flag = False
	else:
		flag = False
	return flag

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DB_DIR)
	return db
	
@app.teardown_appcontext
def close_connection():
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def call_db(cmd, db='test.db'):
	try:
		connection = sqlite3.connect(db)
		# Создаем cursor, он позволяет делать SQL-запросы
		cursor = connection.cursor()
		# Выполняем запрос:
		cursor.execute(cmd)
		# Извлекаем результаты запроса
		data = cursor.fetchall()
		# Закрыть курсор:
		cursor.close()
		# Закрыть соединение:
		connection.close()
		
	except Exception as e:
		raise RuntimeError(e)
	else:
		return [{'id':i[0], 'name':i[1], 'quote':i[2]} for i in data if len(i)==3]


@app.route("/quotes")
def get_quotes():
	try:
		quotes = call_db(f"SELECT * from quotes;")
		if quotes:
			return quotes
	except Exception as e:
		return f"Internal Server Error:\n{str(e)}\n", 500
	return f'404', 404


@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
	try:
		quotes = call_db(f"SELECT * from quotes where id is {quote_id}")[0]
		if quotes:
			return quotes
	except Exception as e:
		return f"Internal Server Error:\n{str(e)}\n", 500
	return f"Quote with id={quote_id} not found", 404


@app.route("/quotes/count")
def quotes_count():
	quotes = call_db('select * from quotes')
	if quotes:
		return {"count": len(quotes)}
	return {'count':0}
# 
# 
@app.route("/quotes/create", methods=["POST", "PUT"])
def create_quote():
	new_quote = request.json
	if validate(new_quote):
		connection = get_db()
		cursor = connection.cursor()
		sql = f"INSERT INTO quotes (author, text) VALUES ('{new_quote['name']}', '{new_quote['quote']}');"
		cursor.execute(sql)
		connection.commit()
		new_quote["id"] = cursor.lastrowid
		return new_quote, 201
	else:
		return f"Error: Wrong data/ data:\n{new_quote}\n"
# 
# 
# @app.route("/quotes/<int:quote_id>", methods=['PUT'])
# def edit_quote(quote_id):
# 	new_data = request.json
# 	for quote in quotes:
# 		if quote["id"] == quote_id:
# 			if new_data.get("author"):
# 				quote["author"] = new_data["author"]
# 			if new_data.get("text"):
# 				quote["text"] = new_data["text"]
# 			return quote, 200
# 	return f"Quote with id={quote_id} not found", 404
