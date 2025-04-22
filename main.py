from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

posts = [
    {"id":1,"title":"Hello World","content":"This is your first blog post."},
    {"id":2,"title":"FastAPI Rocks","content":"Building with FastAPI is fun and fast!"}
]

@app.get("/",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"posts":posts})