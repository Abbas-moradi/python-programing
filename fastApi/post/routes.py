from fastapi import APIRouter, HTTPException
from post.models import Post, PostUpdate
from database import posts, users, user_jwt
from user.utilse import decode_access_token

post_router = APIRouter(tags=["post"])


@post_router.post("/posts")
def add_post(post: Post):
    if post.author not in users.keys():
        raise HTTPException(404, "invalid author")
    if post.author not in user_jwt:
        raise HTTPException(422, "author not in login")
    posts[len(posts) + 1] = {
        "title": post.title,
        "content": post.content,
        "author": post.author,
    }
    return {"title": post.title, "content": post.content, "author": post.author}


@post_router.get("/posts")
def get_all_posts():
    list_post = []
    for value in posts.values():
        post_title = f"title: {value['title']}"
        post_content = f"content: {value['content']}"
        post_author = f"author: {value['author']}"
        list_post.append({post_title, post_content, post_author})
    return list_post


@post_router.get("/post/{id}")
def get_all_post(id: int):
    post = posts.get(id)
    if not post:
        raise HTTPException(404, "user not found")
    return {id: [posts[id]["title"], posts[id]["content"], posts[id]["author"]]}


@post_router.put("/post/{id}")
def update_post(id: int, update: PostUpdate):
    if not posts.get(id):
        raise HTTPException(404, detail="post does not exists")
    if not users.get(update.user_name):
        raise HTTPException(404, "user not found...")
    if not user_jwt.get(update.user_name):
        raise HTTPException(404, "user not found...")
    decode_token = decode_access_token(update.user_name, user_jwt.get(update.user_name))
    if decode_token[update.user_name] != "admin":
        raise HTTPException(422, "you are not update post, admin just a update post...")
    posts[id] = {"title": update.title, "content": update.content, "author": posts[id]['author']}
    return {id: "info changed successfully"}


@post_router.delete("/post/{id}")
def delete_post(id: int):
    if id not in posts.keys():
        raise HTTPException(404, detail="post does not exists")
    posts.pop(id)
    return {id: "post deleted successfully."}