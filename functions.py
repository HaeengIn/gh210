from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import requests, os

KST = ZoneInfo("Asia/Seoul")
load_dotenv()
KEY = os.getenv("neisApi")

def base_params():
    return {
        "KEY": KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "ATPT_OFCDC_SC_CODE": "J10",
        "SD_SCHUL_CODE": "7530774",
    }

def getMeal():
    mealToday = datetime.now(KST).strftime("%Y%m%d")
    baseUrl = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    params = base_params()
    params.update({
        "MLSV_YMD": mealToday,
    })

    response = requests.get(baseUrl, params=params)
    data = response.json()

    try:
        meal = data["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        return meal.replace("<br/>", "\n")
    except Exception:
        return "오늘의 급식 정보가 없습니다."

def getTimeTable():
    dayOfWeek = datetime.now(KST).weekday()
    if dayOfWeek >= 5:
        return "오늘은 수업이 없습니다."

    baseUrl = "https://open.neis.go.kr/hub/hisTimetable"
    params = base_params()
    params.update({
        "ALL_TI_YMD": datetime.now().strftime("%Y%m%d"),
        "GRADE": 2,
        "CLASS_NM": "10",
    })

    response = requests.get(baseUrl, params=params)
    data = response.json()

    try:
        timetableData = data["hisTimetable"][1]["row"]
        timetable = ["<b>[오늘의 시간표]</b>\n"]
        for entry in sorted(timetableData, key=lambda x: x["PERIO"]):
            period = entry["PERIO"]
            subject = entry["ITRT_CNTNT"]
            timetable.append(f"{period}교시: {subject}")
        return "\n".join(timetable)
    except Exception:
        return "오늘의 시간표 정보가 없습니다."
    
def getSchedule():
    baseUrl = "https://open.neis.go.kr/hub/SchoolSchedule"
    params = base_params()
    params.update({
        "AA_YMD": datetime.now(KST).strftime("%Y%m%d"),
    })

    response = requests.get(baseUrl, params=params)
    data = response.json()

    try:
        scheduleData = data["SchoolSchedule"][1]["row"]
        schedule = ["<b>[오늘의 학교 일정]</b>\n"]
        for entry in scheduleData:
            eventName = entry["EVENT_NM"]
            schedule.append(f"- {eventName}")
        return "\n".join(schedule)
    except Exception:
        return "오늘의 학교 일정 정보가 없습니다."