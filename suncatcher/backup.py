# реализация с распаковкой кнопок в цикле
def show_mid_suncatcher(message):
    i = 1
    item = []
    reply_markup=types.ReplyKeyboardRemove()
    markup_inline = types.InlineKeyboardMarkup()
    for elem in data['items']:

        text_message = "Привет, это средние ловцы"
        url_photo = elem['thumb_photo']
        print(elem['title'])
        discount = elem.get('discount_rate')
        
        
        if elem['title'] != 'Доставка' and (25000 < int(elem['price']['amount']) < 350000):
            print(elem['title'])
            item.append(types.InlineKeyboardButton(text = i, callback_data = elem['title'][0:3]))
            i+=1
        
    markup_inline.row(*item)
    markup_inline.add(types.InlineKeyboardButton(text = 'Посмотреть каталог товаров', callback_data = 'Каталог'))
    markup_inline.add(types.InlineKeyboardButton(text = 'Написать мне', url = 'https://t.me/Lunar_room'))

    bot.send_photo(message.from_user.id, url_photo, caption=text_message, reply_markup=markup_inline)



# для вывода ловцов списком 1-ый вариант

def show_big_suncatcher(message):
    for elem in data['items']:
        description = elem['title'] + '\n\n' + elem['description'] + '\n\n' + 'Стоимость - ' + elem['price']['amount'][0:4] + ' ' + elem['price']['currency']['name']
        title = elem['title']
        url_photo = elem['thumb_photo']
        markup_inline = types.InlineKeyboardMarkup()

        if elem['title'] != 'Доставка' and int(elem['price']['amount']) > 310000: 
            item = types.InlineKeyboardButton(text = "Заказать", callback_data = elem['title'][0:3])
            item2 = types.InlineKeyboardButton(text = 'Написать мне', url = 'https://t.me/Lunar_room')
            markup_inline.add(item)
            markup_inline.add(item2)
            bot.send_photo(message.from_user.id, url_photo, caption=description, reply_markup=markup_inline)


def show_mid_suncatcher(message):
    for elem in data['items']:
        description = elem['title'] + '\n\n' + elem['description'] + '\n\n' + 'Стоимость - ' + elem['price']['amount'][0:4] + ' ' + elem['price']['currency']['name']
        title = elem['title']
        url_photo = elem['thumb_photo']
        markup_inline = types.InlineKeyboardMarkup()

        if elem['title'] != 'Доставка' and (29000 < int(elem['price']['amount']) < 310000):
            item = types.InlineKeyboardButton(text = "Заказать", callback_data = elem['title'][0:3])
            item2 = types.InlineKeyboardButton(text = 'Написать мне', url = 'https://t.me/Lunar_room')
            markup_inline.add(item)
            markup_inline.add(item2)
            bot.send_photo(message.from_user.id, url_photo, caption=description, reply_markup=markup_inline)


def show_low_suncatcher(message):
    is_low = 0
    for elem in data['items']:
        description = elem['title'] + '\n\n' + elem['description'] + '\n\n' + 'Стоимость - ' + elem['price']['amount'][0:4] + ' ' + elem['price']['currency']['name']
        title = elem['title']
        url_photo = elem['thumb_photo']
        markup_inline = types.InlineKeyboardMarkup()

        if elem['title'] != 'Доставка' and (int(elem['price']['amount']) < 29000):
            is_low += 1
            item = types.InlineKeyboardButton(text = "Заказать", callback_data = elem['title'][0:3])
            item2 = types.InlineKeyboardButton(text = 'Написать мне', url = 'https://t.me/Lunar_room')
            markup_inline.add(item)
            markup_inline.add(item2)
            bot.send_photo(message.from_user.id, url_photo, caption=description, reply_markup=markup_inline)
        
    if is_low == 0:
        text = "Сейчас все малые ловцы закончились. Подпишитесь на канал и ожидайте новой коллекции."
        markup_inline = types.InlineKeyboardMarkup()
        item = types.InlineKeyboardButton(text = 'Подписаться на канал', url = 'https://t.me/moonroomart')
        markup_inline.add(item)
        bot.send_message(message.from_user.id, text, reply_markup=markup_inline)