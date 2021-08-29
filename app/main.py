from fastapi import FastAPI
from bitrix_currency import currency_update_all
from validation import Order, Client
from bitrix_deal import bitrix_deal_add
from bitrix_deal import bitrix_contact_add

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Bitrix api test task"}

@app.get("/exchage_rates_update")
async def read_exchage_rates():
    currencies = ['KZT','RUB','USD']
    return currency_update_all(currencies, 'EUR')

@app.post("/add_deal")
async def read_order(order: Order):
    return bitrix_deal_add(order)

@app.post("/add_contact")
async def read_contact(client: Client):
    return {"id": bitrix_contact_add(client)}
