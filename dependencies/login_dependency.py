# Imports
from models.Users import User
from utils.bcrypt_util import bcrypt_context

def authenticate_user(email: str , password: str , db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
       return False
    if not bcrypt_context.verify(password , user.password):
        return False
    if not user.is_verified:
        return False
    return user
    