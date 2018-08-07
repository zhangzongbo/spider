# -*- coding: utf-8 -*-
# @Author: Catofes
# @Date:   2015-08-15
'''
Class to stores everything into a json file.
'''
from __future__ import (
    print_function, unicode_literals, division, absolute_import
)

import json

from future.builtins import open

from const import Constant
from singleton import Singleton
# from .utils import utf8_data_to_file


def utf8_data_to_file(f, data):
    if hasattr(data, 'decode'):
        f.write(data.decode('utf-8'))
    else:
        f.write(data)


class Storage(Singleton):

    def __init__(self):
        '''
        Database stores every info.
        '''
        if hasattr(self, '_init'):
            return
        self._init = True

        self.database = {
            'user': {
                'username': '',
                'password': '',
                'user_id': '',
                'nickname': '',
            },
            'collections': [],
            'songs': {},
            'player_info': {
                'player_list': [],
                'player_list_type': '',
                'player_list_title': '',
                'playing_order': [],
                'playing_mode': 0,
                'idx': 0,
                'ridx': 0,
                'playing_volume': 60,
            }
        }
        self.storage_path = Constant.storage_path
        self.cookie_path = Constant.cookie_path

    def login(self, username, password, userid, nickname):
        self.database['user'] = dict(
            username=username,
            password=password,
            user_id=userid,
            nickname=nickname
        )

    def logout(self):
        self.database['user'] = {
            'username': '',
            'password': '',
            'user_id': '',
            'nickname': '',
        }

    def load(self):
        try:
            with open(self.storage_path, 'r') as f:
                for k, v in json.load(f).items():
                    if isinstance(self.database[k], dict):
                        self.database[k].update(v)
                    else:
                        self.database[k] = v
        except (OSError, KeyError, ValueError) as e:
            pass
        self.save()

    def save(self):
        with open(self.storage_path, 'w') as f:
            data = json.dumps(self.database)
            utf8_data_to_file(f, data)
