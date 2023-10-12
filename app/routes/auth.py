# auth.py
from functools import wraps
from flask import Blueprint, render_template,request,redirect,url_for,session
import bcrypt

from app.database.seeder import fetch_all,confirm_user,seeder
from app.utils.account.token import confirm_token,generate_token

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

def login_confirmed(route_function):
    @wraps(route_function)
    def wrapper(*args,**kwargs):
        if 'user_id' in session:
            if session['confirmed'] == 1:
                # User is Logged In
                return route_function(*args,**kwargs)   
            else:
                #####SHOW MESSAGE FOR NOT BEING CONFIRMED
                return redirect(url_for('auth.login'))     
        else:
            # User is NOT Logged In
            return redirect(url_for('auth.login'))
    return wrapper

# This wrapper has to be implemented so that if user is logged, 
# just show a message saying he is logged, and redirect him to the main page
"""
def logout_required(route_function):
    @wraps(route_function)
    def wrapper(*args,**kwargs):
        if 'user_id' in session:
            # User is Logged In

            return redirect(url_for('auth.login'))        
        else:
            # User is NOT Logged In
            return route_function(*args,**kwargs)
            
    return wrapper
"""

#--------------- ROUTES ---------------#

@auth_bp.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':        
        all_users = fetch_all()   
        print(all_users)    
        fetched_emails = [x.email for x in all_users.users]                

        email = request.form['email']
        password = request.form['password']

        # Check if the username exists in the users dictionary
        try:
            index_user = fetched_emails.index(email)
        except ValueError:
            index_user = -1
        if index_user >= 0:   
            user = all_users.users[index_user]
            user_password = user.password
            user_company = user.company
            user_confirmed = user.is_confirmed  
            # Check if user is confirmed
            if not user_confirmed:
                resend_url = ''
                return render_template('login.html', error='User is not confirmed. Use this link to send the code again: '+resend_url)
            # Check if the entered password matches the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['company'] = user_company
                session['confirmed'] = user_confirmed
                # Redirect to a success page or dashboard
                return redirect(url_for('dash.dashboard'))
            else:
                # Display an error message if authentication fails
                return render_template('login.html', error='Invalid credentials')

        # Display an error message if the username doesn't exist
        return render_template('login.html', error='User is not registered')

    return render_template('login.html')

@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    return render_template('login.html')

@auth_bp.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if 'confirmed' == 1:
        #flash("Account already confirmed.", "success")
        return redirect(url_for("private/dashboard.html"))
    email = confirm_token(token)
    
    if session['user_email'] == email:
        confirm_user(email=email)
        session['confirmed'] = 1
        #flash("You have confirmed your account. Thanks!", "success")
        return redirect("private/dashboard.html")
    else:
        pass
        #flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("login.html"))



@auth_bp.route("/register", methods=["GET", "POST"])
#@logout_required
def register():
    from app.utils.communication.mailing import send_email

    if request.method == 'POST':
        in_email = request.form['email']        
        in_password = request.form['password']
        in_company = request.form['company']

        all_emails = []
        all_companies = []
        
        if in_password != request.form['password_confirmation']:
            return render_template("register.html",error="Passwords don't match")

        for x in fetch_all().users:
            all_emails.append(x.email)
            all_companies.append(x.company)

        try:
            all_emails.index(in_email)   
            # EMAIL IS ALREADY IN OUR DATABASE
            return render_template("register.html",error="This email has been used")         
        except ValueError:
            pass

        try:
            all_companies.index(in_company)
        except ValueError:
            # COMPANY IS NOT IN OUR DATABASE
            return render_template("register.html",error="This company is not registered")
        
        seeder(email=in_email,password=in_password,company=in_company)
    
        token = generate_token(in_email)
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)
        html = render_template("confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(in_email, subject, html)

        #flash("A confirmation email has been sent via email.", "success")
        return redirect(url_for("auth.login"),error="Check your inbox (spam folder) to confirm your account")

    return render_template("register.html")


