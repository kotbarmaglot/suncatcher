import vk
from .config import VK_TOKEN_USER, VK_MARKET_ID
from pathlib import Path
import json
import datetime
import os

vkapi = vk.API(VK_TOKEN_USER)


def market_get():
    return vkapi.market.get(count='100', extended=1, v=5.131, owner_id=VK_MARKET_ID)


def get_catalog_vk():

    data = market_get()

    suns = {}
    suns['big'] = []
    suns['mid'] = []
    suns['low'] = []
    suns['amount'] = {}
    # suns['date'] = str(datetime.datetime.now())[0:10]

    for elem in data['items']:
        suncatcher = {}
        big = (elem['title'] != 'Доставка') and elem['owner_info']['category'] == 'Большие 40см'
        mid = (elem['title'] != 'Доставка') and elem['owner_info']['category'] == 'Средние 30см'
        low = (elem['title'] != 'Доставка') and elem['owner_info']['category'] == 'Малые 20см'

        suncatcher['id'] = elem['id']
        suncatcher['title'] = elem['title']
        suncatcher['description'] = elem['description']
        suncatcher['price'] = elem['price']['amount']
        suncatcher['url_photo'] = []

        if big:
            suncatcher['url_photo'] = get_url_photo_list(elem)
            suns['big'].append(suncatcher)

        if mid:
            suncatcher['url_photo'] = get_url_photo_list(elem)
            suns['mid'].append(suncatcher)

        if low:
            suncatcher['url_photo'] = get_url_photo_list(elem)
            suns['low'].append(suncatcher)
        
    suns['amount']['big'] = len(suns['big'])
    suns['amount']['mid'] = len(suns['mid'])
    suns['amount']['low'] = len(suns['low'])

    return suns


def get_url_photo_list(data):
    out_list = []
    for photo in data['photos']:
        for x in photo['sizes']:
            if x['type'] == 'x':
                out_list.append(x['url'])
    return out_list


def create_catalog_file():
    catalog_patch = Path(f"suncatcher/admin_file/catalog_suns.json")
    data = get_catalog_vk()
    with open(catalog_patch, "w") as write_file:
        json.dump(data, write_file)


def update_catalog_file():
    current_date = str(datetime.datetime.now())[0:10]
    catalog_patch = Path(f"suncatcher/admin_file/catalog_suns.json")

    if not os.path.exists(catalog_patch):
        create_catalog_file()
        print('Файл не было. Файл создан')

    else:
        with open(catalog_patch, "r") as read_file:
            user_data = json.load(read_file)

        if user_data['date'] == current_date:
            print('Файл существует, создан сегодня и не нуждается в обновлении')
        else:
            create_catalog_file()
            print('Файл был старый. Обновили')
    

def get_moon(size):
    suns = {}
    suns[size] = []
    suns[f'{size}_count'] = 0

    data = market_get()

    for elem in data['items']:
        big = (elem['title'] != 'Доставка') and elem['owner_info']['category'] == 'Большие 40см'
        mid = (elem['title'] != 'Доставка') and elem['owner_info']['category'] == 'Средние 30см'
        low = (elem['title'] != 'Доставка') and elem['owner_info']['category'] == 'Малые 20см'
        suncatcher = {}

        suncatcher['id'] = elem['id']
        suncatcher['title'] = elem['title']
        suncatcher['description'] = elem['description']
        suncatcher['price'] = elem['price']['amount']
        suncatcher['url_photo'] = []


        if big and size == 'big':
            suns[f'{size}_count'] = suns[f'{size}_count'] + 1
            suncatcher['url_photo'] = get_url_photo_list(elem)
            suns['big'].append(suncatcher)

        if mid and size == 'mid':
            suns[f'{size}_count'] = suns[f'{size}_count'] + 1
            suncatcher['url_photo'] = get_url_photo_list(elem)
            suns['mid'].append(suncatcher)

        if low and size == 'low':
            suns[f'{size}_count'] = suns[f'{size}_count'] + 1
            suncatcher['url_photo'] = get_url_photo_list(elem)
            suns['low'].append(suncatcher)

    return suns


def get_moon_amount():
    amount = {}
    amount['big'] = 0
    amount['mid'] = 0
    amount['low'] = 0

    data = market_get()

    for elem in data['items']:
        big = (elem['title'] != 'Доставка') and elem['owner_info']['category'] == 'Большие 40см'
        mid = (elem['title'] != 'Доставка') and elem['owner_info']['category'] == 'Средние 30см'
        low = (elem['title'] != 'Доставка') and elem['owner_info']['category'] == 'Малые 20см'

        if big:
            amount['big'] += 1

        if mid:
            amount['mid'] += 1

        if low:
            amount['low'] += 1

    return amount


def main():
    pass


if __name__ == '__main__':
    main()