from fastapi import APIRouter, HTTPException, Depends
from user.models import UserIn, UserUpdate, UserLogin, UserLogout
from database import users, user_jwt, sessions
from user.utilse import hash_pass, verify_password, create_access_token, create_session, decode_access_token
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

user_router = APIRouter(tags=['user'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/")


@user_router.post("/users")
def add_user(user: UserIn , token: str = Depends(oauth2_scheme)):
    if user.user_name in users.keys():
        raise HTTPException(403, "the user name has been exists")
    for item in users.values():
        if item["email"] == user.email:
            raise HTTPException(403, "the email has been exists")
    users[user.user_name] = {'email' : user.email, 'password': hash_pass(user.password), 'roll': user.roll}
    return {user.user_name: 'user created successfully'}


@user_router.post('/login')
def login_user(user: UserLogin, token: str = Depends(oauth2_scheme)):
    if user.user_name not in users.keys():
        raise HTTPException(404, "username or password invalid")
    if not verify_password(user.password, users[user.user_name]['password']):
        raise HTTPException(404, "username or password invalid")
    if user.user_name in user_jwt:
        raise HTTPException(422, "The user is already logged in")
    
    roll = next((users[_user]['roll'] for _user in users.keys() if _user == user.user_name), None)

    token = create_access_token(user.user_name, roll, create_session(user.user_name))
    user_jwt[user.user_name] = token
    return {user.user_name: "token created..."}


@user_router.post('/log_out')
def logout_user(user: UserLogout):
    if user.user_name not in users:
        raise HTTPException(404, 'user not found...')
    user_jwt.pop(user.user_name)
    return {user.user_name: "log out..."}


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
        return {
            'User Name': username,
            'Email': users[username]['email'],
            'User Roll': users[username]['roll']
            }
    else: 
        HTTPException(404, 'user not found')
        

@user_router.put("/users/{username}")
def update_user(admin: str, update:UserUpdate):
    if not users.get(admin):
        raise HTTPException(404, detail='admin does not exists')
    if not user_jwt.get(admin):
        raise HTTPException(404, detail='admin not loging...')
    decode_token = decode_access_token(update.user_name, user_jwt.get(admin))
    login_time = datetime.strptime(decode_token['login_time'], "%Y-%m-%d %H:%M:%S.%f")
    if login_time + timedelta(seconds=decode_token['expire_time']) < datetime.now():
        user_jwt.pop(admin)
        raise HTTPException(422, 'Token is expire...')
    if "admin" not in decode_token[admin]:
        raise HTTPException(422, f"The user {admin} is not an admin")
    if not users.get(update.user_name):
        raise HTTPException(404, detail='user does not exists')
    
    users[update.user_name] = {'email': update.email, 'password': update.password, 'user_roll': update.user_roll}
    return {update.user_name: 'info changed successfully'}


@user_router.delete("/user/{username}")
def delete_user(username: str, admin: str):
    if not users.get(admin):
        raise HTTPException(404, detail='admin does not exists')
    if not user_jwt.get(admin):
        raise HTTPException(404, detail='admin not loging...')
    decode_token = decode_access_token(username, user_jwt.get(admin))
    login_time = datetime.strptime(decode_token['login_time'], "%Y-%m-%d %H:%M:%S.%f")
    if login_time + timedelta(seconds=decode_token['expire_time']) < datetime.now():
        user_jwt.pop(admin)
        raise HTTPException(422, 'Token is expire...')
    if "admin" not in decode_token[admin]:
        raise HTTPException(422, f"The user {admin} is not an admin")
    if not users.get(username):
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