from .config import API_KEY
from .vksunbot import *
import telebot
import json
from telebot import types
from telebot.types import InputMediaPhoto


bot = telebot.TeleBot(API_KEY)

with open("info_product.json", "r") as read_file:
    data = json.load(read_file)


def fill_big_lunnica(message):
    description, title, url_photo, id_product = get_big_lunnica(data, message)
    print(description, title, url_photo)

    markup_inline = types.InlineKeyboardMarkup()

    item = types.InlineKeyboardButton(text = '🎁 Выбрать ✍️ Написать мастеру', url = 'https://t.me/Lunar_room')
    item2 = types.InlineKeyboardButton(text = '⭐️ В избранное', callback_data = 'big_lunnicy')

    markup_inline.add(item)
    markup_inline.add(item2)

    pic1 = 'https://sun6-23.userapi.com/impg/pRg4gqwTFhHSqBb5Do8_CbAh6gDl3gz86DC_Qw/UmSErGTB0f8.jpg?size=1080x1079&quality=95&sign=12ff1fd6996900453e878b3db40cf1b8&type=album'

    pic2 = 'https://sun9-78.userapi.com/impg/_Y9m20t7FWYNtloSaiJi1yb0X8_Tcn47rljT9Q/80WHFlMFpdk.jpg?size=2560x2560&quality=95&sign=3f8255c76872459ae10bce313d0abddc&type=album'

    media = [InputMediaPhoto(pic1, caption="test"), InputMediaPhoto(pic2)]
    bot.send_media_group(message.from_user.id, media)

    # bot.send_photo(message.from_user.id, url_photo[0], caption=description[0], reply_markup=markup_inline)


def big_suncatcher(message):
    description = "Большие ловцы солнца – общая длина с фурнитурой ~ 40 см, а размер цветочной основы 20 см."
    url_photo = "https://sun9-42.userapi.com/impg/V7H81niHXYdgP2M_ZqbL4lRvuwGQGajdTvkdYw/KqT-wWKWTHw.jpg?size=2560x2560&quality=95&sign=79eab711010666d1651f6001fdf322d9&type=album"

    markup_inline = types.InlineKeyboardMarkup()

    item = types.InlineKeyboardButton(text = 'Луны', callback_data = 'big_moon')
    item2 = types.InlineKeyboardButton(text = 'Лунницы', callback_data = 'big_lunnicy')
    item3 = types.InlineKeyboardButton(text = 'Фазы луны', callback_data = 'big_fazy')
    item4 = types.InlineKeyboardButton(text = 'Круги', callback_data = 'big_circle')
    item5 = types.InlineKeyboardButton(text = 'Сердца', callback_data = 'big_hearts')
    item6 = types.InlineKeyboardButton(text = 'Звёзды', callback_data = 'big_stars')

    markup_inline.add(item)
    markup_inline.add(item2)
    markup_inline.add(item3)
    markup_inline.add(item4)
    markup_inline.add(item5)
    markup_inline.add(item6)

    bot.send_photo(message.from_user.id, url_photo, caption=description, reply_markup=markup_inline)


def mid_suncatcher(message):
    description = "Средние ловцы солнца – общая длина с фурнитурой ~ 30 см, а размер цветочной основы 15 см."
    url_photo = "https://sun9-42.userapi.com/impg/V7H81niHXYdgP2M_ZqbL4lRvuwGQGajdTvkdYw/KqT-wWKWTHw.jpg?size=2560x2560&quality=95&sign=79eab711010666d1651f6001fdf322d9&type=album"

    markup_inline = types.InlineKeyboardMarkup()

    item = types.InlineKeyboardButton(text = 'Луны', callback_data = 'mid_moon')
    item2 = types.InlineKeyboardButton(text = 'Лунницы', callback_data = 'mid_lunnicy')
    item3 = types.InlineKeyboardButton(text = 'Круги', callback_data = 'mid_circle')
    item4 = types.InlineKeyboardButton(text = 'Сердца', callback_data = 'mid_hearts')
    item5 = types.InlineKeyboardButton(text = 'Звёзды', callback_data = 'mid_stars')

    markup_inline.add(item)
    markup_inline.add(item2)
    markup_inline.add(item3)
    markup_inline.add(item4)
    markup_inline.add(item5)

    bot.send_photo(message.from_user.id, url_photo, caption=description, reply_markup=markup_inline)


def low_suncatcher(message):
    description = "Ловцы солнца малые – общая длина с фурнитурой ~ 20 см, а размер цветочной основы 10 см."
    url_photo = "https://sun9-42.userapi.com/impg/V7H81niHXYdgP2M_ZqbL4lRvuwGQGajdTvkdYw/KqT-wWKWTHw.jpg?size=2560x2560&quality=95&sign=79eab711010666d1651f6001fdf322d9&type=album"

    markup_inline = types.InlineKeyboardMarkup()

    item = types.InlineKeyboardButton(text = 'Луны', callback_data = 'low_moon')
    item2 = types.InlineKeyboardButton(text = 'Лунницы', callback_data = 'low_lunnicy')
    item3 = types.InlineKeyboardButton(text = 'Круги', callback_data = 'low_circle')
    item4 = types.InlineKeyboardButton(text = 'Сердца', callback_data = 'low_hearts')
    item5 = types.InlineKeyboardButton(text = 'Звёзды', callback_data = 'low_stars')

    markup_inline.add(item)
    markup_inline.add(item2)
    markup_inline.add(item3)
    markup_inline.add(item4)
    markup_inline.add(item5)

    bot.send_photo(message.from_user.id, url_photo, caption=description, reply_markup=markup_inline)


@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    text_message = "Привет, " + f"{message.from_user.first_name}!" + "\n\nМеня зовут Оксана. Я создательница ловцов солнца. Хочешь я покажу тебе каталог товаров?"
    url_photo = "https://sun9-54.userapi.com/impg/vnK5xGTaFNIB8DjusXniXDLUweZ8mp9O9H398g/d9_He-KNepo.jpg?size=1440x2160&quality=95&sign=ead03b10d6230c7a345507663da80d7f&type=album"
    markup_inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text = 'Посмотреть каталог товаров', callback_data = 'Каталог')
    item2 = types.InlineKeyboardButton(text = 'Написать мне', url = 'https://t.me/Lunar_room')
    markup_inline.add(item1)
    markup_inline.add(item2)
    bot.send_photo(message.from_user.id, url_photo, caption=text_message, reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda m: True)
def callback_choice(message):
    t = message.data
    print(t)

    if t == 'Каталог':
        big_sun = "Большие ловцы - размер 35см. Стоимость 4т.р.\n\n"
        mid_sun = "Средние ловцы - размер 35см. Стоимость 4т.р.\n\n"
        low_sun = 'Маленькие ловцы - размер 35см. Стоимость 4т.р.\n\n'
        text = "Выбери свой ловец солнца \n\n" + f"{big_sun}{mid_sun}{low_sun}"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Большие ловцы")
        item2=types.KeyboardButton("Средние ловцы")
        item3=types.KeyboardButton("Малые ловцы")
        item4=types.KeyboardButton("Акции")
        # item5=types.KeyboardButton("Показать всё наличие")

        markup.add(item1, item2)
        markup.add(item3, item4)
        # markup.add(item5)

        msg = bot.send_message(message.from_user.id, text, reply_markup=markup)
    
    if t == 'big_moon':
        x = get_big_moon(data, message)
        print(x)
        # print('big_moon')

    if t == 'mid_moon':

        
        print('mid_moon')
    
    if t == 'low_moon':
        print('low_moon')

    if t == 'big_lunnicy':
        fill_big_lunnica(message)

    if t == 'mid_lunnicy':
        print('mid_lunnicy')
    
    if t == 'low_lunnicy':
        print('low_lunnicy')

    if t == 'big_fazy':
        print('big_fazy')

    if t == 'mid_fazy':
        print('mid_fazy')
    
    if t == 'low_fazy':
        print('low_fazy')


@bot.message_handler(func=lambda m: True)
def main(message):
    t = message.text

    if t == 'Большие ловцы':
        big_suncatcher(message)

    if t == "Средние ловцы":
        mid_suncatcher(message)

    if t == "Малые ловцы":
        low_suncatcher(message)

    if t == "Акции":
        pass

    if t == "Показать всё наличие":
        pass



bot.infinity_polling() 


def main():
    pass


if __name__ == '__main__':
    main()