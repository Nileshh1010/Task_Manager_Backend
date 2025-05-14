import jwt
from flask import current_app

def generate_jwt(data):
    return jwt.encode(data, current_app.config['SECRET_KEY'], algorithm='HS256')

def decode_jwt(token):
    try:
        # Remove "Bearer " if it's part of the token string
        token = token.replace("Bearer ", "")
        
        # Decode the JWT token and return the payload
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None  # or return a more specific error if you need
    except jwt.InvalidTokenError:
        return None  # or return a more specific error if you need

