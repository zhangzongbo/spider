# -*- coding: utf-8 -*-
import sys
import requests
import hashlib

from http.cookiejar import LWPCookieJar
sys.path.append('../Util')

from storage import Storage
from encryptUtil import encrypted_request
from Downloader import Downloader

BASE_URL = 'http://music.163.com'
DEFAULT_TIMEOUT = 30


class NetEase(object):

    def __init__(self):
        self.header = {
            # 'Accept': '*/*',
            # 'Accept-Encoding': 'gzip,deflate,sdch',
            # 'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            # 'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Host': 'music.163.com',
            # 'Referer': 'http://music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        }

        self.storage = Storage()
        cookie_jar = LWPCookieJar(self.storage.cookie_path)
        cookie_jar.load()
        self.session = requests.Session()
        self.session.cookies = cookie_jar
        for cookie in cookie_jar:
            if cookie.is_expired():
                cookie_jar.clear()
                self.storage.database['user'] = {
                    'username': '',
                    'password': '',
                    'user_id': '',
                    'nickname': '',
                }
                self.storage.save()
                break

    @property
    def toplists(self):
        return [l[0] for l in TOP_LIST_ALL.values()]

    def logout(self):
        self.session.cookies.clear()
        self.storage.database['user'] = {
            'username': '',
            'password': '',
            'user_id': '',
            'nickname': '',
        }
        self.session.cookies.save()
        self.storage.save()

    def _raw_request(self, method, endpoint, data=None):
        if method == 'GET':
            resp = self.session.get(
                endpoint, params=data, headers=self.header, timeout=DEFAULT_TIMEOUT
            )
        elif method == 'POST':
            print("url: %s" % endpoint)
            print("data: %s" % data)
            resp = self.session.post(
                endpoint, data=data, headers=self.header, timeout=DEFAULT_TIMEOUT
            )
        return resp

    def request(self, method, path, params={}, default={'code': -1}):
        endpoint = '{}{}'.format(BASE_URL, path)
        csrf_token = ''
        for cookie in self.session.cookies:
            if cookie.name == '__csrf':
                csrf_token = cookie.value
                break
        params.update({'csrf_token': csrf_token})
        data = default

        params = encrypted_request(params)
        try:
            resp = self._raw_request(method, endpoint, params)
            print (resp.content)
            data = resp.json()
            # print(data)
        except requests.exceptions.RequestException as e:
            log.error(e)
        except ValueError as e:
            log.error('Path: {}, response: {}'.format(path, resp.text[:200]))
        finally:
            return data

    def login(self, username, password):
        self.session.cookies.load()

        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        password = md5.hexdigest()

        if username.isdigit():
            path = '/weapi/login/cellphone'
            params = dict(
                phone=username,
                password=password,
                rememberLogin='true',
            )
        else:
            # magic token for login
            # see https://github.com/Binaryify/NeteaseCloudMusicApi/blob/master/router/login.js#L15
            client_token = '1_jVUMqWEPke0/1/Vu56xCmJpo5vP1grjn_SOVVDzOc78w8OKLVZ2JH7IfkjSXqgfmh'
            path = '/weapi/login'
            params = dict(
                username=username,
                password=password,
                rememberLogin='true',
                clientToken=client_token
            )
        data = self.request('POST', path, params)
        # url = 'https://music.163.com/weapi/login/cellphone?csrf_token='
        # params = encrypted_request(params)
        # print(params)
        # header = self.header
        # data = Downloader.postData(url, header, params).content
        print(data)
        self.session.cookies.save()
        return data

    # 用户歌单
    def user_playlist(self, uid, offset=0, limit=50):
        path = '/weapi/user/playlist'
        params = dict(
            uid=uid,
            offset=offset,
            limit=limit,
            csrf_token=''
        )
        return self.request('POST', path, params).get('playlist', [])


if __name__ == "__main__":
    netease = NetEase()
    # data = netease.login(username='13253375519',
    #                      password='1994@zhang./')
    # print(data)
    play_list = netease.user_playlist(uid="434418620")
    print(play_list)
