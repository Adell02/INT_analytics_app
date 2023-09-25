from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)    
    
    db.init_app(app)  
    from app.database.models import User
    with app.app_context():
        db.create_all()

    # Import and register Blueprint(s)
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.dash import dash_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dash_bp, url_prefix='/private')

    return app