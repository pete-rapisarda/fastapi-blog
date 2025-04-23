from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

posts = [
    {"id":1,"title":"Hello World","content":"This is your first blog post."},
    {"id":2,"title":"FastAPI Rocks","content":"Building with FastAPI is fun and fast!"}
]

@app.get("/create",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"posts":posts})

@app.post("/",response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("create.html",{"request":request})

@app.post("/create")
def create_post(request: Request,title: str = Form(...),content:str=Form(...)):
    posts.append({"id":len(posts) + 1, "title":title, "content":content})
    return RedirectResponse("/",status_code="303")