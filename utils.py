from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

def set_flash(request, message):
    request.session["flash"] = message