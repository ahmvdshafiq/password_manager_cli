from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .crud import save_password, get_passwords, init_db

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

init_db()

@app.get("/")
def read_root(request: Request):
    passwords = get_passwords()
    return templates.TemplateResponse("index.html", {"request": request, "passwords": passwords})

@app.post("/add")
def add_password(site: str = Form(...), username: str = Form(...), password: str = Form(...)):
    save_password(site, username, password)
    return RedirectResponse("/", status_code=303)
