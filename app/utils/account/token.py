from itsdangerous import URLSafeTimedSerializer

from app.config import Config

def generate_token(parameter):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(parameter, salt=Config.SECRET_KEY)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        parameter = serializer.loads(
            token, salt=Config.SECRET_KEY, max_age=expiration
        )
        return parameter
    except Exception:
        return False
    
def generate_personal_token(parameter):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY_PERSONAL_TOKEN)
    return serializer.dumps(parameter, salt=Config.SECRET_KEY_PERSONAL_TOKEN)

def confirm_personal_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY_PERSONAL_TOKEN)
    try:
        parameter = serializer.loads(
            token, salt=Config.SECRET_KEY_PERSONAL_TOKEN, max_age=expiration
        )
        return parameter
    except Exception:
        return False