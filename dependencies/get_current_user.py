# Imports
from models.Users import User

def get_current_user_from_jwt(user: dict , db):
    current_user = db.query(User).filter(User.email == user["user_email"]).first()
    if not current_user:
        return False
    return current_user