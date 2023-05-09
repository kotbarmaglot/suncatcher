from pathlib import Path
import os
import json
import datetime


def init_user_file():
    user = {}
    id = {}
    current_path = {}
    status_order_item = {}
    user_path_item = {}
    user_path = []
    status_order = []
    user_path_item_catalog_item = {}

    id['user_id'] = 0
    id['user_name'] = ''
    id['user_surname'] = ''
    id['user_nickname'] = ''
    id['user_start'] = []

    current_path['size_sun'] = ''
    current_path['number_sun'] = 0
    current_path['message_id_media_group'] = []
    current_path['message_id_media'] = 0
    current_path['message_id_text'] = 0

    user_path_item_catalog_item['time'] = ''
    user_path_item_catalog_item['size_sun'] = ''
    user_path_item_catalog_item['id_sun'] = 0
    user_path_item['data'] = ''
    user_path_item['catalog'] = [user_path_item_catalog_item]
    user_path = [user_path_item]
    
    status_order_item['data'] = ''
    status_order_item['suncatcher_id'] = []
    status_order_item['adress'] = ''
    status_order_item['status_pay'] = ''
    status_order_item['track_number'] = ''
    status_order_item['delivered'] = ''
    status_order_item['step_order'] = ''
    status_order = [status_order_item]

    user['id'] = id
    user['current_path'] = current_path
    user['user_path'] = [user_path]
    user['status_order'] = [status_order]

    return user

def create_user_file(message):
    print(message)
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    user_nickname = message.from_user.username
    user_start = str(datetime.datetime.now())[0:10]
    user_patch = Path(f"suncatcher/user_file/{user_id}.json")

    user = init_user_file()

    if os.path.exists(user_patch):
        with open(user_patch, "r") as read_file:
            user_data = json.load(read_file)

        user['current_path']['size_sun'] = user_data['current_path']['size_sun']
        user['current_path']["number_sun"] = user_data_old['catalog'][user_data_old['current_size']]['current']
        user['current_path']["message_id_meda_group"] = user_data_old['id_media']
        user['current_path']["message_id_meda"] = user_data_old['id_mes']
    
    with open(user_patch, "w") as write_file:
        json.dump(user, write_file)

    
def get_user_file(message):
    user_id = message.from_user.id
    user_patch = Path(f"suncatcher/user_file/id_{user_id}.json")

    with open(user_patch, "r") as read_file:
        user_data = json.load(read_file)

    return user_data


def update_user_file(message, data):
    user_id = message.from_user.id
    user_patch = Path(f"suncatcher/user_file/id_{user_id}.json")

    with open(user_patch, "w") as write_file:
        json.dump(data, write_file)
