import sqlite3

connection = sqlite3.connect("banco.db")
cursor = connection.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, name text, stars real, diaria real,cidade text)"

cria_hotel = "INSERT INTO hoteis VALUES ('1','Alpha',4.3,400,'Rio de Janeiro')"

cursor.execute(cria_tabela)
cursor.execute(cria_hotel)

connection.commit()
connection.close()
