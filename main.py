from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from storage import load_posts, save_posts

app = FastAPI()
templates = Jinja2Templates(directory="templates")

posts = load_posts()

@app.get("/",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"posts":posts})

@app.get("/create",response_class=HTMLResponse)
def create_form(request: Request,error:str=None,title:str="",content:str=""):
    return templates.TemplateResponse("create.html",{
        "request":request,
        "error":error,
        "title":title,
        "content":content
        })

@app.post("/create")
def create_post(request:Request,title:str = Form(...),content:str=Form(...)):
    if not title.strip() or not content.strip():
        return RedirectResponse(
            f"/create?error=missing&title={title}&content={content}",
            status_code=303
            )
    posts.append({
        "id":len(posts) + 1,
        "title":title,
        "content":content
        })
    save_posts(posts)
    return RedirectResponse("/",status_code=303)

@app.get("/posts/{post_id}",response_class=HTMLResponse)
def read_post(post_id:int,request:Request):
    post = next((p for p in posts if p["id"] == post_id),None)
    if post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    return templates.TemplateResponse("post.html",{"request":request,"post":post})
    if not post:
        return templates.TemplateResponse("404.html")