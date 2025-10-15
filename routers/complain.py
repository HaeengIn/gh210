from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Form
import os, asyncio
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

templates = Jinja2Templates(directory="templates")
complain_router = APIRouter()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@complain_router.get("/complain")
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

@complain_router.get("/complain/{id}")
async def complainPost(request: Request, id: int):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, supabase.table("posts").select("*").eq("id", id).single().execute)
    post = response.data
    return templates.TemplateResponse("posts.html", {"request": request, "post": post})

@complain_router.get("/write")
async def write(request: Request):
    return templates.TemplateResponse("write.html", {"request": request})

@complain_router.post("/write")
async def writePost(request: Request, title: str = Form(...), content: str = Form(...)):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, supabase.table("posts").insert({"title": title, "content": content, "status": 0}).execute)
    newPost = response.data[0]
    newId = newPost["id"]
    return RedirectResponse(url="/complain", status_code=303)