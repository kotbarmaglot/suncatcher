import sqlite3
from .vksunbot import get_catalog_vk
import datetime
import json


def create_table_all():
    create_table_user()
    create_table_suncatcher()
    create_table_suncatcher_photo()
    create_table_press_start()
    create_table_current_state()
    create_table_user_path()
    create_table_order()
    create_table_step_order()


def create_table_user():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 0')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `user`')
    con.execute('PRAGMA foreign_keys = 1')

    cur.execute("""
        CREATE TABLE `user`(
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            nickname TEXT NOT NULL,
            adress TEXT NOT NULL
        )""")
    
    con.commit()
    con.close()


def update_table_user(message, adress='none'):
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    user = {}

    user['id'] = message.from_user.id
    user['name'] = message.from_user.first_name if message.from_user.first_name else 'none'
    user['surname'] = message.from_user.last_name if message.from_user.last_name else 'none'
    user['nickname'] = message.from_user.username if message.from_user.username else 'none'
    user['adress'] = adress

    cur.execute("""INSERT OR REPLACE INTO `user` (id, name, surname, nickname, adress) VALUES(:id, :name, :surname, :nickname, :adress)""", user)

    con.commit()
    con.close()


def create_table_press_start():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 0')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `press_start`')
    con.execute('PRAGMA foreign_keys = 1')

    cur.execute("""
        CREATE TABLE `press_start` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )""")
    con.commit()
    con.close()


def update_table_press_start(id):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()
    current_data = {}

    current_data['user_id'] = id
    current_data['date'] = str(datetime.datetime.now())[0:19]

    cur.execute(f"INSERT OR REPLACE INTO press_start(user_id, date) values(:user_id, :date)", current_data).fetchall()

    con.commit()
    con.close()


def get_table_press_start(id):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT * FROM press_start WHERE user_id={id}").fetchall()

    con.close()

    return res


def create_table_current_state():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 0')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `current_state`')
    con.execute('PRAGMA foreign_keys = 1')

    cur.execute("""
        CREATE TABLE `current_state` (
            user_id INTEGER PRIMARY KEY NOT NULL,
            current_number INTEGER NOT NULL,
            current_catalog TEXT NULL,
            suncatcher_current_id INTEGER NULL,
            message_photo_id INTEGER NULL,
            message_meda_id TEXT NULL,
            message_text_id INTEGER NULL,
            message_admin_id INTEGER NULL,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (suncatcher_current_id) REFERENCES suncatcher(id)
        )""")
    con.commit()
    con.close()

 
def create_table_user_path():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 0')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `user_path`')
    con.execute('PRAGMA foreign_keys = 1')

    cur.execute("""
        CREATE TABLE `user_path` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            catalog TEXT NOT NULL,
            suncatcher_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (suncatcher_id) REFERENCES suncatcher(id)
        )""")
    con.commit()
    con.close()


def update_user_path(message, catalog, suncatcher_id=0):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()
    current_data = {}

    user_id = message.from_user.id

    current_data['user_id'] = user_id
    current_data['date'] = str(datetime.datetime.now())[0:19]
    current_data['catalog'] = catalog
    current_data['suncatcher_id'] = suncatcher_id

    cur.execute(f"INSERT OR REPLACE INTO user_path(user_id, date, catalog, suncatcher_id) values(:user_id, :date, :catalog, :suncatcher_id)", current_data).fetchall()

    con.commit()
    con.close()


def get_user_path(id):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT * FROM user_path WHERE user_id={id}").fetchall()

    con.close()

    return res


def create_table_suncatcher():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 0')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `suncatcher`')
    con.execute('PRAGMA foreign_keys = 1')

    cur.execute("""
        CREATE TABLE `suncatcher` (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price TEXT NOT NULL,
            catalog TEXT NOT NULL,
            available TEXT NOT NULL
        )""")
    con.commit()
    con.close()


def insert_table_suncatcher():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    create_table_suncatcher()

    catalog_vk = get_catalog_vk()
    category = ['big', 'mid', 'low']

    for cat in category:
        for elem in catalog_vk[cat]:
            elem['catalog'] = cat
            elem['available'] = 'true'
            cur.execute("INSERT OR IGNORE INTO suncatcher(id, title, description, price, catalog, available) VALUES(:id, :title, :description, :price, :catalog, :available)", elem)
    con.commit()
    con.close()


def get_amount_suncatcher():
    insert_table_suncatcher()
    amount = {}
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    res = cur.execute("SELECT catalog, count(*) FROM suncatcher GROUP BY catalog").fetchall()

    for elem in res:
        size, number = elem
        amount[size] = number

    con.close()

    return amount


def create_table_suncatcher_photo():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 0')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `suncatcher_photo`')

    con.execute('PRAGMA foreign_keys = 1')

    cur.execute("""
        CREATE TABLE `suncatcher_photo` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suncatcher_photo_id INTEGER NOT NULL,
            url_photo TEXT NOT NULL,
            FOREIGN KEY (suncatcher_photo_id) REFERENCES suncatcher(id)
        )""")
    con.commit()
    con.close()


def insert_table_suncatcher_photo():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    catalog_vk = get_catalog_vk()
    category = ['big', 'mid', 'low']
    sun_photo = {}

    for cat in category:
        for elem in catalog_vk[cat]:
            for url in elem['url_photo']:
                
                sun_photo['id'] = elem['id']
                sun_photo['url_photo'] = url
                cur.execute("INSERT OR IGNORE INTO suncatcher_photo(suncatcher_photo_id, url_photo) VALUES(:id, :url_photo)", sun_photo)
    con.commit()
    con.close()


def create_table_order():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 0')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `order`')

    con.execute('PRAGMA foreign_keys = 1')

    cur.execute("""
        CREATE TABLE `order` (
            order_user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            suncatcher_id INTEGER PRIMARY KEY,
            payment_status TEXT NOT NULL,
            track_number TEXT NOT NULL,
            delivered_status TEXT NOT NULL,
            step_order TEXT NOT NULL,
            FOREIGN KEY (order_user_id) REFERENCES user(id),
            FOREIGN KEY (suncatcher_id) REFERENCES suncatcher(id)
        )""")
    con.commit()
    con.close()


def create_table_step_order():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 0')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `step_order`')

    con.execute('PRAGMA foreign_keys = 1')

    cur.execute("""
        CREATE TABLE `step_order` (
            order_id INTEGER PRIMARY KEY,
            step1 TEXT NOT NULL,
            step2 TEXT NOT NULL,
            step3 TEXT NOT NULL,
            step4 TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES `order`(id)
        )""")
    con.commit()
    con.close()


def get_suncather_catalog(size='all'):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()

    if size != 'all':
        res = cur.execute(f"SELECT * FROM suncatcher WHERE catalog='{size}' AND available='true'").fetchall()
    else:
        res = cur.execute(f"SELECT * FROM suncatcher").fetchall()

    con.close()

    return res


def get_current_state(id):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM current_state WHERE user_id={id}").fetchone()
    con.close()

    con.close()

    return res


def update_step_order(order_id, step):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()
    current_data = {}

    current_data['order_id'] = order_id
    current_data['step1'] = 'none'
    current_data['step2'] = 'none'
    current_data['step3'] = 'none'
    current_data['step4'] = 'none'

    cur.execute(f"INSERT OR REPLACE INTO `step_order`(order_id, step1, step2, step3, step4) values(:order_id, :step1, :step2, :step3, :step4)", current_data).fetchall()

    con.commit()
    con.close()


def update_order(data):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()
    current_data = {}

    current_data['order_user_id'] = data['order_user_id']
    current_data['date'] = data['date']
    current_data['suncatcher_id'] = data['suncatcher_id']
    current_data['payment_status'] = data['payment_status']
    current_data['track_number'] = data['track_number']
    current_data['delivered_status'] = data['delivered_status']
    current_data['step_order'] = data['step_order']


    cur.execute(f"INSERT OR REPLACE INTO `order`(order_user_id, date, suncatcher_id, payment_status, track_number, delivered_status, step_order) values(:order_user_id, :date, :suncatcher_id, :payment_status, :track_number, :delivered_status, :step_order)", current_data).fetchall()

    con.commit()
    con.close()

def get_order(id):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM `order` WHERE order_user_id={id}").fetchall()
    con.close()

    return res


def update_current_state(message, type='start', sun_id=0, message_admin_id=0):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()
    current_data = {}

    if type == 'start' or type == 'text':
        current_user_id = message.chat.id
    elif type == 'media':
        for elem in message:
            current_user_id = elem.chat.id
    elif type == 'back1':
        current_user_id = message.chat.id
    else:
        current_user_id = message.from_user.id

    data = get_current_state(current_user_id)
    
    if data:
        current_data['user_id'] = current_user_id
        current_data['current_number'] = data[1]
        current_data['current_catalog'] = data[2]
        current_data['suncatcher_current_id'] = sun_id
        current_data['message_photo_id'] = data[4]
        current_data['message_meda_id'] = data[5]
        current_data['message_text_id'] = data[6]
        current_data['message_admin_id'] = message_admin_id

    if type == 'catalog':
        current_data['current_number'] = 0

    if type == 'back1':
        current_data['message_photo_id'] = message.id

    if type == 'order':
        current_data['suncatcher_current_id'] = data[3]
        current_data['message_admin_id'] = message_admin_id

    if type == 'start':
        current_data['user_id'] = current_user_id
        current_data['current_number'] = 0
        current_data['current_catalog'] = 'start'
        current_data['suncatcher_current_id'] = sun_id
        current_data['message_photo_id'] = message.id
        current_data['message_meda_id'] = ''
        current_data['message_text_id'] = 0
        current_data['message_admin_id'] = message_admin_id
    
    if type == 'big' or type == 'mid' or type == 'low':
        current_data['current_catalog'] = type
        current_data['current_number'] = 0

    if type == 'next' or type == 'back':
        if type == 'next':
            current_data['current_number'] = data[1] + 1
        if type == 'back':
            current_data['current_number'] = data[1] - 1

    if type == 'media':
        media = []
        for elem in message:
            media.append(str(elem.message_id))

        str_media = ','.join(media)
        current_data['message_meda_id'] = str_media

    if type == 'text':
        current_data['message_text_id'] = message.id

    cur.execute(f"INSERT OR REPLACE INTO current_state values(:user_id, :current_number, :current_catalog, :suncatcher_current_id, :message_photo_id, :message_meda_id, :message_text_id, :message_admin_id)", current_data).fetchall()

    con.commit()
    con.close()


def get_url_suncatcher(id):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT url_photo FROM suncatcher_photo WHERE suncatcher_photo_id={id}").fetchall()
    con.close()

    return res


def get_user(id):
    con = sqlite3.connect("suncatcher.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM user WHERE id={id}").fetchall()
    con.close()

    return res
    

# create_table_suncatcher()
# insert_table_suncatcher()

# create_table_suncatcher_photo()
# insert_table_suncatcher_photo()

# res = cur.execute("SELECT * FROM user")

# res = cur.execute("SELECT * FROM suncatcher where id=12460561")
# res2 = cur.execute("SELECT * FROM suncatcher_photo where suncatcher_id=12460561")

# create_table_all()
# insert_table_suncatcher()
# insert_table_suncatcher_photo()


def main():
    pass

if __name__ == '__main__':
    main()
