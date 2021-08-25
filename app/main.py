from fastapi import FastAPI
from bitrix_currency import currency_update_all

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Bitrix api test task"}

@app.get("/exchage_rates_update")
async def read_exchage_rates():
    currencies = ['KZT','RUB','USD']
    return currency_update_all(currencies, 'EUR')
