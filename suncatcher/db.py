import sqlite3
from .vksunbot import *
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


def create_table_user():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `user`')
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


def insert_table_user(data):
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    user = {}
    user['id'] = data.from_user.id
    user['name'] = data.from_user.first_name if data.from_user.first_name else 'none'
    user['surname'] = data.from_user.last_name if data.from_user.last_name else 'none'
    user['nickname'] = data.from_user.username if data.from_user.username else 'none'
    user['adress'] = 'none'

    cur.execute("INSERT OR IGNORE INTO user VALUES(:id, :name, :surname, :nickname, :adress)", user)

    con.commit()
    con.close()


def create_table_press_start():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `press_start`')
    cur.execute("""
        CREATE TABLE `press_start` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )""")
    con.commit()
    con.close()


def insert_table_press_start():

    now = datetime.datetime.now()


def create_table_current_state():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `current_state`')
    cur.execute("""
        CREATE TABLE `current_state` (
            user_id INTEGER PRIMARY KEY NOT NULL,
            suncatcher_current_id INTEGER IS NULL
            message_photo_id INTEGER IS NULL,
            message_meda_id TEXT IS NULL,
            message_text_id INTEGER IS NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
            FOREIGN KEY (suncatcher_id) REFERENCES suncatcher(id)
        )""")
    con.commit()
    con.close()

 
def create_table_user_path():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `user_path`')
    cur.execute("""
        CREATE TABLE `user_path` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            catalog TEXT NOT NULL,
            new_field INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )""")
    con.commit()
    con.close()


def create_table_suncatcher():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `suncatcher`')
    cur.execute("""
        CREATE TABLE `suncatcher` (
            id INTEGER PRIMARY KEY NOT NULL,
            suncatcher_id INEGER NOT NULL,
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

    catalog_vk = get_catalog_vk()
    category = ['big', 'mid', 'low']

    for cat in category:
        for elem in catalog_vk[cat]:
            elem['catalog'] = cat
            elem['available'] = 'true'
            cur.execute("INSERT OR IGNORE INTO suncatcher VALUES(:id, :title, :description, :price, :catalog, :available)", elem)
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

    print(amount)

    return amount


def sell_suncatcher():
    pass



def create_table_suncatcher_photo():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `suncatcher_photo`')
    cur.execute("""
        CREATE TABLE `suncatcher_photo` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suncatcher_id INTEGER,
            url_photo TEXT NOT NULL,
            FOREIGN KEY (suncatcher_id) REFERENCES suncatcher(id)
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
                cur.execute("INSERT INTO suncatcher_photo(suncatcher_id, url_photo) VALUES(:id, :url_photo)", sun_photo)
    con.commit()
    con.close()


def create_table_order():
    con = sqlite3.connect("suncatcher.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS `order`')
    cur.execute("""
        CREATE TABLE `order` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_user INTEGER NOT NULL,
            date TEXT NOT NULL,
            suncatcher_id INTEGER NOT NULL,
            payment_status TEXT NOT NULL,
            track_number TEXT NOT NULL,
            delivered_status TEXT NOT NULL,
            step_order INTEGER NOT NULL,
            FOREIGN KEY (order_user) REFERENCES user(id),
            FOREIGN KEY (suncatcher_id) REFERENCES suncatcher(id)
        )""")
    con.commit()
    con.close()


def get_url_suncatcher(number=0):
    pass


# create_table_suncatcher()
# insert_table_suncatcher()

# create_table_suncatcher_photo()
# insert_table_suncatcher_photo()

# res = cur.execute("SELECT * FROM user")
# print(res.fetchall())

# res = cur.execute("SELECT * FROM suncatcher where id=12460561")
# print(res.fetchall())
# res2 = cur.execute("SELECT * FROM suncatcher_photo where suncatcher_id=12460561")
# print(res2.fetchall())

if __name__ == '__main__':
    create_table_all()