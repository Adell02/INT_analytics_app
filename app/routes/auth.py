# auth.py
from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return "AUTH"
    return render_template('auth/login.html')

@auth_bp.route("/logout")
def logout():
    a = 2
    b = 3
    z = a+b
    return(str(z))