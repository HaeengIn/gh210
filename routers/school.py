from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from functions import get_meal, get_timetable, get_schedule
import asyncio

templates = Jinja2Templates(directory="templates")
school_router = APIRouter()

@school_router.get("/meal")
async def meal(request: Request):
    loop = asyncio.get_event_loop()
    meal = await asyncio.gather(loop.run_in_executor(None, get_meal))
    return templates.TemplateResponse("school/meal.html", {"request": request, "meal": meal})

@school_router.get("/timetable")
async def meal(request: Request):
    loop = asyncio.get_event_loop()
    timetable = await asyncio.gather(loop.run_in_executor(None, get_timetable))
    return templates.TemplateResponse("school/timetable.html", {"request": request, "timetable": timetable})

@school_router.get("/schedule")
async def meal(request: Request):
    loop = asyncio.get_event_loop()
    schedule = await asyncio.gather(loop.run_in_executor(None, get_schedule))
    return templates.TemplateResponse("school/schedule.html", {"request": request, "schedule": schedule})