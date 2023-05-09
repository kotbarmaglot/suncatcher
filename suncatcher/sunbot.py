from .config import API_KEY, API_KEY2
from .vksunbot import get_moon, get_moon_amount, create_catalog_file
from .user import *
from .patch1 import patch1
from .db import insert_table_user, get_amount_suncatcher, sell_suncatcher, get_url_suncatcher
import telebot
import json
from telebot import types
import pathlib
from pathlib import Path
import os
import sys
from pprint import pprint


bot = telebot.TeleBot(API_KEY2)


def message_delete(message, type_del):
    if type_del == 'message':
        ms_id = get_message_id(message)
        if ms_id:
            bot.delete_message(message.from_user.id, ms_id)

    if type_del == 'media':
        med_id = get_media_id(message)
        if med_id:
            for elem in med_id:
                bot.delete_message(message.from_user.id, elem)

            save_media_id(message, del_media_id=1)


def save_message_id(message, type='photo'):
    if type == 'photo':
        user_id = message.chat.id
        user_patch = Path(f"suncatcher/user_file/{user_id}.json")

        with open(user_patch, "r") as read_file:
            user_data = json.load(read_file)

        user_data['id_mes'] = message.message_id

        with open(user_patch, "w") as write_file:
            json.dump(user_data, write_file)
    
    if type == 'message':
        user_id = message.chat.id
        user_patch = Path(f"suncatcher/user_file/{user_id}.json")

        with open(user_patch, "r") as read_file:
            user_data = json.load(read_file)

        user_data['id_mes_message'] = message.message_id

        with open(user_patch, "w") as write_file:
            json.dump(user_data, write_file)


def save_media_id(message, del_media_id=0):
    media = []

    if del_media_id == 0:
        for elem in message:
            media.append(elem.message_id)
            user_id = elem.chat.id

        user_patch = Path(f"suncatcher/user_file/{user_id}.json")

        with open(user_patch, "r") as read_file:
            user_data = json.load(read_file)
            user_data['id_media'] = media

        with open(user_patch, "w") as write_file:
            json.dump(user_data, write_file)

    if del_media_id == 1:
        user_id = message.from_user.id
        user_patch = Path(f"suncatcher/user_file/{user_id}.json")

        with open(user_patch, "r") as read_file:
            user_data = json.load(read_file)
            user_data['id_media'] = ''

        with open(user_patch, "w") as write_file:
            json.dump(user_data, write_file)


def get_media_id(message, type='photo'):
    user_id = message.from_user.id
    user_patch = Path(f"suncatcher/user_file/{user_id}.json")

    if not os.path.exists(user_patch):
        return False
    else:
        with open(user_patch, "r") as read_file:
            user_data = json.load(read_file)

            if user_data['id_media'] != '':
                return user_data['id_media']
            else:
                return False


def get_message_id(message):
    user_id = message.from_user.id
    user_patch = Path(f"suncatcher/user_file/{user_id}.json")

    if not os.path.exists(user_patch):
        return False
    else:
        with open(user_patch, "r") as read_file:
            user_data = json.load(read_file)
            return user_data['id_mes']


def set_current_size_sun(message, size):
    user_id = message.from_user.id
    user_patch = Path(f"suncatcher/user_file/{user_id}.json")

    with open(user_patch, "r") as read_file:
        user_data = json.load(read_file)
        user_data['current_size'] = size

    with open(user_patch, "w") as write_file:
        json.dump(user_data, write_file)


def set_current_number_sun(message, current, size):
    user_id = message.from_user.id
    user_patch = Path(f"suncatcher/user_file/{user_id}.json")

    with open(user_patch, "r") as read_file:
        user_data = json.load(read_file)

    user_data['catalog'][size]['current'] = current

    with open(user_patch, "w") as write_file:
        json.dump(user_data, write_file)


def get_current_number_size_sun(message):
    user_id = message.from_user.id
    user_patch = Path(f"suncatcher/user_file/{user_id}.json")

    with open(user_patch, "r") as read_file:
        user_data = json.load(read_file)

    current_size = user_data['current_size']
    current_number = user_data['catalog'][current_size]['current']
    all_size = user_data['catalog'][current_size]['all']

    return current_number, current_size, all_size


def create_or_get_user_file(message):
    user_id = message.from_user.id
    user_patch = Path(f"suncatcher/user_file/{user_id}.json")
    amount = get_moon_amount()

    user_data = {}
    user_data['id'] = user_id
    user_data['catalog'] = {}
    user_data['catalog']['big'] = {}
    user_data['catalog']['mid'] = {}
    user_data['catalog']['low'] = {}
    user_data['catalog']['big']['all'] = amount['big']
    user_data['catalog']['mid']['all'] = amount['mid']
    user_data['catalog']['low']['all'] = amount['low']
    user_data['catalog']['big']['current'] = 0
    user_data['catalog']['mid']['current'] = 0
    user_data['catalog']['low']['current'] = 0
    user_data['start'] = 1
    user_data['current_size'] = ''
    user_data["id_mes"] = 0
    user_data["id_media"] = ''
    user_data["id_mes_message"] = 0

    with open(user_patch, "w") as write_file:
        json.dump(user_data, write_file)

    return user_data


def show_catalog(message, step_pre=0):
    title = '🌈☀️ Какие ловцы солнца вы хотите посмотреть:\n\n'
    big_sun = '☀️☀️☀️ <b>Большие ловцы </b> - общей длиной 40 см и больше. Cтоимость - 4000р.\n\n'
    mid_sun = '☀️☀️ <b>Средние ловцы</b> ~ 30 см. Cтоимость - 3000р.\n\n'
    low_sun = '☀️ <b>Малые ловцы</b> ~ 20 см. Cтоимость - 2000р.\n\n'

    text = f"{title}{big_sun}{mid_sun}{low_sun}"

    markup_inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("☀️☀️☀️ Большие ☀️☀️☀️", callback_data='big')
    item2 = types.InlineKeyboardButton("☀️☀️ Средние ☀️☀️", callback_data='mid')
    item3 = types.InlineKeyboardButton("☀️ Малые ☀️", callback_data='low')

    url_photo = 'https://sun9-42.userapi.com/impg/V7H81niHXYdgP2M_ZqbL4lRvuwGQGajdTvkdYw/KqT-wWKWTHw.jpg?size=2560x2560&quality=95&sign=79eab711010666d1651f6001fdf322d9&type=album'

    markup_inline.add(item1)
    markup_inline.add(item2)
    markup_inline.add(item3)

    if step_pre == 'media':
        msg = bot.send_photo(message.from_user.id, url_photo, caption=text, reply_markup=markup_inline, parse_mode='HTML')
        save_message_id(msg)
    else:
        ms_id = get_message_id(message)
        bot.edit_message_media(chat_id=message.from_user.id, message_id=ms_id, media=types.InputMediaPhoto(url_photo, caption=text, parse_mode='HTML'), reply_markup=markup_inline)


def show_choose_size_suncatcher(message, number_sun, size, next_update=0, step_pre=0):
    sun = get_moon(size)

    current_number, type, all_sun = get_current_number_size_sun(message)

    url_photo = sun[size][number_sun]['url_photo'][0]
    count = f'{size}_count'
    current_sun_text = f'{current_number+1}/{sun[count]}'

    callback_data_back = 'back'
    callback_data_next = 'next'

    if current_number+1 == sun[count]:
        callback_data_next = 'none'

    if current_number+1 == 1:
        callback_data_back = 'none'

    markup_inline = types.InlineKeyboardMarkup()

    if message.from_user.id == 257930228:
        item7 = types.InlineKeyboardButton(text='Продано', callback_data='sell_suncatcher')
        markup_inline.add(item7)

    item = types.InlineKeyboardButton(text='💫 Описание/Фото', callback_data='more')
    item2 = types.InlineKeyboardButton(text='⬅️', callback_data=callback_data_back)
    item3 = types.InlineKeyboardButton(text='➡️', callback_data=callback_data_next)
    item6 = types.InlineKeyboardButton(text='🎁 Заказать', callback_data='choose')
    item4 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')
    item5 = types.InlineKeyboardButton(text=f'{current_sun_text}', callback_data='none')

    markup_inline.add(item2, item5, item3)
    markup_inline.add(item6)
    markup_inline.add(item)
    markup_inline.add(item4)

    if next_update == 0:
        if step_pre == 'media':
            message_delete(message, type_del='message')
            msg = bot.send_photo(message.from_user.id, url_photo,  reply_markup=markup_inline)
            save_message_id(msg)
        else:
            ms_id = get_message_id(message)
            bot.edit_message_media(chat_id=message.from_user.id, message_id=ms_id, media=types.InputMediaPhoto(url_photo), reply_markup=markup_inline)
    
    if next_update == 'next':
        ms_id = get_message_id(message)
        bot.edit_message_media(chat_id=message.from_user.id, message_id=ms_id,  media=types.InputMediaPhoto(url_photo), reply_markup=markup_inline)


def show_choose_size_suncatcher_more(message, number_sun, size):
    sun = get_moon(size)

    url_photo = sun[size][number_sun]['url_photo']
    description = sun[size][number_sun]['description'].replace('"выбрать" ⬇️ чтобы заказать', '🎁 <b>Заказать</b>')

    media = []

    for url in url_photo:
        media.append(types.InputMediaPhoto(url))

    msg_med = bot.send_media_group(message.from_user.id, media)

    save_media_id(msg_med)

    markup_inline = types.InlineKeyboardMarkup()

    item = types.InlineKeyboardButton(text='🎁 Заказать', callback_data='choose1')
    item2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back1')
    item4 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog1')

    markup_inline.add(item)
    markup_inline.add(item2, item4)

    message_delete(message, type_del='message')

    msg = bot.send_message(message.from_user.id, text=description, reply_markup=markup_inline, parse_mode='HTML')

    save_message_id(msg)


def choose(message, number_sun, size, step_pre=0):
    sun = get_moon(size)

    url_photo = sun[size][number_sun]['url_photo'][0]

    text = '👍 Для заказа этого ловца солнца нажмите: \n\n✍️ Написать - чтобы связаться с мастером и лично обсудить детали заказа и доставки.\n\n🎁 Заказать - чтобы пройти процедуру заказа в автоматическом режиме.'

    markup_inline = types.InlineKeyboardMarkup()

    item = types.InlineKeyboardButton(text='✍️ Написать', url='https://t.me/Lunar_room')
    item2 = types.InlineKeyboardButton(text='🎁 Заказать', callback_data='orderbot')
    item3 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back2')
    item4 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')

    markup_inline.add(item, item2)
    markup_inline.add(item3, item4)

    if step_pre == 'media':
        message_delete(message, type_del='message')
        msg = bot.send_photo(message.from_user.id, url_photo, caption=text, reply_markup=markup_inline)
        save_message_id(msg)
    else:
        ms_id = get_message_id(message)
        bot.edit_message_media(chat_id=message.from_user.id, message_id=ms_id, media=types.InputMediaPhoto(url_photo, caption=text), reply_markup=markup_inline)

    # bot.send_photo(-1001976282334, url_photo, caption=description)
    chat = bot.get_chat(message.from_user.id)
    print('!!!!!!!!!!!!!!!\n\n', chat)
    chat_id = str(chat.id)

    chat_username = '@' + chat.username if chat.username else 'none'

    chat_firstname = chat.first_name if chat.first_name else 'none'

    chat_lastname = chat.last_name if chat.last_name else 'none'

    send_text_chat = 'id: ' + chat_id + '\n' + 'username: ' + chat_username + '\n' + 'Имя: ' + chat_firstname + '\n' + 'Фамилия: ' + chat_lastname

    # bot.send_message(-1001976282334, text=send_text_chat)


def step_adress(message):
    order_sun_via_bot(message, step='details_pay')
    bot.delete_message(message.chat.id, message.message_id)


def order_sun_via_bot(message, step):
    number, size, all = get_current_number_size_sun(message)
    sun = get_moon(size)

    if size == 'big' or 'mid':
        cost_ship = '350 рублей'
        size_sun = 'больших и средних'
    else:
        cost_ship = '300 рублей'
        size_sun = 'малых'

    url_photo = sun[size][number]['url_photo'][0]

    if step == 'orderbot':
        script_one_step = 'Этот ловец солнца в наличии. \n\n<b>Вы для себя его выбрали или в подарок?</b> '

        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='💁‍♀️ Для себя', callback_data='forme')
        item2 = types.InlineKeyboardButton(text='🎁 В подарок', callback_data='forgift')
        item3 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back2')
        item4 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')

        markup_inline.add(item, item2)
        markup_inline.add(item3, item4)

        ms_id = get_message_id(message)

        bot.edit_message_media(chat_id=message.from_user.id, message_id=ms_id,  media=types.InputMediaPhoto(url_photo, caption=script_one_step, parse_mode='HTML'), reply_markup=markup_inline)
    
    if step == 'forme':
        script_one_step = f'🚚 Доставка из Краснодарского края {size_sun} ловцов стоит {cost_ship}. \n\n📦 Отправка почтой России в день заказа, либо на следующий день. \n\n💳 Оплата переводом на Сбербанк или Тинькоф. \n\n<b>Вам подходит?</b>'

        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='✅ Да', callback_data='input_adress')
        item2 = types.InlineKeyboardButton(text='⛔️ Нет. Связаться с мастером', url='https://t.me/Lunar_room')

        markup_inline.add(item)
        markup_inline.add(item2)

        ms_id = get_message_id(message)

        bot.edit_message_media(chat_id=message.from_user.id, message_id=ms_id,  media=types.InputMediaPhoto(url_photo, caption=script_one_step, parse_mode='HTML'), reply_markup=markup_inline)

    
    if step == 'forgift':
        script_one_step = f'🎁 Ловец солнца придёт к вам в подарочной упаковке. К заказу я приложу открытку, которую вы сами сможете подписать. И подарок полностью будет готов к вручению)\n\n🚚 Доставка из Краснодарского края {size_sun} ловцов стоит {cost_ship}. \n\n📦 Отправка почтой России в день заказа, либо на следующий день. \n\n💳 Оплата переводом на Сбербанк или Тинькоф. \n\n<b>Вам подходит?</b>'

        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='✅ Да', callback_data='input_adress')
        item2 = types.InlineKeyboardButton(text='⛔️ Нет. Связаться с мастером', url='https://t.me/Lunar_room')

        markup_inline.add(item)
        markup_inline.add(item2)

        ms_id = get_message_id(message)

        bot.edit_message_media(chat_id=message.from_user.id, message_id=ms_id,  media=types.InputMediaPhoto(url_photo, caption=script_one_step, parse_mode='HTML'), reply_markup=markup_inline)


    if step == 'input_adress':
        script_one_step = '<b>Введите адрес доставки в поле сообщения и нажмите отправить:</b> '
        markup_inline = types.InlineKeyboardMarkup()

        ms_id = get_message_id(message)

        msg = bot.edit_message_media(chat_id=message.from_user.id, message_id=ms_id,  media=types.InputMediaPhoto(url_photo, caption=script_one_step, parse_mode='HTML'))

        bot.register_next_step_handler(msg, step_adress)


    if step == 'details_pay':
        adress = message.json['text']
        details_pay = '👍 Хорошо. Доставка 300р + стоимость ловца солнца 2000р. Итого 2300р. Оплату можно перевести на карту Тинькоф или Сбербанк по номеру телефона 89180119741 Получатель: Оксана Николаевна И.\n\n'
        script_one_step =  f'{details_pay}Ваш адрес: {adress}. \n\nЕсли все правильно, оплачивайте и нажимайте оплатил(a). В течении часа вам придет номер для отслеживания посылки' 

        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='Оплатил(а)', callback_data='none')
        item2 = types.InlineKeyboardButton(text='Проверить трекинг номер', callback_data='none')

        markup_inline.add(item)
        markup_inline.add(item2)

        ms_id = get_message_id(message)

        bot.edit_message_media(chat_id=message.from_user.id, message_id=ms_id, media=types.InputMediaPhoto(url_photo, caption=script_one_step), reply_markup=markup_inline)


@bot.message_handler(commands=['start'])
def start(message):

    insert_table_user(message)
    get_amount_suncatcher()

    bot.delete_message(message.from_user.id, message.message_id)

    # create_user_file(message)

    try:
        message_delete(message, type_del='message')
        message_delete(message, type_del='media')

    except Exception:
        create_or_get_user_file(message)

    create_or_get_user_file(message)

    user_name = message.from_user.first_name if message.from_user.first_name else message.from_user.username

    text_message = f'Привет, {user_name}! \n\nДобро пожаловать в каталог с ловцами солнца 🌈✨\n\nВы можете посмотреть здесь наличие.\n\nА если выберете цветочную луну по душе, то чат-бот пришлёт вам инструкцию, как заказать ловец солнца.'

    url_photo = Path("suncatcher/admin_file/oksa.jpg")
    img = open(url_photo, 'rb')
    markup_inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')
    markup_inline.add(item1)

    msg = bot.send_photo(message.from_user.id, img, caption=text_message, reply_markup=markup_inline)

    save_message_id(msg)


@bot.callback_query_handler(func=lambda m: True)
def callback_choice(message):
    t = message.data

    if t == 'catalog':
        set_current_size_sun(message, size='')
        show_catalog(message)
        set_current_number_sun(message, current=0, size='big')
        set_current_number_sun(message, current=0, size='mid')
        set_current_number_sun(message, current=0, size='low')

    if t == 'catalog1':
        message_delete(message, type_del='message')
        message_delete(message, type_del='media')
        set_current_size_sun(message, size='')
        show_catalog(message, step_pre='media')
        set_current_number_sun(message, current=0, size='big')
        set_current_number_sun(message, current=0, size='mid')
        set_current_number_sun(message, current=0, size='low')

    if t == 'big':
        set_current_size_sun(message, t)
        show_choose_size_suncatcher(message, number_sun=0, size=t, next_update=0)

    if t == 'mid':
        set_current_size_sun(message, t)
        show_choose_size_suncatcher(message, number_sun=0, size=t, next_update=0)

    if t == 'low':
        set_current_size_sun(message, t)
        show_choose_size_suncatcher(message, number_sun=0, size=t, next_update=0)

    if t == 'next':
        number, size, all = get_current_number_size_sun(message)
        set_current_number_sun(message, current=number+1, size=size)
        show_choose_size_suncatcher(message, number_sun=number+1, size=size, next_update='next')

    if t == 'back':
        number, size, all = get_current_number_size_sun(message)
        set_current_number_sun(message, current=number-1, size=size)
        show_choose_size_suncatcher(message, number_sun=number-1, size=size, next_update='next')

    if t == 'more':
        number, size, all = get_current_number_size_sun(message)
        show_choose_size_suncatcher_more(message, number_sun=number, size=size)

    if t == 'choose':
        number, size, all = get_current_number_size_sun(message)
        # message_delete(message, type_del='media')
        choose(message, number_sun=number, size=size)

# Когда предыдущий шаг формирует сообщение из группы картинок, метод edit_message не подходит. Поэтому приходится удалять сообщение и отправлять новое. Это касается всех функций с параметром step_pre.
    if t == 'choose1':
        number, size, all = get_current_number_size_sun(message)
        message_delete(message, type_del='media')
        choose(message, number_sun=number, size=size, step_pre='media')

    if t == 'back1':
        message_delete(message, type_del='media')
        number, size, all = get_current_number_size_sun(message)
        set_current_number_sun(message, current=number, size=size)
        show_choose_size_suncatcher(message, number_sun=number, size=size, step_pre='media')

    if t == 'back2':
        number, size, all = get_current_number_size_sun(message)
        set_current_number_sun(message, current=number, size=size)
        show_choose_size_suncatcher(message, number_sun=number, size=size)

    if t == 'orderbot':
        order_sun_via_bot(message, step=t)

    if t == 'forme':
        order_sun_via_bot(message, step=t)

    if t == 'forgift':
        order_sun_via_bot(message, step=t)

    if t == 'input_adress':
        order_sun_via_bot(message, step=t)

    if t == 'sell_suncatcher':
        sell_suncatcher()


@bot.message_handler(func=lambda m: True)
def handler(message):
    pass


bot.infinity_polling()


def main():
    pass


if __name__ == '__main__':
    main()