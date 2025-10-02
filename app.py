from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from functions import *
import asyncio

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@app.get("/")
async def index(request: Request):
    loop = asyncio.get_event_loop()
    ddayMessages = await loop.run_in_executor(None, dday, supabase)
    meal, timeTable, schedule = await asyncio.gather(
        loop.run_in_executor(None, getMeal),
        loop.run_in_executor(None, getTimeTable),
        loop.run_in_executor(None, getSchedule)
    )
    return templates.TemplateResponse("index.html", {"request": request, "ddayMessages": ddayMessages, "meal": meal, "timeTable": timeTable, "schedule": schedule})

@app.get("/notice")
async def notice(request: Request):
    return templates.TemplateResponse("notice.html", {"request": request})

@app.get("/complain")
async def complain(request: Request):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, supabase.table("posts").select("*").order("id", desc=True).execute)
    posts = response.data
    for p in posts:
        dt = datetime.fromisoformat(p['created_at'].replace("Z", "+00:00"))
        p['created_at'] = dt.strftime("%Y-%m-%d")
    for s in posts:
        st = s['status']
        if st == 0:
            s['status'] = "대기"
        elif st == 1:
            s['status'] = "완료"
        elif st == 2:
            s['status'] = "공지"
    return templates.TemplateResponse("complain.html", {"request": request, "posts": posts})

@app.get("/complain/{id}")
async def complainPost(request: Request, id: int):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, supabase.table("posts").select("*").eq("id", id).single().execute)
    post = response.data
    return templates.TemplateResponse("posts.html", {"request": request, "post": post})

@app.get("/write")
async def write(request: Request):
    return templates.TemplateResponse("write.html", {"request": request})

@app.post("/write")
async def writePost(request: Request, title: str = Form(...), content: str = Form(...)):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, supabase.table("posts").insert({"title": title, "content": content, "status": 0}).execute)
    newPost = response.data[0]
    newId = newPost["id"]
    return RedirectResponse(url="/complain", status_code=303)

@app.get("/{subject}")
async def cloud_subject(request: Request, subject: str):
    valid_subjects = ["bio", "chem", "earth", "eng", "essay", "ethic", "gram", "jp", "kor", "math", "music", "pe", "phys", "stat"]
    if subject not in valid_subjects:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse(f"cloud/{subject}.html", {"request": request})