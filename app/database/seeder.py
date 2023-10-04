
from flask import Blueprint
import bcrypt

from app.config import Config
from app import conn,cursor

seeder_bp = Blueprint('seeder', __name__)

@seeder_bp.route('/seeder')
def seeder():
    print("Enter Email: ",end="")
    email = str(input())
    print("\nEnter Password: ",end="")
    password = bcrypt.hashpw(input().encode('utf-8'), bcrypt.gensalt())
    print(password)
    print("\nEnter Comapany: ",end="")
    company = str(input())

    #Creating a connection cursor
    cursor.execute(''' INSERT INTO user (userid,email,password,company) VALUES (0,%s,%s,%s)''',(email,password,company))
    #Saving the Actions performed on the DB
    conn.commit()
    return fetch_all()
 
@seeder_bp.route('/new_table')
def new_table():    
    #Executing SQL Statements
    cursor.execute(''' CREATE TABLE user (userid INT NOT NULL AUTO_INCREMENT, email VARCHAR(50) NOT NULL, password VARCHAR(100), company VARCHAR(50),PRIMARY KEY(userid)); ''')
    #Saving the Actions performed on the DB
    conn.commit()

    return "Table Created"

@seeder_bp.route('/fetch_all')
def fetch_all():
    cursor.execute(''' SELECT * from user''')
    return cursor.fetchall()

@seeder_bp.route('/delete_user')
def delete_user():
    print(fetch_all())
    print("Enter Email: ",end="")
    email = input()

    cursor.execute(''' DELETE FROM user WHERE email = %s;''',(email,))
    conn.commit()
    return fetch_all()



