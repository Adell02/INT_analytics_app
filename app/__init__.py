from flask import Flask,url_for,redirect,session
from flask_mail import Mail
from flask_session import Session
import openai

from app.config import Config


conn = None
cursor = None
conn_ray = None
cursor_ray = None
mail = None

def create_app(config_class=Config):
    global mail
    
    app = Flask(__name__)
    app.config.from_object(config_class) 

    Session(app)   
    mail = Mail(app)

    openai.api_key = Config.OPENAI_KEY
    
    # Import and register Blueprint(s)
    from app.routes.auth import auth_bp
    from app.database.seeder import seeder_bp
    from app.routes.RESTful_API import api_bp

    from app.routes.dash import dash_bp
    from app.routes.newgraphic import newgraphic_bp
    from app.routes.analytics import analytics_bp
    from app.routes.mapview import mapview_bp
    from app.routes.ai_chat import ai_chat_bp
    from app.routes.settings import settings_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(seeder_bp)
    app.register_blueprint(api_bp)

    app.register_blueprint(dash_bp, url_prefix='/private')
    app.register_blueprint(newgraphic_bp, url_prefix='/private')
    app.register_blueprint(analytics_bp, url_prefix='/private')
    app.register_blueprint(mapview_bp, url_prefix='/private')
    app.register_blueprint(ai_chat_bp, url_prefix='/private')
    app.register_blueprint(settings_bp,url_prefix="/private")
    
    @app.route("/")
    def redirect_home():
        return redirect(url_for("dash.dashboard"))
    
    @app.context_processor
    def global_variables():
        return{'session':session}        
    return app