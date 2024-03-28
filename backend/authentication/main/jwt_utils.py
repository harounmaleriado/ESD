import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_jwt_token(user_id):
    payload = {
        'sub': user_id,
        'iss': current_app.config['JWT_ISSUER'],
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1),  # 1 day validity
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token.decode('utf-8') if isinstance(token, bytes) else token

def decode_jwt_token(token):
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
