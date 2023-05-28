from hashlib import sha256
from datetime import datetime, timedelta
from typing import Any, Union
import jwt


def hash_pass(password):
    return sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_pass: str) -> bool:
    return hash_pass(password) == hashed_pass


def create_access_token(subject: Union[str, Any] = None, expires_delta: int = 30):
    key = "abbas"  # the secret key
    roll = {"user": "regular"}
    encoded = jwt.encode(roll, key, algorithm="HS256")
    return encoded


def decode_access_token(user_name: str = None, token: str = None):
    encoded = token
    key = "abbas"  # the secret key
    token_decode = jwt.decode(encoded, key, algorithms="HS256")
    return token_decode