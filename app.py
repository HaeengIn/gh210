from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from functions import *

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

supabaseUrl = os.getenv("SUPABASE_URL")
supabaseKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabaseUrl, supabaseKey)

@app.get("/")
def index(request: Request):
    ddayMessages = dday(supabase)
    meal = getMeal()
    timeTable = getTimeTable()
    schedule = getSchedule()

    return templates.TemplateResponse("index.html", {"request": request, "ddayMessages": ddayMessages, "meal": meal, "timeTable": timeTable, "schedule": schedule})

@app.get("/notice")
def notice(request: Request):
    return templates.TemplateResponse("notice.html", {"request": request})

@app.get("/{subject}")
def cloud_subject(request: Request, subject: str):
    valid_subjects = ["bio", "chem", "earth", "eng", "essay", "ethic", "gram", "jp", "kor", "math", "music", "pe", "phys", "stat"]
    if subject not in valid_subjects:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse(f"cloud/{subject}.html", {"request": request})

@app.get("/complain")
def complain(request: Request):
    response = supabase.table("complain").select("*").execute()
    posts = response.data

    return templates.TemplateResponse("complain.html", {"request": request, "posts": posts})

@app.get("/complain/{post_id}")
def complainPost(request: Request, post_id: int):
    response = supabase.table("complain").select("*").eq("id", post_id).single().execute()
    post = response.data

    return templates.TemplateResponse("posts.html", {"request": request, "post": post})