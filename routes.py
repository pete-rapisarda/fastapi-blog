from fastapi import FastAPI, HTTPException, Request, Form, APIRouter
from storage import load_posts, save_posts, load_deleted_posts, save_deleted_posts
from fastapi.responses import HTMLResponse, RedirectResponse
from utils import templates, set_flash
from auth import users

posts = load_posts()
router = APIRouter()

@router.get("/",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"posts":posts})

@router.get("/create",response_class=HTMLResponse)
def create_form(request: Request,error:str=None,title:str="",content:str=""):
    return templates.TemplateResponse("create.html",{
        "request":request,
        "error":error,
        "title":title,
        "content":content
        })

@router.post("/create")
def create_post(request:Request,title:str = Form(...),content:str=Form(...)) -> RedirectResponse:
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

@router.get("/posts/{post_id}",response_class=HTMLResponse)
def read_post(post_id:int,request:Request):
    post = next((p for p in posts if p["id"] == post_id),None)
    if post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    return templates.TemplateResponse("post.html",{"request":request,"post":post})

@router.get("/posts/{post_id}/edit",response_class=HTMLResponse)
def edit_form(post_id:int,request:Request):
    post = next((p for p in posts if p["id"] == post_id),None)
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    return templates.TemplateResponse("edit.html",{
        "request":request,
        "post":post
    })

@router.post("/posts/{post_id}/edit")
def update_post(
    post_id:int,
    request:Request,
    title:str = Form(...),
    content:str = Form(...)
):
    if not title.strip() or not content.strip():
        post = next((p for p in posts if p["id"] == post_id),None)
        if not post:
            raise HTTPException(status_code=404,detail="Post not found")
        return templates.TemplateResponse(
            "edit.html",
            {
                "request":request,
                "post":post,
                "error":"Title and content cannot be empty"
            }
        )
    for post in posts:
        if post["id"] == post_id:
            post["title"] = title
            post["content"] = content
            save_posts(posts)
            break
    return RedirectResponse("/",status_code=303)

@router.post("/posts/{post_id}/delete")
def delete_post(post_id:int,request:Request) -> RedirectResponse:
    global posts
    post_to_delete = next((p for p in posts if p["id"] == post_id),None)
    if post_to_delete:
        posts = [p for p in posts if p["id"] != post_id]
        save_posts(posts)
        deleted = load_deleted_posts()
        deleted.append(post_to_delete)
        save_deleted_posts(deleted)
        set_flash(request,"Post archived successfully!")
    else:
        raise HTTPException(status_code=404, detail="Post not found")
    return RedirectResponse("/",status_code=303)

@router.get("/login",response_class=HTMLResponse)
def login_form(request:Request,error:str=None):
    return templates.TemplateResponse("login.html",{
        "request":request,
        "error":error
    })

@router.post("/login")
def login(request:Request,username:str = Form(...),password:str = Form(...)) -> RedirectResponse:
    stored_password = users.get(username)
    if stored_password is None or stored_password != password:
        return RedirectResponse(f"/login?error=invalid",status_code=303)
    else:
        request.session["username"] = username
        set_flash(request,"Login successful!  Welcome" + username + "!")
        return RedirectResponse(f"/",status_code=303)
    
@router.post("/logout")
def logout(request:Request) -> RedirectResponse:
    request.session.pop("username",None)
    set_flash(request,"Logout successfull")
    return RedirectResponse(f"/login",status_code=303)