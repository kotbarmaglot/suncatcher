from .config import API_KEY
from .vksunbot import get_moon, get_moon_amount
import telebot
import json
from telebot import types
from pathlib import Path


bot = telebot.TeleBot(API_KEY)


def save_message_chat_id(message):
    user_id = message.chat.id
    user_patch = Path(f"suncatcher/user_file/{user_id}.json")

    print('save message', message)

    with open(user_patch, "r") as read_file:
        user_data = json.load(read_file)

    user_data['id_mes'] = message.message_id
    user_data['id_chat'] = message.chat.id

    with open(user_patch, "w") as write_file:
        json.dump(user_data, write_file)


def get_message_chat_id(message):
    user_id = message.from_user.id
    user_patch = Path(f"suncatcher/user_file/{user_id}.json")

    with open(user_patch, "r") as read_file:
        user_data = json.load(read_file)

    return user_data['id_mes'], user_data['id_chat']


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
    user_data['id_chat'] = 0

    with open(user_patch, "w") as write_file:
        json.dump(user_data, write_file)

    return user_data


def show_catalog(message):
    title = 'Какие ловцы солнца вы хотите посмотреть:\n\n'
    big_sun = '1. Ловцы общей длиной 40 см и больше, стоимостью 4000р.\n\n'
    mid_sun = '2. Ловцы длиной ~ 30 см, стоимостью 3000р.\n\n'
    low_sun = '3. Ловцы длиной ~ 20 см, стоимостью 2000р.\n\n'

    text = f"{title}{big_sun}{mid_sun}{low_sun}"

    markup_inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Большие ловцы", callback_data='big')
    item2 = types.InlineKeyboardButton("Средние ловцы", callback_data='mid')
    item3 = types.InlineKeyboardButton("Малые ловцы", callback_data='low')

    url_photo = 'https://sun9-42.userapi.com/impg/V7H81niHXYdgP2M_ZqbL4lRvuwGQGajdTvkdYw/KqT-wWKWTHw.jpg?size=2560x2560&quality=95&sign=79eab711010666d1651f6001fdf322d9&type=album'

    markup_inline.add(item1)
    markup_inline.add(item2)
    markup_inline.add(item3)

    msg = bot.send_photo(message.from_user.id, url_photo, caption=text, reply_markup=markup_inline)

    save_message_chat_id(msg)

    print(msg)


def show_choose_size_suncatcher(message, number_sun, size):

    big = get_moon(size)

    current_number, type, all_sun = get_current_number_size_sun(message)

    print(big)
    print(current_number)

    url_photo = big[size][number_sun]['url_photo'][0]
    count = f'{size}_count'
    current_sun_text = f'{current_number+1}/{big[count]}'
    description = big[size][number_sun]['description'] + current_sun_text

    markup_inline = types.InlineKeyboardMarkup()

    if current_number+1 == big[count]:
        item = types.InlineKeyboardButton(text='Описание/Фото', callback_data='more')
        item2 = types.InlineKeyboardButton(text='⬅️', callback_data='back')
        item3 = types.InlineKeyboardButton(text='⛔️', callback_data='none')
        item4 = types.InlineKeyboardButton(text='Каталог', callback_data='catalog')
        item5 = types.InlineKeyboardButton(text=f'{current_sun_text}', callback_data='none')

        markup_inline.add(item2, item5, item3)
        markup_inline.add(item)
        markup_inline.add(item4)

    if current_number+1 == 1:
        item = types.InlineKeyboardButton(text='Описание/Фото', callback_data='more')
        item2 = types.InlineKeyboardButton(text='⛔️', callback_data='none')
        item3 = types.InlineKeyboardButton(text='➡️', callback_data='next')
        item4 = types.InlineKeyboardButton(text='Каталог', callback_data='catalog')
        item5 = types.InlineKeyboardButton(text=f'{current_sun_text}', callback_data='none')

        markup_inline.add(item2, item5, item3)
        markup_inline.add(item)
        markup_inline.add(item4)

    if 1 < current_number+1 < big[count]:
        item = types.InlineKeyboardButton(text='Описание/Фото', callback_data='more')
        item2 = types.InlineKeyboardButton(text='⬅️', callback_data='back')
        item3 = types.InlineKeyboardButton(text='➡️', callback_data='next')
        item4 = types.InlineKeyboardButton(text='Каталог', callback_data='catalog')
        item5 = types.InlineKeyboardButton(text=f'{current_sun_text}', callback_data='none')

        markup_inline.add(item2, item5, item3)
        markup_inline.add(item)
        markup_inline.add(item4)

    ms, ch = get_message_chat_id(message)

    bot.delete_message(message.from_user.id, ms)
    

    msg = bot.send_photo(message.from_user.id, url_photo,  reply_markup=markup_inline)

    save_message_chat_id(msg)


def show_choose_size_suncatcher_more(message, number_sun, size):
    
    big = get_moon(size)

    current_number, type, all_sun = get_current_number_size_sun(message)

    print(big)
    print(current_number)

    url_photo = big[size][number_sun]['url_photo'][0]
    count = f'{size}_count'
    current_sun_text = f'{current_number+1}/{big[count]}'
    description = big[size][number_sun]['description'] + current_sun_text

    markup_inline = types.InlineKeyboardMarkup()

    item = types.InlineKeyboardButton(text='Заказать', url='https://t.me/Lunar_room')
    item4 = types.InlineKeyboardButton(text='Каталог', callback_data='catalog')

    markup_inline.add(item)
    markup_inline.add(item4)

    ms, ch = get_message_chat_id(message)

    bot.delete_message(message.from_user.id, ms)
    
    msg = bot.send_photo(message.from_user.id, url_photo, caption=description, reply_markup=markup_inline)

    save_message_chat_id(msg)


def mid_suncatcher(message):
    pass


def low_suncatcher(message):
    pass


@bot.message_handler(commands=['start'])
def start(message):
    print('start', message)

    create_or_get_user_file(message)

    user_name = message.from_user.first_name
    text_message = "Привет, " + f"{user_name}!" + "\n\nМеня зовут Оксана. Я создательница ловцов солнца. Хочешь я покажу тебе каталог товаров?"
    url_photo = "https://sun9-54.userapi.com/impg/vnK5xGTaFNIB8DjusXniXDLUweZ8mp9O9H398g/d9_He-KNepo.jpg?size=1440x2160&quality=95&sign=ead03b10d6230c7a345507663da80d7f&type=album"
    markup_inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text='Каталог', callback_data='catalog')
    markup_inline.add(item1)
    msg = bot.send_photo(message.from_user.id, url_photo, caption=text_message, reply_markup=markup_inline)

    save_message_chat_id(msg)


@bot.callback_query_handler(func=lambda m: True)
def callback_choice(message):
    t = message.data

    if t == 'catalog':
        ms, ch = get_message_chat_id(message)
        bot.delete_message(message.from_user.id, ms)

        set_current_size_sun(message, size='')
        show_catalog(message)
        set_current_number_sun(message, current=0, size='big')
        set_current_number_sun(message, current=0, size='mid')
        set_current_number_sun(message, current=0, size='low')

    if t == 'big':
        set_current_size_sun(message, t)
        show_choose_size_suncatcher(message, number_sun=0, size=t)

    if t == 'mid':
        set_current_size_sun(message, t)
        show_choose_size_suncatcher(message, number_sun=0, size=t)

    if t == 'low':
        set_current_size_sun(message, t)
        show_choose_size_suncatcher(message, number_sun=0, size=t)

    if t == 'next':
        number, size, all = get_current_number_size_sun(message)
        print(number)
        set_current_number_sun(message, current=number+1, size=size)
        show_choose_size_suncatcher(message, number_sun=number+1, size=size)

    if t == 'back':
        number, size, all = get_current_number_size_sun(message)
        print(number)
        set_current_number_sun(message, current=number-1, size=size)
        show_choose_size_suncatcher(message, number_sun=number-1, size=size)

    if t == 'more':
        number, size, all = get_current_number_size_sun(message)
        show_choose_size_suncatcher_more(message, number_sun=number, size=size)


# @bot.message_handler(func=lambda m: True)
# def handler(message):

#     t = message.text

#     if t == 'Каталог':
#         set_current_size_sun(message, size='')
#         show_catalog(message)
#         set_current_number_sun(message, current=0, size='big')
#         set_current_number_sun(message, current=0, size='mid')
#         set_current_number_sun(message, current=0, size='low')
        


#     if t == "Средние ловцы":
#         mid_suncatcher(message)

#     if t == "Малые ловцы":
#         low_suncatcher(message)

bot.infinity_polling()


def main():
    pass


if __name__ == '__main__':
    main()