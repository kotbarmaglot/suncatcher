from .config import API_KEY, API_KEY2 
from .vksunbot import get_moon, get_moon_amount, create_catalog_file
from .db import update_table_user, get_amount_suncatcher, get_url_suncatcher, get_suncather_catalog, update_current_state, get_current_state, get_user, insert_table_suncatcher, update_step_order, update_table_press_start, create_table_press_start, get_table_press_start, update_user_path, get_user_path, create_table_user_path, get_user_path, create_table_current_state, update_order, get_order, create_table_all, insert_table_suncatcher_photo, create_table_user, get_table
import telebot
import json
from telebot import types
import pathlib
from pathlib import Path
import os
import sys
from pprint import pprint
import datetime


bot = telebot.TeleBot(API_KEY2)

table = ['user','suncatcher', 'suncatcher_photo', 'press_start', 'current_state', 'user_path', 'order', 'step_order']

admin = [257930228, 1820161475]


def update_patch():
    fds = sorted(os.listdir('suncatcher/user_file/'))

    for js in fds:
        with open(f'suncatcher/user_file/{js}') as f:
            user = json.load(f)

            try:
                bot.delete_message(user['id'], user['id_mes'])
            except:
                print('oops1')

            for elem in user['id_media']:
                try:
                    bot.delete_message(user['id'], elem)
                except:
                    print('oops2')

            bot.send_message(user['id'], text=f'В чат-боте произошли обновления. Чтобы посмотреть изменения, вам нужно перезапустить бота. \n\nНажмите /start')

        os.remove(f'suncatcher/user_file/{js}')
        print(f'удалено-{js}')
                

def delete_message(message, type):
    if type == 'media_and_text':
        current_data = get_current_state(message.from_user.id)
        current_message_id_text = current_data[6]
        current_message_id_media = current_data[5].split(',')

        for elem in current_message_id_media:
            bot.delete_message(message.from_user.id, elem)

        bot.delete_message(message.from_user.id, current_message_id_text)
    
    if type == 'photo':
        current_data = get_current_state(message.from_user.id)
        current_message_id_photo = current_data[4]

        bot.delete_message(message.from_user.id, current_message_id_photo)


def show_catalog(message, step_pre=0):

    insert_table_suncatcher()
    insert_table_suncatcher_photo()

    title = '🌈 Какие ловцы солнца вы хотите посмотреть:\n\n'
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
        delete_message(message, type='media_and_text')
        update_current_state(msg, type='start')
    else:
        current_data = get_current_state(message.from_user.id)
        current_message_id = current_data[4]

        bot.edit_message_media(chat_id=message.from_user.id, message_id=current_message_id, media=types.InputMediaPhoto(url_photo, caption=text, parse_mode='HTML'), reply_markup=markup_inline)


def show_choose_size_suncatcher_db(message, size, step_pre=0):
    catalog = get_suncather_catalog(size)
    current_data = get_current_state(message.from_user.id)

    current_number_sun = current_data[1]
    current_message_id = current_data[4]

    current_sun_id = catalog[current_number_sun][0]
    current_sun_title = catalog[current_number_sun][1]
    current_sun_desc = catalog[current_number_sun][2]
    current_sun_price = catalog[current_number_sun][3]
    current_sun_cat = catalog[current_number_sun][4]
    available_sun = catalog[current_number_sun][4]

    amount_sun = len(catalog)

    current_url_sun = get_url_suncatcher(current_sun_id)

    callback_data_back = 'back'
    callback_data_next = 'next'

    if current_number_sun+1 == amount_sun:
        callback_data_next = 'none'

    if current_number_sun+1 == 1:
        callback_data_back = 'none'

    markup_inline = types.InlineKeyboardMarkup()

    # if message.from_user.id == 257930228:
    #     item7 = types.InlineKeyboardButton(text='Продано', callback_data='sell_suncatcher')
    #     markup_inline.add(item7)

    # item9 = types.InlineKeyboardButton(text=f'{current_sun_title}', callback_data='none')
    item10 = types.InlineKeyboardButton(text=f'💰 Цена - {current_sun_price[0:4]}р', callback_data='none')
    item = types.InlineKeyboardButton(text='💫 Описание/Фото', callback_data='more')
    item2 = types.InlineKeyboardButton(text='⬅️', callback_data=callback_data_back)
    item3 = types.InlineKeyboardButton(text='➡️', callback_data=callback_data_next)
    item6 = types.InlineKeyboardButton(text=f'🎁 Заказать ({current_sun_price[0:4]}р)', callback_data='choose')
    item4 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')
    item5 = types.InlineKeyboardButton(text=f'{current_number_sun+1}/{amount_sun}', callback_data='none')

    # markup_inline.add(item9)
    markup_inline.add(item2, item5, item3)
    markup_inline.add(item6)
    markup_inline.add(item,item4)
    # markup_inline.add(item10, item6)

    if step_pre == 'media':
        msg = bot.send_photo(message.from_user.id, current_url_sun[0][0], reply_markup=markup_inline, parse_mode='HTML')
        delete_message(message, type='media_and_text')
        update_current_state(msg, type='back1', sun_id=current_sun_id)

    else:
        msg = bot.edit_message_media(chat_id=message.from_user.id, message_id=current_message_id, media=types.InputMediaPhoto(current_url_sun[0][0]), reply_markup=markup_inline)
        update_current_state(msg, type='back1', sun_id=current_sun_id)


def show_choose_size_suncatcher_db_more(message, size):
    catalog = get_suncather_catalog(size)
    current_data = get_current_state(message.from_user.id)

    current_number_sun = current_data[1]
    current_message_id = current_data[4]

    current_sun_id = catalog[current_number_sun][0]
    current_sun_title = catalog[current_number_sun][1]
    current_sun_desc = catalog[current_number_sun][2].replace('"выбрать" ⬇️ чтобы заказать', '🎁 <b>Заказать</b>')
    current_sun_price = catalog[current_number_sun][3]
    current_sun_cat = catalog[current_number_sun][4]

    amount_sun = len(catalog)

    current_url_sun = get_url_suncatcher(current_sun_id)

    update_user_path(message, catalog=current_sun_cat, suncatcher_id=current_sun_id)

    media = []

    for url in current_url_sun:
        media.append(types.InputMediaPhoto(url[0]))

    msg_med = bot.send_media_group(message.from_user.id, media)

    markup_inline = types.InlineKeyboardMarkup()

    # item = types.InlineKeyboardButton(text='🎁 Заказать', callback_data='choose1')
    item = types.InlineKeyboardButton(text=f'🎁 Заказать ({current_sun_price[0:4]}р)', callback_data='choose1')
    item2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back1')
    item4 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog1')

    markup_inline.add(item)
    markup_inline.add(item2, item4)

    msg = bot.send_message(message.from_user.id, text=f'🌈☀️ {current_sun_desc}', reply_markup=markup_inline, parse_mode='HTML')

    delete_message(message, type='photo')

    update_current_state(msg_med, type='media', sun_id=current_sun_id)
    update_current_state(msg, type='text', sun_id=current_sun_id)

    
def choose(message, size, step_pre=0):
    catalog = get_suncather_catalog(size)
    current_data = get_current_state(message.from_user.id)

    current_number_sun = current_data[1]
    current_sun_title = catalog[current_number_sun][1]
    current_sun_price = catalog[current_number_sun][3]
    current_message_id = current_data[4]
    current_sun_id = catalog[current_number_sun][0]
    current_url_sun = get_url_suncatcher(current_sun_id)

    text = f'👍 Для заказа <b>{current_sun_title}</b> нажмите: \n\n✍️ <b>Написать</b> - чтобы связаться с мастером и лично обсудить детали заказа и доставки.\n\n🎁 <b>Заказать</b> - чтобы пройти процедуру заказа в автоматическом режиме.'

    markup_inline = types.InlineKeyboardMarkup()

    item = types.InlineKeyboardButton(text='✍️ Написать', url='https://t.me/Lunar_room')
    item2 = types.InlineKeyboardButton(text=f'🎁 Заказать ({current_sun_price[0:4]}р)', callback_data='orderbot')
    # item2 = types.InlineKeyboardButton(text='🎁 Заказать', callback_data='orderbot')
    item3 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back2')
    item4 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')

    markup_inline.add(item2)
    markup_inline.add(item)
    markup_inline.add(item3, item4)

    if step_pre == 'media':
        msg = bot.send_photo(message.from_user.id, current_url_sun[0][0], caption=text, reply_markup=markup_inline, parse_mode='HTML')
        delete_message(message, type='media_and_text')
        update_current_state(msg, type='back1', sun_id=current_sun_id)
    else:
        bot.edit_message_media(chat_id=message.from_user.id, message_id=current_message_id, media=types.InputMediaPhoto(current_url_sun[0][0], caption=text, parse_mode='HTML'), reply_markup=markup_inline)


def step_adress(message):
    current = get_current_state(message.from_user.id)
    order_sun_via_bot(message, step='details_pay', size=current[2])
    bot.delete_message(message.chat.id, message.message_id)


def order_sun_via_bot(message, step, size):
    catalog = get_suncather_catalog(size)
    current_data = get_current_state(message.from_user.id)

    order = {}

    user = get_user(message.from_user.id)

    id_user, name_user, surname_user, nickname_user, adress_user = user[0]

    user_full = f'id: {id_user} \nИмя: {name_user} \nФамилия: {surname_user} \nНик: @{nickname_user} \nАдрес: {adress_user} \n\n'

    current_number_sun = current_data[1]
    current_message_id = current_data[4]
    current_message_admin_id = current_data[7]
    
    current_sun_id = catalog[current_number_sun][0]
    current_sun_title = catalog[current_number_sun][1]
    current_url_sun = get_url_suncatcher(current_sun_id)
    current_sun_price = catalog[current_number_sun][3]

    order['order_user_id'] = id_user
    order['date'] = str(datetime.datetime.now())[0:19]
    order['suncatcher_id'] = current_sun_id
    order['payment_status'] = 'none'
    order['track_number'] = 'none'
    order['delivered_status'] = 'none'
    order['step_order'] = 'none'

    if current_sun_title == 'big' or 'mid':
        cost_ship = '350 рублей'
        size_sun = 'больших и средних'
    else:
        cost_ship = '300 рублей'
        size_sun = 'малых'

    if step == 'orderbot':
        order['step_order'] = 'step1'

        update_order(order)

        script_one_step = f'☀️ <b>{current_sun_title}</b> в наличии. \n\n💰<b>Стоимость</b> - {current_sun_price[0:4]} рублей. \n\n<b>✅ Вы для себя его выбрали или в подарок?</b> '

        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='💁‍♀️ Для себя', callback_data='forme')
        item2 = types.InlineKeyboardButton(text='🎁 В подарок', callback_data='forgift')
        item3 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back2')
        item4 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')
        item5 = types.InlineKeyboardButton(text='✍️ Написать мастеру', url='https://t.me/Lunar_room')

        markup_inline.add(item, item2)
        markup_inline.add(item3, item4)
        markup_inline.add(item5)

        bot.edit_message_media(chat_id=message.from_user.id, message_id=current_message_id,  media=types.InputMediaPhoto(current_url_sun[0][0], caption=script_one_step, parse_mode='HTML'), reply_markup=markup_inline)

        description = f'Пользовтель: \n\n{user_full}Заинтересовался {current_sun_title} и изъявил желание заказать его автоматически'
        msg_admin_id = bot.send_photo(-1001976282334, current_url_sun[0][0], caption=description)

        update_current_state(message, type='order', message_admin_id=msg_admin_id.message_id)

    if step == 'forme':
        order['step_order'] = 'step2'

        update_order(order)

        # update_step_order(step2=step)

        script_one_step = f'🚚 Доставка из Краснодарского края {size_sun} ловцов стоит {cost_ship}. \n\n📦 Отправка почтой России в день заказа, либо на следующий день. \n\n💳 Оплата переводом на Сбербанк или Тинькоф. \n\n<b>✅ Вам подходит?</b>'

        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='✅ Да', callback_data='input_adress')
        item2 = types.InlineKeyboardButton(text='✍️ Нет. Написать мастеру', url='https://t.me/Lunar_room')
        item3 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')

        markup_inline.add(item, item2)
        markup_inline.add(item3)

        bot.edit_message_media(chat_id=message.from_user.id, message_id=current_message_id,  media=types.InputMediaPhoto(current_url_sun[0][0], caption=script_one_step, parse_mode='HTML'), reply_markup=markup_inline)

        description = f'Пользовтель: \n\n{user_full}Выбрал {current_sun_title} для себя'

        bot.edit_message_media(chat_id=-1001976282334, message_id=current_message_admin_id, media=types.InputMediaPhoto(current_url_sun[0][0], caption=description, parse_mode='HTML'))

    if step == 'forgift':
        order['step_order'] = 'step2'

        update_order(order)

        # update_step_order(step2=step)

        script_one_step = f'🎁 <b>{current_sun_title}</b> придёт к вам в подарочной упаковке. К заказу я приложу открытку, которую вы сами сможете подписать. И подарок полностью будет готов к вручению)\n\n🚚 Доставка из Краснодарского края {size_sun} ловцов стоит {cost_ship}. \n\n📦 Отправка почтой России в день заказа, либо на следующий день. \n\n💳 Оплата переводом на Сбербанк или Тинькоф. \n\n<b>✅ Вам подходит?</b>'

        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='✅ Да', callback_data='input_adress')
        item2 = types.InlineKeyboardButton(text='✍️ Нет. Написать мастеру', url='https://t.me/Lunar_room')
        item3 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')

        markup_inline.add(item, item2)
        markup_inline.add(item3)

        bot.edit_message_media(chat_id=message.from_user.id, message_id=current_message_id,  media=types.InputMediaPhoto(current_url_sun[0][0], caption=script_one_step, parse_mode='HTML'), reply_markup=markup_inline)

        description = f'Пользовтель: \n\n{user_full}Выбрал {current_sun_title} в подарок'

        bot.edit_message_media(chat_id=-1001976282334, message_id=current_message_admin_id, media=types.InputMediaPhoto(current_url_sun[0][0], caption=description, parse_mode='HTML'))

        # bot.send_photo(-1001976282334, current_url_sun[0][0], caption=description)

    if step == 'input_adress':

        order['step_order'] = 'step3'

        update_order(order)

        script_one_step = '<b>✅ Отправьте чат-боту адрес, куда нужно доставить, в формате:</b> \n\nГород, улица, № дома, № квартиры, ФИО получателя, Номер телефона получателя. \n\n👉 Просто наберите сообщение в поле ввода и отправьте:'
        
        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')
        item2 = types.InlineKeyboardButton(text='✍️ Написать мастеру', url='https://t.me/Lunar_room')

        markup_inline.add(item, item2)

        msg = bot.edit_message_media(chat_id=message.from_user.id, message_id=current_message_id,  media=types.InputMediaPhoto(current_url_sun[0][0], caption=script_one_step, parse_mode='HTML'), reply_markup=markup_inline)

        bot.register_next_step_handler(msg, step_adress)

    if step == 'details_pay':

        order['step_order'] = 'step4'

        update_order(order)

        finish_cost = int(current_sun_price[0:4]) + int(cost_ship[0:3])
        adress = message.json['text']

        # update_step_order(step3=adress)
        update_table_user(message, adress=adress)

        details_pay = f'👍 Отлично. Почти закончили!\n\n🚚 Доставка <b>{current_sun_title}</b> - {cost_ship} + стоимость ловца солнца - {current_sun_price[0:4]}р.\n\n<b>Итого</b> - {finish_cost} рублей. \n\n💳 Оплату можно перевести на карту Тинькоф или Сбербанк:\n\nПо номеру телефона: <b>89180119741</b> \n\nПолучатель: <b>Оксана Николаевна И.</b>\n\n'
        script_one_step =  f'{details_pay}📬 Ваш адрес:\n\n <b>{adress}</b> \n\n✅ Если всё правильно, оплачивайте и нажимайте оплатил(a). В течении получаса вам придет номер для отслеживания посылки. \n\n‼️ В случае каких-то вопросов, вы всегда можете написать мне лично, нажав в любом месте чат-бота <b>✍️ Написать мастеру</b>'

        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='Оплатил(а)', callback_data='pay_yes')
        # item2 = types.InlineKeyboardButton(text='Проверить трекинг номер', callback_data='none')
        item3 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')
        item4 = types.InlineKeyboardButton(text='✍️ Написать мастеру', url='https://t.me/Lunar_room')

        markup_inline.add(item)
        # markup_inline.add(item2)
        markup_inline.add(item3)
        markup_inline.add(item4)

        bot.edit_message_media(chat_id=message.from_user.id, message_id=current_message_id, media=types.InputMediaPhoto(current_url_sun[0][0], caption=script_one_step, parse_mode='HTML'), reply_markup=markup_inline)

        description = f'Пользовтель: \n\n{user_full}Выбрал {current_sun_title} и ввел адрес: \n\n{adress}'

        bot.edit_message_media(chat_id=-1001976282334, message_id=current_message_admin_id, media=types.InputMediaPhoto(current_url_sun[0][0], caption=description, parse_mode='HTML'))

    if step == 'pay_yes':

        user1 = get_user(message.from_user.id)

        adress = user1[0][4]

        script_one_step = f'🎁 Поздравляю с покупкой <b>{current_sun_title}</b>! \n\nВ течении получаса я оформлю посылку по адресу: \n\n<b>{adress}</b>\n\nи вышлю вам трек-номер. Ожидайте.'

        markup_inline = types.InlineKeyboardMarkup()

        # item = types.InlineKeyboardButton(text='Оплатил(а)', callback_data='pay_yes')
        # item2 = types.InlineKeyboardButton(text='Проверить трекинг номер', callback_data='none')
        item3 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')
        item4 = types.InlineKeyboardButton(text='✍️ Написать мастеру', url='https://t.me/Lunar_room')
        # item5 = types.InlineKeyboardButton(text='📦 Проверить трек-номер', callback_data='check_track')

        markup_inline.add(item3)
        # markup_inline.add(item2)
        markup_inline.add(item4)
        # markup_inline.add(item5)

        bot.edit_message_media(chat_id=message.from_user.id, message_id=current_message_id, media=types.InputMediaPhoto(current_url_sun[0][0], caption=script_one_step, parse_mode='HTML'), reply_markup=markup_inline)

        
        markup_inline2 = types.InlineKeyboardMarkup()
        item_user = types.InlineKeyboardButton(text='Отправить трек номер', callback_data='send_track')
        markup_inline2.add(item_user)
        description = f'Пользовтель: \n\n{user_full}Выбрал {current_sun_title} и нажал кнопку ОПЛАТИЛ(A)'

        msg = bot.edit_message_media(chat_id=-1001976282334, message_id=current_message_admin_id, media=types.InputMediaPhoto(current_url_sun[0][0], caption=f'{description}\n\n Отправь трек-номер, указав вначале сообщения id, например: 24352345, трек-номер для отслеживания - 313543:', parse_mode='HTML'))

        bot.register_next_step_handler(msg, send_track)


def send_track(message):
    str = message.text
    id = str.partition(',')[0]
    track_number = str.partition(',')[2]

    order = {}

    current_data = get_current_state(id)

    catalog = get_suncather_catalog(current_data[2])

    current_message_id = current_data[4]
    current_number_sun = current_data[1]
    current_message_id = current_data[4]

    current_sun_id = catalog[current_number_sun][0]
    current_sun_title = catalog[current_number_sun][1]
    current_url_sun = get_url_suncatcher(current_sun_id)
    current_sun_price = catalog[current_number_sun][3]


    markup_inline = types.InlineKeyboardMarkup()

    item3 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')
    item4 = types.InlineKeyboardButton(text='✍️ Написать мастеру', url='https://t.me/Lunar_room')

    markup_inline.add(item3)
    markup_inline.add(item4)

    # bot.send_message(user['id'], text=f'В чат-боте произошли обновления. Чтобы посмотреть изменения, вам нужно перезапустить бота. \n\nНажмите /start')

    msg = bot.send_photo(id, current_url_sun[0][0], caption=f'Спасибо за покупку! \n\nВаш трек-номер:<b>{track_number}</b>', reply_markup=markup_inline, parse_mode='HTML')

    print('dddddd', msg)

    bot.delete_message(id, current_message_id)

    update_current_state(msg, type='start')

    order_data = get_order(id)[0]

    order['order_user_id'] = order_data[0]
    order['date'] = order_data[1]
    order['suncatcher_id'] = order_data[2]
    order['payment_status'] = 'true'
    order['track_number'] = track_number
    order['delivered_status'] = 'in transit'
    order['step_order'] = 'finish'

    update_order(order)


@bot.message_handler(commands=['start'])
def start(message):

    try:
        delete_message(message, type='photo')
    except:
        print('oops1')

    try:
        delete_message(message, type='media_and_text')
    except:
        print('oops1')

    update_table_press_start(message.from_user.id)

    update_table_user(message)

    bot.delete_message(message.from_user.id, message.message_id)

    user_name = message.from_user.first_name if message.from_user.first_name else message.from_user.username

    text_message = f'✨ Привет, {user_name}! \n\n🌈 Добро пожаловать в <b>каталог</b> с ловцами солнца! \n\n✅ Вы можете посмотреть здесь наличие.\n\n‼️ А если выберете цветочную луну по душе, то чат-бот пришлёт вам инструкцию, как заказать ловец солнца.'

    url_photo = Path("suncatcher/admin_file/oksa.jpg")
    img = open(url_photo, 'rb')
    markup_inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text='✨ Каталог', callback_data='catalog')
    item4 = types.InlineKeyboardButton(text='✍️ Написать мастеру', url='https://t.me/Lunar_room')
    
    markup_inline.add(item1)
    markup_inline.add(item4)

    msg = bot.send_photo(message.from_user.id, img, caption=text_message, reply_markup=markup_inline, parse_mode='HTML')
    
    update_current_state(msg, type='start')

# отправка сообщения через file_id
#     img_list = []
#     img_list.append(types.InputMediaPhoto('AgACAgIAAxkDAAIkWGRffWPqBs072UfzyHs0L8YXXN2kAAKMxzEbTwfpSmHSqPFF3PHiAQADAgADcwADLwQ'))
#     bot.send_media_group(message.from_user.id, img_list)

    
@bot.message_handler(commands=['создать_таблицы'])
def start(message):
    if message.from_user.id == 257930228:
        create_table_all()
        update_patch()
        print('admin создал и обновил все таблицы')


@bot.callback_query_handler(func=lambda m: True)
def callback_choice(message):
    t = message.data

    if t == 'catalog':
        update_user_path(message, catalog='catalog')
        update_current_state(message, type='catalog')
        show_catalog(message)

    if t == 'catalog1':
        update_user_path(message, catalog='catalog')
        update_current_state(message, type='catalog')
        show_catalog(message, step_pre='media')

    if t == 'big':
        update_user_path(message, catalog='big')
        update_current_state(message, type='big')
        show_choose_size_suncatcher_db(message, t)

    if t == 'mid':
        update_user_path(message, catalog='mid')
        update_current_state(message, type='mid')
        show_choose_size_suncatcher_db(message, t)

    if t == 'low':
        update_user_path(message, catalog='low')
        update_current_state(message, type='low')
        show_choose_size_suncatcher_db(message, t)

    if t == 'next':
        current = get_current_state(message.from_user.id)
        update_current_state(message, type='next')
        show_choose_size_suncatcher_db(message, size=current[2])

    if t == 'back':
        current = get_current_state(message.from_user.id)
        update_current_state(message, type='back')
        show_choose_size_suncatcher_db(message, size=current[2])

    if t == 'more':
        current = get_current_state(message.from_user.id)
        show_choose_size_suncatcher_db_more(message, size=current[2])

    if t == 'choose':
        current = get_current_state(message.from_user.id)
        choose(message, size=current[2])

# Когда предыдущий шаг формирует сообщение из группы картинок, метод edit_message не подходит. Поэтому приходится удалять сообщение и отправлять новое. Это касается всех функций с параметром step_pre.
    if t == 'choose1':
        current = get_current_state(message.from_user.id)
        choose(message, size=current[2], step_pre='media')

    if t == 'back1':
        current = get_current_state(message.from_user.id)
        show_choose_size_suncatcher_db(message, size=current[2], step_pre='media')

    if t == 'back2':
        current = get_current_state(message.from_user.id)
        show_choose_size_suncatcher_db(message, size=current[2])

    if t == 'orderbot':
        current = get_current_state(message.from_user.id)
        order_sun_via_bot(message, step=t, size=current[2])

    if t == 'forme':
        current = get_current_state(message.from_user.id)
        order_sun_via_bot(message, step=t, size=current[2])

    if t == 'forgift':
        current = get_current_state(message.from_user.id)
        order_sun_via_bot(message, step=t, size=current[2])

    if t == 'input_adress':
        current = get_current_state(message.from_user.id)
        order_sun_via_bot(message, step=t, size=current[2])

    if t == 'pay_yes':
        current = get_current_state(message.from_user.id)
        order_sun_via_bot(message, step=t, size=current[2])

    if t == 'send_track':
        send_track()


bot.infinity_polling()


def main():
    pass


if __name__ == '__main__':
    main()