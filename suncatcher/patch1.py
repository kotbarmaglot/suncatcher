# создание новой структуры user_file, если старые существовали
import os
import json
from .user import init_user_file
from pathlib import Path
import pathlib
import sys


def patch1():
    user = init_user_file()

    for root, dirs, files in os.walk('./suncatcher/user_file'):
        print(root)
        print(dirs)
        print(files)
        for filename in files:
            print(filename)
            with open('./suncatcher/user_file/'+filename, "r") as read_file:
                user_data = json.load(read_file)

            user['current_path']['size_sun'] = user_data['current_size']

            if user_data['current_size']:
                user['current_path']["number_sun"] = user_data['catalog'][user_data['current_size']]['current']
            else: 
                user['current_path']["number_sun"] = 0
            user['current_path']["message_id_meda_group"] = user_data['id_media']
            user['current_path']["message_id_meda"] = user_data['id_mes']
        
            with open('./suncatcher/user_file/'+filename, "w") as write_file:
                json.dump(user, write_file)

    # print('llllll')
    # print('patch1.py:', sys.path)


if __name__ == '__main__':
    patch1()