import sqlite3

connection = sqlite3.connect('bibliotheque.db')
cursor = connection.cursor()

cursor.execute('SELECT LIVRE.isbn FROM LIVRE EXCEPT SELECT EMPRUNT.isbn FROM EMPRUNT')
isbn = cursor.fetchall()

for i in isbn:
    cursor.execute('SELECT * FROM EMPRUNT WHERE isbn = ?', [i[0], ])
    x = cursor.fetchall()
    if len(x) != 0:
        print("Marche pas")

cursor.close()
connection.close()