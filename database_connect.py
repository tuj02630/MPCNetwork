import mysql.connector

connection = connection = mysql.connector.connect(host='127.0.0.1',
                                                  user='root',
                                                  password='',
                                                  database='hw02')
with connection:
    with connection.cursor() as cursor:
        print("Connection")
    connection.commit()
cursor.close()