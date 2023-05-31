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


class UserLogout(BaseModel):
    user_name: str



class UserUpdate(BaseModel):
    user_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    user_roll: Optional[str]