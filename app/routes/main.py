# main.py
from flask import Blueprint, render_template
from app import db  # To add new rows to the DB (not needed)
from app.database.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    #Example adding to DB with SQLAlchemy
    #new_item = User(email="test@gmail.com",password="password")
    #db.session.add(new_item)
    #db.session.commit()
    
    users = User.query.all()
    return(str(users))
    return render_template('main/index.html')
