import requests
import os
from utils import write_json
from utils import bitrix_api
from currency import exchage_rate

URL = 'https://b24-nh974e.bitrix24.ru/rest/1/09nvbvhafjit7lbe/'

def currency_list():
    return bitrix_api('crm.currency.list',{},True,'currency_list.json')

def currency_get(symbol_id):
    data = {'id': symbol_id}
    bitrix_api_param = {
        'url': 'crm.currency.get',
        'data': data,
        'write_to_file': True,
        'filename': f'currency_{symbol_id}.json'
    }
    bitrix_api(**bitrix_api_param)

def currency_add(currency, amount):
    data =  {
        "fields":
        {
            "CURRENCY": currency,
            "AMOUNT_CNT": 1,
            "AMOUNT": amount,
            "SORT": 1000
        }
    }
    return bitrix_api('crm.currency.add', data)

def currency_update(symbol_id, amount, amount_cnt=1):
    data = {
                'id': symbol_id,
                'fields':
                {
                    "AMOUNT_CNT": amount_cnt,
                    "AMOUNT": amount,
                }
            }
    return bitrix_api('crm.currency.update', data)

def currency_update_all(currencies, base_currency):
    amount_cnt_list = {'KZT': 1000, 'RUB': 100}
    if bitrix_api('crm.currency.base.get').get('result') != base_currency:
        bitrix_api('crm.currency.base.set', {'id': base_currency})
    rates = exchage_rate(currencies, base_currency)
    for currency,rate in rates.items():
        amount_cnt = amount_cnt_list.get(currency,1)
        currency_update(currency, rate*amount_cnt, amount_cnt)
    return currency_list()

def main():
    currencies = ['KZT','RUB','USD']
    # print(currency_list())
    # print(currency_update('ARS', 5500))
    r = currency_update_all(currencies, 'EUR')
    print(r)

if __name__ == '__main__':
    main()
