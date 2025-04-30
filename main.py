from fastapi import FastAPI, HTTPException, Request
from routes import router
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from utils import templates
import os
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise ValueError("SECRET_KEY environment variable not set")

app = FastAPI()
app.include_router(router)
app.add_middleware(SessionMiddleware, secret_key=secret_key)

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html",{"request":request},status_code=404)