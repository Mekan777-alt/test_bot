import requests


async def search_article_from_wb(article):
    url = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}'

    response = requests.get(url)

    if response.status_code != 200:

        return None

    product_data = response.json()

    if 'data' in product_data and 'products' in product_data['data'] and product_data['data']['products']:

        return product_data

    return None
