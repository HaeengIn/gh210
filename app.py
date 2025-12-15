from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from starlette.responses import JSONResponse, Response
from routers.complain import complain_router
from routers.school import school_router
from supabase import create_client, Client
from dotenv import load_dotenv
from functions import *
import os, asyncio, importlib.util

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
    theme = request.cookies.get("theme", "")
    return templates.TemplateResponse("index.html", {"request": request, "theme": theme})

@app.route("/set_theme", methods=["POST"])
async def set_theme(request: Request):
    data = await request.json()
    theme = data.get("theme", "light")
    response = JSONResponse(content={"status": "ok", "theme": theme})
    response.set_cookie(key="theme", value=theme, max_age=60*60*24*30, httponly=False, samesite="Lax")
    return response

app.include_router(school_router)
app.include_router(complain_router)

@app.get("/{subject}")
async def cloud_subject(request: Request, subject: str):
    theme = request.cookies.get("theme", "light")
    valid_subjects = ["bio", "chem", "earth", "eng", "essay", "ethic", "gram", "jp", "kor", "math", "music", "pe", "phys", "stat"]
    if subject not in valid_subjects:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse(f"cloud/{subject}.html", {"request": request, "subject": subject, "theme": theme})