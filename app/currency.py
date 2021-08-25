import requests
from lxml.html.soupparser import fromstring


def exchage_rate(currencies, base_currency='EUR'):
    out = {base_currency: 1}
    # base is RUB, from Central Bank RF
    url = 'https://www.cbr.ru/currency_base/daily/'
    response = requests.get(url)
    tree = fromstring(response.text)
    if base_currency=='RUB':
        base = 1
    else:
        base_txt = tree.xpath(f"//table/tbody/tr/child::td[2][text()='{base_currency}']/parent::node()/td[5]/text()")[0]
        base_quantity = int(tree.xpath(f"//table/tbody/tr/child::td[2][text()='{base_currency}']/parent::node()/td[3]/text()")[0])
        # in rubles
        base = float(base_txt.replace(',','.')) / base_quantity
    for c in currencies:
        if c==base_currency:
            continue
        elif c=='RUB':
            c_in_RUB = 1
        else:
            c_txt = tree.xpath(f"//table/tbody/tr/child::td[2][text()='{c}']/parent::node()/td[5]/text()")[0]
            c_quantity = int(tree.xpath(f"//table/tbody/tr/child::td[2][text()='{c}']/parent::node()/td[3]/text()")[0])
            c_in_RUB = float(c_txt.replace(',','.')) / c_quantity
        c_in_base = c_in_RUB / base
        out.update({c: c_in_base})

    return out

def main():
    currencies = ['KZT', 'RUB','USD','EUR']
    print(exchage_rate(currencies,'RUB'))

if __name__ == '__main__':
    main()
