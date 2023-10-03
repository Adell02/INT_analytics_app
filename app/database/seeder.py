
from flask import Blueprint

from app.app import conn,cursor

seeder_bp = Blueprint('seeder', __name__)

@seeder_bp.route('/seeder')
def seeder():
    print("Enter Email: ",end="")
    email = str(input())
    print("\nEnter Password: ",end="")
    password = str(input())
    print("\nEnter Comapany: ",end="")
    company = str(input())

    #Creating a connection cursor
    cursor.execute(''' INSERT INTO user (userid,email,password,company) VALUES (0,%s,%s,%s)''',(email,password,company))
    #Saving the Actions performed on the DB
    conn.commit()
    return "Table Populated"
 
@seeder_bp.route('/new_table')
def new_table():    
    #Executing SQL Statements
    cursor.execute(''' CREATE TABLE user (userid INT NOT NULL AUTO_INCREMENT, email VARCHAR(50) NOT NULL, password VARCHAR(50), company VARCHAR(50),PRIMARY KEY(userid)); ''')
    #Saving the Actions performed on the DB
    conn.commit()

    return "Table Created"

@seeder_bp.route('/fetch_all')
def fetch_all():
    cursor.execute(''' SELECT * from user''')
    return cursor.fetchall()
