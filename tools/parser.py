import requests

class ProductRef:

    def __init__(self, art, name, url, price):
        self.art = art
        self.name = name
        self.url = url
        self.price = price

proxies = {
    'http': 'http://Jaulka:dxub88sa@46.8.22.82:5500'
}

def get_info_by_url(url):
    #URL example
    #https://www.wildberries.ru/catalog/12345678/detail.aspx

    art = url.split("/")[4]
    detail_url = f"https://card.wb.ru/cards/v4/detail?appType=1&curr=rub&dest=-5551776&spp=30&hide_dtype=13;14&ab_testing=false&lang=ru&nm={art}"
    response = requests.get(detail_url, proxies=proxies, timeout=10)
    response.raise_for_status()
    data = response.json()

    for product in data["products"]:
        try:
            res = ProductRef(product['id'], product['name'], url, product['sizes'][0]['price']['product']/100)
        except:
            continue

    return res