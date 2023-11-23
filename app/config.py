import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv("dev.env")

class Config:
    DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECRET_KEY_PERSONAL_TOKEN = os.getenv("SECRET_KEY_PERSONAL_TOKEN")
    SERVER_TOKEN = os.getenv("SERVER_TOKEN")

    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    MYSQL_PORT = 3306

    MYSQL_HOST_RAY = os.getenv("MYSQL_HOST_RAY")
    MYSQL_USER_RAY = os.getenv("MYSQL_USER_RAY")
    MYSQL_PASSWORD_RAY = os.getenv("MYSQL_PASSWORD_RAY")
    MYSQL_DB_RAY = os.getenv("MYSQL_DB_RAY")
    MYSQL_PORT_RAY = 3308

    SESSION_TYPE= os.getenv("SESSION_TYPE")
    SESSION_PERMANENT= False
    SESSION_USE_SIGNER=True

    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    OPENAI_KEY = os.getenv("OPENAI_KEY")

    PATH_DATAFRAMES = "app/database/dfs/"
    PATH_CRITICAL_DATA = "app/database/dfs/critical_data.parquet"
    PATH_CACHE_DASHBOARD = "app/database/cache/dashboard"
    PATH_CACHE_ANALYTICS = "app/database/cache/analytics"
    PATH_DASHBOARD_CONFIG = "app/utils/graph_functions/dashboard_config.json"
    PATH_ANALYTICS_CONFIG = "app/utils/graph_functions/analytics_config.json"
    PATH_BATTERY_PARAMS = "app/utils/DataframeManager/param_battery.json"

    template_folder="app/templates"
