import jwt
from flask import current_app

def generate_jwt(data):
    return jwt.encode(data, current_app.config['SECRET_KEY'], algorithm='HS256')

def decode_jwt(token):
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
