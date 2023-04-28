import vk
import json
from .config import VK_TOKEN_USER, VK_MARKET_ID


def update_info_product():
    vkapi = vk.API(VK_TOKEN_USER)
    market_get = vkapi.market.get(count='100', v=5.131, owner_id=VK_MARKET_ID)

    if data == market_get:
        print('Данные одинаковые. Новых товаров или изменений нет')
    else:
        with open("info_product.json", "w") as write_file:
            json.dump(market_get, write_file)
            print('Данные разные. Файл с товарами обновлен.')

    # for elem in data['items']:
    #     print(elem['description'])

    # for elem in data['items']:
    #     print(elem['thumb_photo'])

    # for elem in data['items']:
    #     print(elem['price'])

    # for elem in data['items']:
    #     print(elem['price']['amount'])

    # for elem in data['items']:
    #     if 'discount_rate' in elem['price']:
    #         print(elem['price']['discount_rate'])


with open("info_product.json", "r") as read_file:
    data = json.load(read_file)
#  and ('луна' in elem['title'].lower())


def get_big_moon(data, message):
    description = []
    title = []
    url_photo = []

    for elem in data['items']:
        if (elem['title'] != 'Доставка') and (int(elem['price']['amount']) > 310000):
            description.append(elem['title'] + '\n\n' + elem['description'] + '\n\n' + 'Стоимость - ' + elem['price']['amount'][0:4] + ' ' + elem['price']['currency']['name'])
            title.append(elem['title'])
            url_photo.append(elem['thumb_photo'])

    return (description, title, url_photo)

def get_big_lunnica(data, message):
    description = []
    title = []
    url_photo = []
    id_product = []
    

    for elem in data['items']:
        if (elem['title'] != 'Доставка') and (int(elem['price']['amount']) > 310000) and ('лунница' in elem['title'].lower()):
            description.append(elem['title'] + '\n\n' + elem['description'] + '\n\n' + 'Стоимость - ' + elem['price']['amount'][0:4] + ' ' + elem['price']['currency']['name'])
            title.append(elem['title'])
            url_photo.append(elem['thumb_photo'])
            id_product.append(elem['id'])


    return (description, title, url_photo, id)


def main():
    pass


if __name__ == '__main__':
    main()