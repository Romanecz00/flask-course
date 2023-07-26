from flask import Flask, request, json
import sqlite3 #json,
from random import choice, randint
from .datatypes import Person#, Quotary

app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False

dataset = []
for i in range(0, 1000):
	dataset.append(Person({'id':i, 'name':chr(i)*10, 'age':randint(0,120), 'sex':'NullPointerException', 'location':'in your walls'}))

@app.route("/")
def hello_world():
	rez = choice(dataset)
	return json.dumps(rez.get(), indent=2)

@app.route("/<field>")
def f_return(field):
	if field.lower() in Person().get().keys():
		rez = choice(dataset).get()[field.lower()]
		return json.dumps({field:rez})
	else:
		return "Error: no such field exists!\n", 404

@app.route("/person", methods=['POST'])
def field_search():
	data = request.json
	for k,v in data.items():
		if k in Person().fields and type(v) in (int, str, float):
			for p in dataset:
				if str(p.get()[k]) == str(v):
					return json.dumps(p.get())
			return f"Error: person with {k} of \"{v}\" was not found", 404
		else:
			return f"Error: incorrect query parameter {k}", 400
	# if 'query' in data.keys() and data['query']:
	# 	if type(data['query'])==str and data['query'].lower() in Person().get().keys():
	# 		rez = choice(dataset).get()[data['query'].lower()]
	# 		return json.dumps({data['query']:rez})
	# 	else:
	# 		return "Error: no such field exists!\n", 404
	# else:
	# 	return "Error: no 'query' key in request, bad request.", 400
	# for i in dataset:
	# 	if i.get()['id'] == _id:
	# 		return i.get()
	# return "Error:No entity found with such ID!\n", 404
	
@app.route('/edit/<int:_id>', methods=['PUT'])
def edit_person(_id):
	data = request.json
	for p in dataset:
		if p.get()['id'] == _id:
			for k,v in data.items():
				if not k in p.fields:
					return f"Error: wrong data field {k}", 400
				try:
					p._set(k, v)
				except Exception as e:
					return f"Internal Server Error", 500
			return json.dumps(p.get())
	return f"Error: no person with {_id} id found!\n", 404

@app.route('/birth', methods=['POST', 'PUT']) #because birth is the /create-person for those of us who aren't psychopaths
def create_person():
	data = request.json
	flag = True
	for i in ['name', 'age', 'sex', 'location']:
		if not i in data.keys():
			flag = False
		elif type(data[i]) not in (int, str, float):
			flag = False
	if flag:
		dataset.append(Person({'id':len(dataset)+1, 'name':data['name'], 'age':data['age'], 'sex':data['sex'], 'location':data['location']}))
		return json.dumps({'id':len(dataset), 'name':data['name'], 'age':data['age'], 'sex':data['sex'], 'location':data['location']})
	return f'Error: invalid data. data: {data}\n', 400

@app.route("/count")
def get_count():
	return {'count':len(dataset)}



# about_me = {
# 	"name": "Евгений",
# 	"surname": "Юрченко",
# 	"email": "eyurchenko@specialist.ru"
# }
# 
# quotes = [
# 	{
# 		"id": 3,
# 		"author": "Rick Cook",
# 		"text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
# 	},
# 	{
# 		"id": 5,
# 		"author": "Waldi Ravens",
# 		"text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
# 	},
# 	{
# 		"id": 6,
# 		"author": "Mosher’s Law of Software Engineering",
# 		"text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
# 	},
# 	{
# 		"id": 8,
# 		"author": "Yoggi Berra",
# 		"text": "В теории, теория и практика неразделимы. На практике это не так."
# 	},
# 
# ]

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
		if len(data) == 1:
			data = data[0]
		return data


# http://127.0.0.1:5000/about
# @app.route("/about")
# def about_author():
# 	return about_me


# # GET: http://127.0.0.1:5000/quotes
@app.route("/quotes")
def get_quotes():
	try:
		quotes = call_db(f"SELECT * from quotes;")
		if quotes:
			rez = [{'id':i[0], 'name':i[1], 'quote':i[2]} for i in quotes if len(i)==3]
			return json.dumps(rez)
	except Exception as e:
		return f"Internal Server Error:\n{str(e)}\n", 500
	return f'404', 404


# http://127.0.0.1:5000/quotes/2
# http://127.0.0.1:5000/quotes/5
# http://127.0.0.1:5000/quotes/10
# http://127.0.0.1:5000/quotes/50
@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
	try:
		quotes = call_db(f"SELECT * from quotes where id is {quote_id}")
		if quotes:
			quote = {'id':quotes[0], 'name':quotes[1], 'quote':quotes[2]}
			return json.dumps(quote)
	except Exception as e:
		return f"Internal Server Error:\n{str(e)}\n", 500
	return f"Quote with id={quote_id} not found", 404


# @app.route("/quotes/count")
# def quotes_count():
# 	return {
# 		"count": len(quotes)
# 	}
# 
# 
# @app.route("/quotes", methods=["POST"])
# def create_quote():
# 	new_quote = request.json
# 	new_id = quotes[-1]["id"] + 1
# 	new_quote["id"] = new_id
# 	quotes.append(new_quote)
# 	return new_quote, 201
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
