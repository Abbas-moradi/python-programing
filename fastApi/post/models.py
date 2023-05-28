from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    author: str


class PostUpdate(BaseModel):
    user_name: str
    title: str
    content: str
