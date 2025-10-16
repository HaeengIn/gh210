from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.routing import APIRouter
from routers.complain import complain_router
from starlette.responses import Response
from supabase import create_client, Client
import os, asyncio, importlib.util
from dotenv import load_dotenv
from functions import *

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class CachedStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response: Response = await super().get_response(path, scope)
        if response.status_code == 200:
            if path.endswith(".html"):
                response.headers["Cache-Control"] = "public, max-age=1209600"
            else:
                response.headers["Cache-Control"] = "public, max-age=10368000, immutable"
        return response

app.mount("/static", CachedStaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware, minimum_size=500)

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@app.get("/")
async def index(request: Request):
    loop = asyncio.get_event_loop()
    ddayMessages = await loop.run_in_executor(None, dday, supabase)
    return templates.TemplateResponse("index.html", {"request": request, "ddayMessages": ddayMessages})

@app.get("/school")
async def school(request: Request):
    loop = asyncio.get_event_loop()
    meal, timeTable, schedule = await asyncio.gather(
        loop.run_in_executor(None, getMeal),
        loop.run_in_executor(None, getTimeTable),
        loop.run_in_executor(None, getSchedule)
    )
    return templates.TemplateResponse("school.html", {"request": request, "meal": meal, "timeTable": timeTable, "schedule": schedule})

app.include_router(complain_router)

@app.get("/{subject}")
async def cloud_subject(request: Request, subject: str):
    valid_subjects = ["bio", "chem", "earth", "eng", "essay", "ethic", "gram", "jp", "kor", "math", "music", "pe", "phys", "stat"]
    if subject not in valid_subjects:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse(f"cloud/{subject}.html", {"request": request})