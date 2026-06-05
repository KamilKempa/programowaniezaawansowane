from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{"route works"}

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

@app.post("/currencies/fetch")
def fetch_currencies():
    return {
        "status": "success",
        "message": "pobieranie kursow walut"
    }