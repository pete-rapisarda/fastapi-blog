from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")

def set_flash(request:Request, message:str) -> None:
    request.session["flash"] = message

def require_login(request:Request) -> RedirectResponse:
    if "username" not in request.session:
        return RedirectResponse(
            f"/login?error=unauthorized",status_code=303
        )