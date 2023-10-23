# auth.py
from functools import wraps
from flask import Blueprint, render_template,request,redirect,url_for,session
import bcrypt

from app.database.seeder import *
from app.utils.account.token import *

auth_bp = Blueprint('auth', __name__)

#--------------- WRAPPERS ---------------#

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


# This wrapper has to be implemented so that if user is logged, 
# just show a message saying he is logged, and redirect him to the main page

def logout_required(route_function):
    @wraps(route_function)
    def wrapper(*args,**kwargs):
        if 'user_id' in session:
            # User is Logged In
            logout()
                   
        return route_function(*args,**kwargs)
            
    return wrapper


#--------------- ROUTES ---------------#

@auth_bp.route('/login',methods=['GET', 'POST'])
def login():
    sign_up_url = url_for('auth.register')
    if request.method == 'POST':                   
        if request.form['change_password'] == 'False':
            email = request.form['email']
            password = request.form['password']

            fetched_user = fetch_user(email) 

            # Check if the username exists in the users dictionary
            if fetched_user != -1:  
                user_id = fetched_user.id
                user_password = fetched_user.password
                user_email = fetched_user.email
                user_personal_token = fetched_user.personal_token
                user_org_name = fetched_user.org_name
                user_external_token = fetched_user.external_token
                user_confirmed = fetched_user.is_confirmed  
                user_role = fetched_user.role
                # Check if user is confirmed
                if not user_confirmed:
                    resend_url = ''
                    return render_template('login.html', error='User is not confirmed. Use this link to send the code again: '+resend_url,sign_up_url=sign_up_url)
                # Check if the entered password matches the stored hash
                if bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
                    session['user_id'] = user_id
                    session['user_email'] = user_email
                    session['personal_token'] = user_personal_token
                    session['org_name'] = user_org_name
                    session['external_token'] = user_external_token
                    session['role'] = user_role
                    session['confirmed'] = user_confirmed
                    # Redirect to a success page or dashboard
                    return redirect(url_for('dash.dashboard'))
                else:
                    # Display an error message if authentication fails
                    return render_template('login.html', error='Invalid credentials',sign_up_url=sign_up_url)

            # Display an error message if the username doesn't exist
            return render_template('login.html', error='User is not registered',sign_up_url=sign_up_url)
        elif request.form['change_password'] == 'True':
            email = request.form['email']
            if check_existance('email',email):
                url_change_password = url_for("auth.change_password",token_user=generate_token(email) )
                return redirect(url_change_password)
            else:
                return render_template('login.html', error='This email is not registered. Please check that field.',sign_up_url=sign_up_url)

    return render_template('login.html',sign_up_url=sign_up_url)

@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route("/register", methods=["GET", "POST"])
@logout_required
def register():

    if request.method == 'POST':
        in_email = request.form['email']        
        in_password = request.form['password']
        
        if in_password != request.form['password_confirmation']:
            return render_template("register.html",error="Passwords don't match")

        if fetch_user(in_email) != -1:
            # EMAIL IS ALREADY IN OUR DATABASE
            return render_template("register.html",error="This email has been used")         
        
        seeder(email=in_email,password=in_password)

        #flash("A confirmation email has been sent via email.", "success")
        return render_template("login.html",error="")

    return render_template("register.html")


@auth_bp.route("/change_password/<token_user>", methods=["GET", "POST"])
def change_password(token_user):
    error =""
    email = confirm_token(token_user)
    if email:
        if request.method == 'POST':
            new_password = request.form['password']    
            if new_password == request.form['password_confirmation']:
                hashedpass = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                edit_user(email,'password',hashedpass.decode())  
                error = "Password changed successfully!" 
                return redirect(url_for('auth.login'))         
            else:
                error = "Passwords introduced are different."
    return render_template("change_password.html",error=error)