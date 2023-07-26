import sqlite3

def create_table():
	create_table = """
	CREATE TABLE IF NOT EXISTS quotes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	author TEXT NOT NULL,
	text TEXT NOT NULL
	);
	"""
	# Подключение в БД
	connection = sqlite3.connect("test.db")
	# Создаем cursor, он позволяет делать SQL-запросы
	cursor = connection.cursor()
	# Выполняем запрос:
	cursor.execute(create_table)
	# Фиксируем выполнение(транзакцию)
	connection.commit()
	# Закрыть курсор:
	cursor.close()
	# Закрыть соединение:
	connection.close()
 
if __name__=='__main__':
	create_table()
