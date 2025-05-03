from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.utils.config import settings
import uuid
import logging

pwd_context = CryptContext(schemes=['bcrypt'])


# Hash Password
def generate_password_hash(password:str) -> str:
    hash = pwd_context.hash(password)
    return hash

# Verify password with hash
def verify_password(password: str, hash:str) -> bool:
    return pwd_context.verify(password,hash)


# The token function
def create_access_token(user_data:dict, refresh:bool=False) -> str:
    
    payload = {
        'user_data':user_data,
        'exp': datetime.now() + timedelta(minutes=settings.access_token_expire_minutes),
        'jti': str(uuid.uuid4()),
        'refresh':refresh
    }
    
    token = jwt.encode(payload=payload,key=settings.secret_key, algorithm=settings.algorithm)
    
    return token


def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(jwt=token, key=settings.secret_key, algorithms=settings.algorithm)
        
        return token_data
    
    except jwt.PyJWTError as jwte:
        logging.exception(jwte)
        return None
    
    except Exception as e:
        logging.exception(e)
        return None