from flask import Flask
import mysql.connector

from app.config import Config

conn = None
cursor = None

def create_app(config_class=Config):
    global conn,cursor
    print(Config.MYSQL_HOST)
    app = Flask(__name__)
    app.config.from_object(config_class)    
    
    db_config= {
    'host':app.config["MYSQL_HOST"],
    'user':app.config["MYSQL_USER"],
    'password':app.config["MYSQL_PASSWORD"],
    'database':app.config["MYSQL_DB"]
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Import and register Blueprint(s)
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.dash import dash_bp
    from app.database.seeder import seeder_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dash_bp, url_prefix='/private')
    app.register_blueprint(seeder_bp)
    return app

