from hashlib import sha256
from datetime import datetime, timedelta
from typing import Any, Union
import jwt
import secrets
from database import sessions, secret_key


def hash_pass(password):
    return sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_pass: str) -> bool:
    return hash_pass(password) == hashed_pass


def create_access_token(user_name: str = None, roll: str = None, session: dict = None):
    key = secret_key  # the secret key
    auth = {user_name: roll, "session": session}
    encoded = jwt.encode(auth, key, algorithm="HS256")
    return encoded


def decode_access_token(user_name: str = None, token: str = None):
    encoded = token
    key = secret_key  # the secret key

    token_decode = jwt.decode(encoded, key, algorithms="HS256")
    
    return token_decode


def create_session(username: str) -> str:
    session_id = secrets.token_hex(16)  # Generate a random session ID
    login_time = datetime.now()  # Get the current login time
    
    session_data = {
        "username": username,
        "login_time": login_time,
    }
    
    sessions[session_id] = session_data  # Store the session data in the fake database by sessions
    
    return session_id