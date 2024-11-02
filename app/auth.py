# app/auth.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from .models import User

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)

def generate_token(identity):
    return create_access_token(identity=identity, expires_delta=timedelta(days=7))

