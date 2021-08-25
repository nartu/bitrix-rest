import os
from pathlib import Path
import json
import requests
import settings as s


def write_json(dump={}, filename='answer.json', dir='json'):
    # parent of app
    BASE_DIR = Path(__file__).resolve().parent.parent
    dir = os.path.join(BASE_DIR, dir)
    path = os.path.join(dir, filename)
    if not os.path.exists(dir):
        os.mkdir(os.path.join(dir, 'json'))
    try:
        with open(path, 'w') as f:
            json.dump(dump, f, indent=4, ensure_ascii=False)
        return path
    except:
        return False


def bitrix_api(url, data={}, write_to_file=False, filename='answer.json'):
    URL = f'https://{s.domain}/rest/1/{s.token}/'
    url = os.path.join(URL, url)
    r = requests.post(url, json=data)
    jr = r.json()
    if write_to_file:
        write_json(jr, filename)
    return jr



def main():
    dump = {"test": "русские символы"}
    # print(write_json(dump))
    print(bitrix_api('crm.currency.list'))
    r = bitrix_api('crm.currency.get', {'id': 'USD'}, write_to_file=True, filename='answer3.json')
    print(r)

if __name__ == '__main__':
    main()
