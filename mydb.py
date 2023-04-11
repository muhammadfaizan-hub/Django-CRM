import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
)

# prepare a cursor object using cursor() method
cursorObject = database.cursor()

# create a database
cursorObject.execute("CREATE DATABASE elderco")

print("Database created successfully........")