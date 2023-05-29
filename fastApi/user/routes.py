from fastapi import APIRouter, HTTPException
from user.models import UserIn, UserUpdate, UserLogin
from database import users, user_jwt, sessions
from user.utilse import hash_pass, verify_password, create_access_token, create_session

user_router = APIRouter(tags=['user'])


@user_router.post("/users")
def add_user(user: UserIn):
    if user.user_name in users.keys():
        raise HTTPException(403, "the user name has been exists")
    for item in users.values():
        if item["email"] == user.email:
            raise HTTPException(403, "the email has been exists")
    users[user.user_name] = {'email' : user.email, 'password': hash_pass(user.password), 'roll': user.roll}
    return {user.user_name: 'user created successfully'}


@user_router.post('/login')
def login_user(user: UserLogin):
    if user.user_name not in users.keys():
        raise HTTPException(404, "username or password invalid")
    if not verify_password(user.password, users[user.user_name]['password']):
        raise HTTPException(404, "username or password invalid")
    
    roll = next((users[_user]['roll'] for _user in users.keys() if _user == user.user_name), None)

    token = create_access_token(user.user_name, roll, create_session(user.user_name))
    user_jwt[user.user_name] = token
    return {user.user_name: "token created..."}


@user_router.get("/users")
def get_all_users():
    list_user = []
    for key, value in users.items():
        user_show = f"user name: {key}"
        email_show = f"email: {value['email']}"
        list_user.append({user_show: email_show})
    return list_user


@user_router.get("/users/{username}")
def get_user_by_name(username: str):
    user = users.get(username)
    if user: 
        return {username: users[username]['email']}
    else: 
        HTTPException(404, 'user not found')
        

@user_router.put("/users/{username}")
def update_user(username: str, update:UserUpdate):
    if not users.get(username):
        raise HTTPException(404, detail='user does not exists')
    users[username] = {'email': update.email, 'password': update.password}
    return {username: 'info changed successfully'}


@user_router.delete("/user/{username}")
def delete_user(username: str):
    if username not in users.keys():
        raise HTTPException(404, detail='user does not exists')
    users.pop(username)
    return {username: 'user deleted successfully.'}


@user_router.get("/token")
def get_all_token():
    repo = []
    for item in user_jwt.items():
        repo.append(item)
    return repo

@user_router.get("/session")
def get_all_session():
    repo = []
    for item in sessions.items():
        repo.append(item)
    return repo