from pydantic import BaseModel
from typing import Optional
from enum import Enum


class RollUser(Enum):
    admin = 'admin'
    regular = 'regular'


class UserIn(BaseModel):
    user_name: str
    email: str
    password: str
    roll: RollUser = RollUser.regular


class UserLogin(BaseModel):
    user_name: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]