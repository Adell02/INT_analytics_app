
from flask import Blueprint,request,render_template,redirect
import bcrypt


from app.config import Config
from app import conn,cursor
from app.database.models import User,All_users
from app.utils.account.token import generate_personal_token


seeder_bp = Blueprint('seeder', __name__)

@seeder_bp.route('/seeder')
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
    confirmed = '1'
    personal_token = generate_personal_token(email)
    external_token = ""
    org_name = ""

    #Creating a connection cursor
    cursor.execute(''' INSERT INTO user (userid,email,password,personal_token,org_name,external_token,role,is_confirmed) VALUES (0,%s,%s,%s,%s,%s,%s,%s)''',(email,password,personal_token,org_name,external_token,role,confirmed))
    #Saving the Actions performed on the DB
    conn.commit()

    return fetch_all()
 
@seeder_bp.route('/new_table')
def new_table():    
    #Executing SQL Statements
    cursor.execute(''' CREATE TABLE user (userid INT NOT NULL AUTO_INCREMENT, email VARCHAR(50) NOT NULL, password VARCHAR(100) NOT NULL, personal_token VARCHAR(100) NOT NULL, org_name VARCHAR(50), external_token VARCHAR(100),role VARCHAR(50) NOT NULL DEFAULT 'user', is_confirmed BOOLEAN NOT NULL, PRIMARY KEY(userid)); ''')
    #Saving the Actions performed on the DB
    conn.commit()

    return "Table Created"

@seeder_bp.route('/fetch_all',methods=['GET'])
def fetch_all():
    cursor.execute(''' SELECT * from user;''')
    all_users = All_users()
    [all_users.add_user(User(x)) for x in cursor.fetchall()]

    if request.method == 'GET':
        return (repr(all_users))
    else:
        return all_users
    
@seeder_bp.route('/fetch_user/<email>',methods=['GET'])
def fetch_user(email):
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
def delete_user():
    print(fetch_all())
    print("Enter Email: ",end="")
    email = input()

    cursor.execute(''' DELETE FROM user WHERE email = %s;''',(email,))
    conn.commit()
    return fetch_all()

@seeder_bp.route("/confirm_user")
def confirm_user(email=None,is_send = 'y'):
    from app.utils.communication.mailing import send_email

    if not email:
        print(fetch_all())

        print("Enter Email: ",end="")
        email = input()

        print("Send email? [y/n]: ", end="")
        is_send = input()

    if is_send == 'y':
        send_email(email,"Confirm Email",render_template("confirm_email.html",confirm_url = "confirm_url"))
        return "Confirmation email sent successfully"
    elif is_send == 'n':      
        cursor.execute(''' UPDATE user SET is_confirmed=1 WHERE email=%s''',(email,))
        conn.commit()
        return "User confirmed successfully"





