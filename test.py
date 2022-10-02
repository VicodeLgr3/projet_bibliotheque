import sqlite3

connection = sqlite3.connect('bibliotheque.db')
cursor = connection.cursor()

cursor.execute('INSERT INTO EMPRUNT VALUES(?,?,?)', ["1465554454", "544544155", "2022-10-01"])
connection.commit()

cursor.close()
connection.close()



