from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import requests
import models
from database import engine, Base, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return{"route works"}

@app.post("/currencies/fetch")
def fetch_currencies(date: str = None,db: Session = Depends(get_db)):

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

# NIE WYKORZYSTANE

# parametr path http://localhost:8000/currency/PLN
@app.get("/currency/{code}")
def currencies(code: str):
    return{"currency": code}

# parametr query http://localhost:8000/rates?date=13-03-2028
@app.get("/rates")
def get_rates(date: str):
    return {"date": date}



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)