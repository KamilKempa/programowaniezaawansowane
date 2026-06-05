from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def root():
    return{"route works"}

@app.post("/currencies/fetch")
def fetch_currencies():
    url = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"

    response = requests.get(url)
    data = response.json()

    rates = data[0]["rates"]

    cleaned = []

    for r in rates:
        cleaned.append({
            "code": r["code"],
            "currency": r["currency"],
            "mid": r["mid"]
        })
    return cleaned

# NIE WYKORZYSTANE

@app.get("/testowa")
def testowa():
    return{"testowa"}

# parametr path http://localhost:8000/currency/PLN
@app.get("/currency/{code}")
def currencies(code: str):
    return{"currency": code}

# parametr query http://localhost:8000/rates?date=13-03-2028
@app.get("/rates")
def get_rates(date: str):
    return {"date": date}

