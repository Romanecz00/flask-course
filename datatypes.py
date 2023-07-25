import json
from os import path
from random import randint

class Person:
	data = {'id':'','name':'', 'age':'', 'sex':'', 'location':''}
	fields=['name', 'age', 'sex', 'location']
	def __init__(self, stuff={'id':-1, 'name':'Test instance', 'age':randint(0,120), 'sex':'NullPointerException', 'location':'in your walls'}):
		self.data = stuff
	
	def get(self):
		return self.data
	
	def get_specific(self, mode='all'):
		if mode.lower() in ['all','id','name','age','sex','location']:
			return self.data[mode.lower()]
		else:
			return "wrong mode"
			
	def _set(self, field, data):
		if field in self.fields:
			if type(data) in (int, str, float):
				self.data[field] = data
			else:
				raise TypeError(f"wrong data type {type(data)} for field {field}\n")
		else:
			raise KeyError(f"wrong field key parameter {field}\n")
	
	def __cmp__(self, other):
		if type(other) == type(self):
			for k,v in self.data.items():
				if not other[k] == v:
					return False
			return True
		else:
			return False

# class Quotary:
# 	data = [
# 		{'id':'', 'author':'', 'content':''}
# 		]
# 	
# 	def validate(self, stuff):
# 		if type(stuff) == dict:
# 			if ['name','author','content'].sort() == stuff.keys().sort():
# 				pass
# 		else:
# 			return False
# 	
# 	def __init__(self, q=[{'id':'-1', 'author':'Debug Entity', 'content':'1337 69 420 71M3'}]):
# 		if type(q) == list:
# 			if 
# 		elif type(q) == dict:
# 			
# 		else:
# 			raise TypeError("wrong data")
