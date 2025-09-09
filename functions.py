from datetime import date, datetime
from supabase import Client

def dday(supabase: Client):
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
        if not dateStr:
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

    return ddayMessages

def getMeal():
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()

    mealToday = datetime.now().strftime("%Y%m%d")
    baseUrl = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    params = {
        "KEY": os.getenv("neisApi"),
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "ATPT_OFCDC_SC_CODE": "J10",
        "SD_SCHUL_CODE": "7530774",
        "MLSV_YMD": mealToday,
    }

    response = requests.get(baseUrl, params=params)
    data = response.json()

    try:
        meal = data["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        return meal.replace("<br/>", "\n")
    except Exception:
        return "오늘의 급식 정보가 없습니다."