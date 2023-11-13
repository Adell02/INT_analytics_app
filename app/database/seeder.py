# Seeder
from functools import wraps
from flask import Blueprint,request,render_template,redirect
import mysql.connector
import bcrypt


from app import conn,cursor
from app.config import Config
from app.database.models import User,All_users
from app.utils.account.token import generate_personal_token


seeder_bp = Blueprint('seeder', __name__)

#--------------- WRAPPER ---------------#

def connection_mysql(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        opening_connection()
        try:
            return route_function(*args, **kwargs)
        finally:
            closing_connection()
    return wrapper

def opening_connection():
    global conn,cursor
    db_config= {
        'host':Config.MYSQL_HOST,
        'user':Config.MYSQL_USER,
        'password':Config.MYSQL_PASSWORD,
        'database':Config.MYSQL_DB
    }

    db_config_ray={
        'host':Config.MYSQL_HOST_RAY,
        'user':Config.MYSQL_USER_RAY,
        'password':Config.MYSQL_PASSWORD_RAY,
        'database':Config.MYSQL_DB_RAY
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(buffered=True,dictionary=True) 
    #conn_ray = mysql.connector.connect(**db_config_ray)
    #cursor_ray = conn_ray.cursor(buffered=True,dictionary=True)

def closing_connection():   
    global conn,cursor 
    cursor.close()
    conn.close()
    # cursor_ray.close()
    # conn_ray.close()
    
#--------------- SEEDER ---------------#

@seeder_bp.route('/seeder')
@connection_mysql
def seeder(email=None,password=None):
    if email == None:
        print("Enter Email: ",end="")
        email = str(input())
        print("\nEnter Password: ",end="")
        password = bcrypt.hashpw(input().encode('utf-8'), bcrypt.gensalt())
        print(password)
    else:
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    role = 'user'
    confirmed = '0'
    personal_token = generate_personal_token(email)
    external_token = ""
    org_name = ""

    #Creating a connection cursor
    cursor.execute(''' INSERT INTO user (userid,email,password,personal_token,org_name,external_token,role,is_confirmed) VALUES (0,%s,%s,%s,%s,%s,%s,%s)''',(email,password,personal_token,org_name,external_token,role,confirmed))
    #Saving the Actions performed on the DB
    conn.commit()

    return fetch_all()
 
@seeder_bp.route('/new_table/<table>')
@connection_mysql
def new_table(table):    
    #Executing SQL Statements
    if table == 'user' or table == 'all':
        cursor.execute(''' CREATE TABLE user (userid INT NOT NULL AUTO_INCREMENT, email VARCHAR(50) NOT NULL, password VARCHAR(100) NOT NULL, personal_token VARCHAR(100) NOT NULL, org_name VARCHAR(50), external_token VARCHAR(100),role VARCHAR(50) NOT NULL DEFAULT 'user', is_confirmed BOOLEAN NOT NULL, PRIMARY KEY(userid)); ''')
    elif table == 'dashboard' or 'all':
        cursor.execute(''' CREATE TABLE dashboard (token_id VARCHAR(100) NOT NULL, org_name VARCHAR(50), configuration JSON,PRIMARY KEY(token_id),FOREIGN KEY (token_id) REFERENCES user(personal_token)); ''')
    elif table == 'data' or 'all':
        #cursor.execute(''' CREATE TABLE user (userid INT NOT NULL AUTO_INCREMENT, email VARCHAR(50) NOT NULL, password VARCHAR(100) NOT NULL, personal_token VARCHAR(100) NOT NULL, org_name VARCHAR(50), external_token VARCHAR(100),role VARCHAR(50) NOT NULL DEFAULT 'user', is_confirmed BOOLEAN NOT NULL, PRIMARY KEY(userid)); ''')
        pass
    #Saving the Actions performed on the DB
    conn.commit()

    return "Table Created"

@seeder_bp.route('/fetch_all',methods=['GET'])
@connection_mysql
def fetch_all():
    conn.commit()
    cursor.execute(''' SELECT * from user;''')
    all_users = All_users()
    [all_users.add_user(User(x)) for x in cursor.fetchall()]

    if request.method == 'GET':
        return (repr(all_users))
    else:
        return all_users
    
@seeder_bp.route('/fetch_user/<email>',methods=['GET'])
@connection_mysql
def fetch_user(email):
    conn.commit()
    cursor.execute(''' SELECT * from user WHERE email = %s;''',(email,))
    user = cursor.fetchone()

    if not user:
        if request.method == 'GET':
            return("This user is not registered")
        else:
            return(-1)

    user = User(user)

    if request.method == 'GET':
        return(repr(user))
    else:
        return(user)

@seeder_bp.route('/delete_user')
@connection_mysql
def delete_user():
    print(fetch_all())
    print("Enter Email: ",end="")
    email = input()

    cursor.execute(''' DELETE FROM user WHERE email = %s;''',(email,))
    conn.commit()
    return fetch_all()

@connection_mysql
def edit_user(email,field,value):
    query = "UPDATE user SET " + field + "=\'"+value+"\' WHERE email = \'"+email+"\';"
    cursor.execute(query)
    conn.commit()
    return True

@connection_mysql
def check_existance(field,value):
    query = "SELECT * FROM user WHERE " + field +"=\'"+value+"\';"
    cursor.execute(query)
    conn.commit()
    fetch = cursor.fetchone()
    return fetch

@seeder_bp.route("/confirm_user")
@connection_mysql
def confirm_user(email=None):

    if not email:
        print(fetch_all())

        print("Enter Email: ",end="")
        email = input()

    cursor.execute(''' UPDATE user SET is_confirmed=1 WHERE email=%s''',(email,))
    conn.commit()
    return "User confirmed successfully"





