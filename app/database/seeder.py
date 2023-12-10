# Seeder
from functools import wraps
from flask import Blueprint,request
import mysql.connector
import pyodbc as sql
import bcrypt
import warnings
warnings.filterwarnings('ignore')
import pandas as pd


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

def connection_sql_ray(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        opening_connection_RAY()
        try:       
            return route_function(*args, **kwargs)
        finally:
            closing_connection_RAY()
    return wrapper

def opening_connection():
    global conn,cursor
    db_config= {
        'host':Config.MYSQL_HOST,
        'user':Config.MYSQL_USER,
        'password':Config.MYSQL_PASSWORD,
        'database':Config.MYSQL_DB,
        'port':Config.MYSQL_PORT
    }    

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(buffered=True,dictionary=True) 
    
def opening_connection_RAY():
    global cursor_ray,conn_ray
        
    db_config_ray=(
        'Driver={SQL Server};'
        f'Server={Config.MYSQL_HOST_RAY},1433;'
        f'Database={Config.MYSQL_DB_RAY};'
        f'UID={Config.MYSQL_USER_RAY}@{Config.MYSQL_HOST_RAY};'
        f'PWD={Config.MYSQL_PASSWORD_RAY};'
        'TrustServerCertificate=yes;' 
        'Encrypt=yes;'       
    )
    
    conn_ray = sql.connect(db_config_ray)
    cursor_ray = conn_ray.cursor()

def closing_connection():   
    global conn,cursor 
    cursor.close()
    conn.close()    
    cursor = None
    conn = None

def closing_connection_RAY():   
    global conn_ray,cursor_ray 
    cursor_ray.close()
    conn_ray.close()
    cursor_ray = None
    conn_ray = None
    
    
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

    return fetch_all_with_connection()
 
@seeder_bp.route('/new_table/<table>')
@connection_mysql
def new_table(table):    
    #Executing SQL Statements
    if table == 'user' or table == 'all':
        cursor.execute(''' CREATE TABLE user (userid INT NOT NULL AUTO_INCREMENT, email VARCHAR(50) NOT NULL, password VARCHAR(100) NOT NULL, personal_token VARCHAR(100) NOT NULL, org_name VARCHAR(50), external_token VARCHAR(100),role VARCHAR(50) NOT NULL DEFAULT 'user', is_confirmed BOOLEAN NOT NULL, PRIMARY KEY(userid)); ''')
    elif table == 'dashboard' or 'all':
        pass
        #cursor.execute(''' CREATE TABLE dashboard (token_id VARCHAR(100) NOT NULL, org_name VARCHAR(50), configuration JSON,PRIMARY KEY(token_id),FOREIGN KEY (token_id) REFERENCES user(personal_token)); ''')
    elif table == 'data' or 'all':
        cursor.execute(''' CREATE TABLE data (org_token VARCHAR(100) NOT NULL, last_timestamp INT, columnes JSON, VINs JSON, PRIMARY KEY(org_token)); ''')
        cursor.execute('''INSERT INTO data (org_token,last_timestamp,columnes,VINs) VALUES ('RAY',NULL,NULL,NULL);''')
    #Saving the Actions performed on the DB
    conn.commit()

    return "Table Created"

@seeder_bp.route('/fetch_all',methods=['GET'])
@connection_mysql
def fetch_all():    
    cursor.execute(''' SELECT * from user;''')    
    all_users = All_users()
    [all_users.add_user(User(x)) for x in cursor.fetchall()]
    conn.commit()

    if request.method == 'GET':
        return (repr(all_users))
    else:
        return all_users

def fetch_all_with_connection():    
    cursor.execute(''' SELECT * from user;''')    
    all_users = All_users()
    [all_users.add_user(User(x)) for x in cursor.fetchall()]
    conn.commit()

    if request.method == 'GET':
        return (repr(all_users))
    else:
        return all_users
    
@seeder_bp.route('/fetch_user/<email>',methods=['GET'])
@connection_mysql
def fetch_user(email):
    
    cursor.execute(''' SELECT * from user WHERE email = %s;''',(email,))
    user = cursor.fetchone()
    conn.commit()

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
    print(fetch_all_with_connection())
    print("Enter Email: ",end="")
    email = input()
    cursor.execute(''' DELETE FROM user WHERE email = %s;''',(email,))
    conn.commit()
    return fetch_all_with_connection()

@connection_mysql
def edit_user(email,field,value):
    query = "UPDATE user SET " + field + "=\'"+str(value)+"\' WHERE email = \'"+email+"\';"
    cursor.execute(query)
    conn.commit()
    return True

@connection_mysql
def check_existance(field,value):
    query = "SELECT * FROM user WHERE " + field +"=\'"+str(value)+"\';"
    cursor.execute(query)
    conn.commit()
    fetch = cursor.fetchone()
    return fetch

@seeder_bp.route("/confirm_user")
@connection_mysql
def confirm_user(email=None):

    if not email:
        print(fetch_all_with_connection())

        print("Enter Email: ",end="")
        email = input()

    cursor.execute(''' UPDATE user SET is_confirmed=1 WHERE email=%s''',(email,))
    conn.commit()
    return "User confirmed successfully"

@connection_sql_ray
def fetch_ray_trip(timestamp_i,timestamp_f):
    CATEGORIES = ["G1","G2","C2","C3","IE","B1","B2","B3","B4"]
    query = '''SELECT DeviceId,OriginalMessage FROM PRORawData WHERE (('''
    for c in CATEGORIES:
        query += f"OriginalMessage LIKE '${c}%'"
        if c == CATEGORIES[len(CATEGORIES)-1]:
            query += ")"
        else:
            query += " OR "
    
    query += f" AND TimeStamp > {timestamp_i} AND TimeStamp < {timestamp_f});"
    
    read_df = pd.read_sql_query(query,conn_ray)
    return read_df

@connection_sql_ray
def fetch_ray_charge(timestamp_i,timestamp_f):
    CATEGORIES = ["H2","H3","H4","H5","H8"]
    query = '''SELECT DeviceId,OriginalMessage FROM PRORawData WHERE (('''
    for c in CATEGORIES:
        query += f"OriginalMessage LIKE '${c}%'"
        if c == CATEGORIES[len(CATEGORIES)-1]:
            query += ")"
        else:
            query += " OR "
    
    query += f" AND TimeStamp > {timestamp_i} AND TimeStamp < {timestamp_f});"
    
    read_df = pd.read_sql_query(query,conn_ray)
    return read_df

@connection_mysql
def edit_data(field,value):
    if field != "columnes" and field != "VINs":
        query = "UPDATE data SET " + field + "="+str(value)+" WHERE org_token = 'RAY';"
    else:
        query = "UPDATE data SET " + field + "= '["+",".join(value)+"]' WHERE org_token = 'RAY';"
    cursor.execute(query)
    conn.commit()
    return True

@connection_mysql
def fetch_data_params(field):
    
    query = "SELECT "+field+" FROM data WHERE org_token = 'RAY';"
    cursor.execute(query)
    conn.commit()
    fetch = cursor.fetchone()

    if field != "columnes" and field != "VINs" or type(fetch[field]) == type(None):
        return fetch[field]    
    else:        
        return fetch[field].strip('][').split(',')
    
@connection_sql_ray
def fetch_ray_gps(vin,timestamp_init,timestamp_end,journey_id):    
    
    query = f'''SELECT TOP(1) DeviceId,Timestamp,OriginalMessage FROM PRORawData WHERE (DeviceId = '{vin}' AND Timestamp >= '{int(timestamp_init)}' AND Timestamp <= '{int(timestamp_end)}' AND OriginalMessage LIKE '$P1%' AND OriginalMessage LIKE '%{int(journey_id)},#&' AND SUBSTRING(OriginalMessage, CHARINDEX(',',OriginalMessage)+1,CHARINDEX(',', OriginalMessage, CHARINDEX(',', OriginalMessage) + 1) - CHARINDEX(',', OriginalMessage) - 1) <> '');'''    
    read_df = pd.read_sql_query(query,conn_ray)
    if len(read_df):
        if read_df['OriginalMessage'][0].split(",")[6] == 'V':
            return ("","")
        split = read_df['OriginalMessage'][0].split(",")[1:5]
        if split[1] == 'N':
            lat = split[0]
        else:
            lat = "-"+split[0]
        if split[3] == 'E':
            long = split[2]
        else:
            long = "-"+split[2]
        
        return (lat,long)
    else:
        return ("","")
