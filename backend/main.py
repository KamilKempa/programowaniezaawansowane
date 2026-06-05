from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import requests
import models
from database import engine, Base, SessionLocal

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
def fetch_currencies(db: Session = Depends(get_db)):
    url = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"

    response = requests.get(url)
    data = response.json()

    rates = data[0]["rates"]

    saved = []

    for r in rates:
        db_rate = models.CurrencyRate(
            code=r["code"],
            currency=r["currency"],
            mid=r["mid"]
        )
        db.add(db_rate)
        saved.append({
            "code": r["code"],
            "currency": r["currency"],
            "mid": r["mid"]
        })

    db.commit()

    return {
        "message": "dane zostaly zapisane",
        "count": len(saved),
        "rates":saved
    }

#get kursow walut z bazy danych

@app.get("/currencies")
def get_currencies(db: Session = Depends(get_db)):
    data = db.query(models.CurrencyRate).all()
    return[
        {
            "code": d.code,
            "currency": d.currency,
            "mid": d.mid
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

