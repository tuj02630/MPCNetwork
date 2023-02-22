import mysql.connector

connection = connection = mysql.connector.connect(host='',
                                                  user='nick',
                                                  password='',
                                                  database='mpcdb')
with connection:
    with connection.cursor() as cursor:
        print("Connection")
    connection.commit()
cursor.close()