from fastapi import FastAPI
import uvicorn
from user.routes import user_router
from post.routes import post_router


app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
