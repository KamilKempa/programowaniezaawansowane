from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
import models
from database import engine, Base, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_weekend(date_str: str):
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    return d.weekday() >= 5


@app.get("/")
def root():
    return{"fastapi dziala": True}

@app.post("/currencies/fetch")
def fetch_currencies(date: str = None,db: Session = Depends(get_db)):

    if date and is_weekend(date):
        raise HTTPException(
            status_code=400,
            detail="Gielda zamknieta w soboty i niedziele"
        )

    if date:
        url = f"https://api.nbp.pl/api/exchangerates/tables/A/{date}/?format=json"
    else:
        url = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"

    response = requests.get(url)
    data = response.json()[0]

    rates = data["rates"]
    parsed_date = datetime.strptime(data["effectiveDate"], "%Y-%m-%d").date()

    db.query(models.CurrencyRate).filter(
        models.CurrencyRate.date == parsed_date
    ).delete()

    saved = []

    for r in rates:
        db_rate = models.CurrencyRate(
            code=r["code"],
            currency=r["currency"],
            mid=r["mid"],
            date=parsed_date
        )
        db.add(db_rate)
        saved.append({
            "code": r["code"],
            "currency": r["currency"],
            "mid": r["mid"],
            "date": parsed_date
        })

    db.commit()

    return {
        "message": "dane zostaly zapisane",
        "count": len(saved),
        "rates":saved
    }

#get kursow walut z bazy danych

@app.get("/currencies")
def get_currencies(date: str = None, code: str = None,db: Session = Depends(get_db)):
    query = db.query(models.CurrencyRate)

    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        query = query.filter(models.CurrencyRate.date == date_obj)
    if code:
        query = query.filter(models.CurrencyRate.code == code)

    data = query.all()

    return[
        {
            "code": d.code,
            "currency": d.currency,
            "mid": d.mid,
            "date": d.date
        }
        for d in data
    ]

@app.get("/currencies/range")
def get_range(start: str, end: str):
    url = f"https://api.nbp.pl/api/exchangerates/tables/A/{start}/{end}/?format=json"

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Brak danych"}

    tables = response.json()
    result = {}

    for table in tables:
        for rate in table["rates"]:

            code = rate["code"]

            if code not in result:
                result[code] = {
                    "code": code,
                    "currency": rate["currency"],
                    "sum": 0,
                    "count": 0
                }

            result[code]["sum"] += rate["mid"]
            result[code]["count"] += 1

    return [
        {
            "code": v["code"],
            "currency": v["currency"],
            "mid": round(v["sum"] / v["count"], 4)
        }
        for v in result.values()
    ]

@app.get("/currencies/year/{year}")
def get_year(year: int):

    ranges = [
        (f"{year}-01-01", f"{year}-03-31"),
        (f"{year}-04-01", f"{year}-06-30"),
        (f"{year}-07-01", f"{year}-09-30"),
        (f"{year}-10-01", f"{year}-12-31"),
    ]

    result = {}

    for start, end in ranges:

        url = f"https://api.nbp.pl/api/exchangerates/tables/A/{start}/{end}/?format=json"

        response = requests.get(url)

        if response.status_code != 200:
            continue

        tables = response.json()

        for table in tables:
            for rate in table["rates"]:

                code = rate["code"]

                if code not in result:
                    result[code] = {
                        "code": code,
                        "currency": rate["currency"],
                        "sum": 0,
                        "count": 0
                    }

                result[code]["sum"] += rate["mid"]
                result[code]["count"] += 1

    return [
        {
            "code": v["code"],
            "currency": v["currency"],
            "mid": round(v["sum"] / v["count"], 4)
        }
        for v in result.values()
    ]

@app.get("/currencies/month/{year}/{month}")
def get_month(year: int, month: int):

    if month == 12:
        end = f"{year}-12-31"
    else:
        end = f"{year}-{month+1:02d}-01"

    start = f"{year}-{month:02d}-01"

    return get_range(start, end)

@app.get("/currencies/quarter/{year}/{quarter}")
def get_quarter(year: int, quarter: int):

    quarters = {
        1: ("01-01", "03-31"),
        2: ("04-01", "06-30"),
        3: ("07-01", "09-30"),
        4: ("10-01", "12-31")
    }

    start, end = quarters[quarter]

    return get_range(
        f"{year}-{start}",
        f"{year}-{end}"
    )