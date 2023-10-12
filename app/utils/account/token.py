from itsdangerous import URLSafeTimedSerializer

from app.config import Config

def generate_token(email):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt=Config.SECRET_KEY)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(
            token, salt=Config.SECRET_KEY, max_age=expiration
        )
        return email
    except Exception:
        return False