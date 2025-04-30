from fastapi import FastAPI
from routes import router
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise ValueError("SECRET_KEY environment variable not set")


app = FastAPI()
app.include_router(router)
app.add_middleware(SessionMiddleware, secret_key=secret_key)

