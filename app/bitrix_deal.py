from validation import Order, Client, input_json
from utils import bitrix_api
from datetime import datetime
from typing import List, Dict

def bitrix_contact_search(client: Client):
    data = {
        "filter":
        {
            # "NAME": client.name,
            # "LAST_NAME": client.surname,
            # "TYPE_ID": "CLIENT",
            # "SOURCE_ID": "REST",
            "PHONE": client.phone,
            # "ADDRESS": client.adress
        },
        "select": ["ID"]
    }
    result = bitrix_api("crm.contact.list", data, True, 'contact_list.json')
    id = result.get("result")[0].get("ID") if result.get("total")>0 else None
    return id


def bitrix_contact_add(client: Client) -> int:
    # if contact already exists
    id = bitrix_contact_search(client)
    if id:
        return id
    data = {
        "fields":
        {
            "NAME": client.name,
            "LAST_NAME": client.surname,
            "OPENED": "Y",
            "ASSIGNED_BY_ID": 1,
            "TYPE_ID": "CLIENT",
            "SOURCE_ID": "REST",
            "PHONE": [ { "VALUE": client.phone, "VALUE_TYPE": "OTHER" } ],
            "ADDRESS": client.adress
        }}
    return bitrix_api("crm.contact.add", data)["result"]

def bitrix_product_get(product_id: int, currency: str, quantity: int = 1):
    product = bitrix_api("crm.product.get", {"id": product_id}, True, f"prodcut_{product_id}.json").get("result")
    base_currency_id = bitrix_api('crm.currency.base.get').get('result')
    product_currency =  bitrix_api('crm.currency.get',{"id": product["CURRENCY_ID"]}).get('result')
    local_currency =  bitrix_api('crm.currency.get',{"id": currency}).get('result')
    price_in_base = float(product["PRICE"]) * float(product_currency["AMOUNT"]) / int(product_currency["AMOUNT_CNT"])
    price_in_local = price_in_base / float(local_currency["AMOUNT"]) * int(local_currency["AMOUNT_CNT"])
    # return [(product["PRICE"], product["CURRENCY_ID"]), (price_in_base, base_currency_id), (price_in_local, currency)]
    # return {"id": product_id, "price": price_in_local}
    return { "PRODUCT_ID": product_id, "PRICE": price_in_local, "QUANTITY": quantity }

def bitix_deal_productrows_set(deal_id: int, product_codes: List):
    currency_id = bitrix_api("crm.deal.get", {"id": deal_id}).get("result").get("CURRENCY_ID")
    data_product_list =  {
                "filter": { "CODE": product_codes },
                "select": [ "ID" ]
            }
    product_ids = [p["ID"] for p in bitrix_api("crm.product.list", data_product_list)["result"]]
    data = {
                "id": deal_id,
                "rows": [bitrix_product_get(p, currency_id) for p in product_ids]
            }
    return bitrix_api("crm.deal.productrows.set", data)

def bitrix_deal_search(delivery_code: str) -> int:
    data =  {
            "order": { "ID": "DESC" },
            # "filter": { ">=STAGE_ID": "EXECUTING", "CURRENCY_ID": currency_id, "CONTACT_ID": contact_id },
            "filter": { "UF_CRM_DELIVERY_CODE": delivery_code },
            "select": [ "ID", "TITLE", "STAGE_ID", "PROBABILITY", "OPPORTUNITY", "CURRENCY_ID" ]
            }
    deals = bitrix_api("crm.deal.list", data)
    return deals["result"][0]["ID"] if deals["total"]>0 else None


def bitrix_deal_add(order: Order, currency_id: str = "RUB"):
    deal_id = bitrix_deal_search(order.delivery_code)
    if not deal_id:
        contact_id = bitrix_contact_add(order.client)
        data = {
            "fields":
            {
                # "TITLE": "Заказ "+datetime.now().strftime("%y%m%dT%H:%M"),
                "TITLE": order.title,
                "COMMENTS": order.description,
                "TYPE_ID": "GOODS",
                "STAGE_ID": "NEW",
                "CONTACT_ID": contact_id,
                "OPENED": "Y",
                "ASSIGNED_BY_ID": 1,
                "CURRENCY_ID": currency_id,
                "BEGINDATE": datetime.now().isoformat(),
                "UF_CRM_DELIVERY_CODE": order.delivery_code,
                "UF_CRM_DELIVERY_DATE": order.delivery_date.isoformat(),
                "UF_CRM_DELIVERY_ADRESS": order.delivery_adress
            }
        }
        deal_id = bitrix_api("crm.deal.add", data)["result"]
    bitix_deal_productrows_set(deal_id, order.products)
    return bitrix_api("crm.deal.get", {"id": deal_id}, True, f"deal_{deal_id}.json")



def main():
    order = Order.parse_raw(input_json)
    order.title = "Заказ "+datetime.now().strftime("%y%m%dT%H:%M")
    client = Client.parse_raw( """{
                "name": "J",
                "surname": "I",
                "phone": "+79800099011",
                "adress": "ul. Poperechnaya, Moscow"
        }""")
    order.client = client
    order.products = ["soap"]
    order.delivery_code = "#232nkF3fsww"
    # print(order)
    # print(bitrix_deal_add(order))
    # print(bitix_deal_productrows_set(18))
    # print(bitrix_product_get(6, "USD"))
    # print(bitix_deal_productrows_set(18, ["Candy", "soap"]))
    # print(bitrix_deal_search(25, "RUB"))
    print(bitrix_deal_add(order))



if __name__ == '__main__':
    main()
