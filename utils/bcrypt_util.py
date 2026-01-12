# Imports
from passlib.context import CryptContext
import secrets

bcrypt_context = CryptContext(schemes=['argon2'], deprecated='auto')

def generate_otp():
    return str(secrets.randbelow(900000)+100000)

def hash_otp(otp: str):
    return bcrypt_context.hash(otp)

def verify_otp(plain_otp: str , hashed_otp: str):
    return bcrypt_context.verify(plain_otp,hashed_otp)