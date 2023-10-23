from flask import Flask,url_for,redirect,session
from flask_mail import Mail
from flask_session import Session
import mysql.connector
import openai

from app.config import Config
from app.utils.AI.openai_request import test


conn = None
cursor = None
mail = None

def create_app(config_class=Config):
    global conn,cursor,mail
    
    app = Flask(__name__)
    app.config.from_object(config_class) 

    Session(app)   
    mail = Mail(app)
    
    
    db_config= {
    'host':app.config["MYSQL_HOST"],
    'user':app.config["MYSQL_USER"],
    'password':app.config["MYSQL_PASSWORD"],
    'database':app.config["MYSQL_DB"]
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(buffered=True,dictionary=True)

    openai.api_key = Config.OPENAI_KEY
    #test()

    # Import and register Blueprint(s)
    from app.routes.auth import auth_bp
    from app.routes.dash import dash_bp
    from app.routes.settings import settings_bp
    from app.database.seeder import seeder_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(settings_bp,url_prefix="/private")
    app.register_blueprint(dash_bp, url_prefix='/private')
    app.register_blueprint(seeder_bp)

    @app.route("/")
    def redirect_home():
        return redirect(url_for("dash.dashboard"))
    
    @app.context_processor
    def global_variables():
        return{'session':session}
    return app