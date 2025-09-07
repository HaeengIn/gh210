from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import date, datetime

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

supabaseUrl = os.getenv("SUPABASE_URL")
supabaseKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabaseUrl, supabaseKey)

@app.get("/")
def index(request: Request):
    # 당일 날짜 불러오기
    today = date.today()

    # 수행평가 데이터 불러오기
    performance = supabase.table("performance").select("subject", "date").execute()
    performanceList = performance.data or []

    # D-Day 그룹화
    ddayGroups: dict[int, list[str]] = {}
    for item in performanceList:
        dateStr = item.get("date")
        subject = item.get("subject")
        if not date:
            continue
        
        # 날짜 형식 변환
        try:
            performanceDate = date.fromisoformat(dateStr)
        except Exception:
            try:
                performanceDate = datetime.strptime(dateStr, "%Y-%m-%d").date()
            except Exception:
                continue

        # D-Day 계산
        dday = (performanceDate - today).days
        if 0 <= dday <= 7:
            ddayGroups.setdefault(dday, []).append(subject)

    # D-Day 메시지 생성
    ddayMessages: list[str] = []
    for d in sorted(ddayGroups.keys()):
        subjects = [s for s in ddayGroups[d] if s]
        if not subjects:
            continue
        subjectStr = ", ".join(subjects)
        if d == 0:
            message = f"<b>오늘</b>은 {subjectStr} 수행평가가 실시되는 날입니다!"
        elif d == 1:
            message = f"{subjectStr} 수행평가가 실시되기까지 <b>1일</b> 남았습니다!"
        else:
            message = f"{subjectStr} 수행평가가 실시되기까지 <b>{d}일</b> 남았습니다!"
        ddayMessages.append(message)

    return templates.TemplateResponse("index.html", {"request": request, "ddayMessages": ddayMessages})

@app.get("/notice")
def notice(request: Request):
    return templates.TemplateResponse("notice.html", {"request": request})

@app.get("/{subject}")
def cloud_subject(request: Request, subject: str):
    valid_subjects = ["bio", "chem", "earth", "eng", "essay", "ethic", "gram", "jp", "kor", "math", "music", "pe", "phys", "stat"]
    if subject not in valid_subjects:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse(f"cloud/{subject}.html", {"request": request})