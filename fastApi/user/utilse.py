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


    # the follow cod with decod token for test

    # encoded = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9
    # .lyeiqhev9lfuwQsCEtcvLjHj2CjHFeyqqmyBUznBPdc'
    # token = jwt.decode(encoded, key, algorithms="HS256")

    return encoded
