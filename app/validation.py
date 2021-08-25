from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import List
import json
import re
from bitrix_currency import currency_update_all

input_json1 = '''
{
    "title": "title",
    "description": "Some description",
    "client": {
        "name": "Jon",
        "surname": "Karter",
        "phone": "+77777777777",
        "adress": "st. Mira, 287, Moscow"
    },
    "products": ["Candy", "Carrot", "Potato"],
    "delivery_adress": "st. Mira, 211, Ekaterinburg",
    "delivery_date": "2021-01-01:16:00",
    "delivery_code": "#232nkF3fAdn"
}
'''

input_json = '''
{
    "title": "title",
    "description": "Some description",
    "client": {
        "name": "Jon",
        "surname": "Karter",
        "phone": "+77777777777",
        "adress": "st. Mira, 287, Moscow"
    },
    "products": ["Candy", "Carrot", "Potato", 1],
    "delivery_adress": "st. Mira, 211, Ekaterinburg",
    "delivery_date": "2021-01-01:16:00",
    "delivery_code": "#232nkF3fAdn"
}
'''

class Client(BaseModel):
    name: str
    surname: str
    phone: str
    adress: str

    @validator('phone')
    def phone_must_be_numeric_with_plus(cls, v):
        phone_pattern = r'\+7\d{10}'
        if len(v) !=12 or not re.search(phone_pattern, v):
            raise ValueError('phone must contain + and 10 digits')
        return v


class Order(BaseModel):
    title: str
    description: str
    client: Client
    products: List[str]
    delivery_adress: str
    delivery_date: str
    delivery_code: str

    @validator('delivery_date')
    def date_must_be_datatime(cls, v):
        if type(v) is datetime:
            return v
        else:
            try:
                # "2021-01-01:16:00"
                dt = datetime.strptime(v, "%Y-%m-%d:%H:%M")
            except:
                raise ValueError('date must be a datatime')
            else:
                return dt

def main():
    try:
        order = Order.parse_raw(input_json)
        # client = Client.parse_raw(input_json)
    except ValidationError as e:
        print(e.json())
    else:
        print(order)
        # print(client)



if __name__ == '__main__':
    main()
