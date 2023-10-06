# auth.py
from functools import wraps
from flask import Blueprint, render_template,request,redirect,url_for,session
import bcrypt

from app.database.seeder import fetch_all

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        fetched_users = fetch_all()   
        print(fetched_users)    
        fetched_emails = [x[1] for x in fetched_users]
        fetched_passwords = [x[2] for x in fetched_users]

        email = request.form['email']
        password = request.form['password']

        # Check if the username exists in the users dictionary
        try:
            index_user = fetched_emails.index(email)
        except ValueError:
            index_user = -1
        if index_user >= 0:           
            # Check if the entered password matches the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), fetched_passwords[index_user].encode('utf-8')):
                session['user_id'] = fetched_users[index_user][0]
                # Redirect to a success page or dashboard
                return redirect(url_for('dash.dashboard'))
            else:
                # Display an error message if authentication fails
                return render_template('login.html', error='Invalid credentials')

        # Display an error message if the username doesn't exist
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    session.clear()
    return render_template('login.html')


def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args,**kwargs):
        if 'user_id' in session:
            # User is Logged In
            return route_function(*args,**kwargs)        
        else:
            # User is NOT Logged In
            return redirect(url_for('auth.login'))
    return wrapper