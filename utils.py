from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

def set_flash(request:Request, message:str) -> None:
    request.session["flash"] = message