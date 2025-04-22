import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .crud import init_db, save_password, get_passwords

load_dotenv()  # Optional for local development

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    passwords = await get_passwords()
    return templates.TemplateResponse("index.html", {"request": request, "passwords": passwords})

@app.post("/add")
async def add_password(website: str = Form(...), username: str = Form(...), password: str = Form(...)):
    await save_password(website, username, password)
    return {"message": "Password saved!"}
