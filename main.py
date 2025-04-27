from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from storage import load_posts, save_posts, load_deleted_posts, save_deleted_posts
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

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

@app.exception_handler(404)
async def custom_404_handler(request: Request, exec: HTTPException):
    return templates.TemplateResponse("404.html",{"request":request},status_code=404)

@app.get("/posts/{post_id}/edit",response_class=HTMLResponse)
def edit_form(post_id:int,request:Request):
    post = next((p for p in posts if p["id"] == post_id),None)
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    return templates.TemplateResponse("edit.html",{
        "request":request,
        "post":post
    })

@app.post("/posts/{post_id}/edit")
def update_post(
    post_id:int,
    title:str = Form(...),
    content:str = Form(...)
):
    for post in posts:
        if post["id"] == post_id:
            post["title"] = title
            post["content"] = content
            save_posts(posts)
            break
    return RedirectResponse("/",status_code=303)

@app.post("/posts/{post_id}/delete")
def delete_post(post_id:int,request:Request):
    global posts
    post_to_delete = next((p for p in posts if p["id"] == post_id),None)
    if post_to_delete:
        posts = [p for p in posts if p["id"] != post_id]
        save_posts(posts)
        deleted = load_deleted_posts()
        deleted.append(post_to_delete)
        save_deleted_posts(deleted)
        request.session["flash"] = "Post archived successfully!"
    else:
        raise HTTPException(status_code=404, detail="Post not found")
    return RedirectResponse("/",status_code=303)
