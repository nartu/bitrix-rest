from utils import bitrix_api
from datetime import datetime

def bitrix_deal_userfield_add(name, label, type, default_value=''):
    data = {
        "fields":
        {
            "FIELD_NAME": name,
            "EDIT_FORM_LABEL": label,
            "LIST_COLUMN_LABEL": label,
            "USER_TYPE_ID": type,   # datetime, string, address
            "XML_ID": "MY_STRING",
            "SETTINGS": { "DEFAULT_VALUE": default_value }
        }
    }
    return bitrix_api("crm.deal.userfield.add", data)

def bitrix_deal_userfield_delete_unused():
    fields = bitrix_api("crm.deal.userfield.list")["result"]
    for f in fields:
        if f["FIELD_NAME"].find('delivery'.upper()) == -1:
            bitrix_api("crm.deal.userfield.delete", {"id": int(f["ID"])})
    return bitrix_api("crm.deal.userfield.list")["result"]


def main():
    # print(bitrix_deal_userfield_add('delivery_code', 'Delivery code', 'string', '#'))
    # print(bitrix_deal_userfield_add('delivery_date', 'Delivery date', 'datetime'))
    # print(bitrix_deal_userfield_add('delivery_adress', 'Delivery address', 'address'))
    # print(datetime.now().isoformat())
    # print(bitrix_deal_userfield_delete_unused())
    # print('delivery'.upper())
    # print("some str".find("stra") == -1)


if __name__ == '__main__':
    main()
