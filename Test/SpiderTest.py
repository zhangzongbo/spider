# coding: utf-8
#
# from LogHandler import LogHandler
# from Downloader import Downloader
import sys
import requests
import json
# import music_mysql
import pymysql
sys.path.append('../Util')
from Downloader import Downloader
# log = LogHandler('test', file=False)

# header
headers = {
    'Referer': 'http://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/66.0.3359.181 Chrome/66.0.3359.181 Safari/537.36'
    # 'Cookie': 'appver=1.5.0.75771;MUSIC_U=e954e2600e0c1ecfadbd06b365a3950f2fbcf4e9ffcf7e2733a8dda4202263671b4513c5c9ddb66f1b44c7a29488a6fff4ade6dff45127b3e9fc49f25c8de500d8f960110ee0022abf122d59fa1ed6a2;',
}
# post的数据
user_data = {
    # 'uid': '107948356',
    # 'type': '0',
    'params': 'MRxenC21V6eNc+1omy+sr6LXrLmQHelJY5h8W7ncgOMd903gZPDReIfTQsEhqYgW3UIP35mFY1w5twWrO3kx86HBjlTTZ0l6BoPEzreQ7N22HeoACdO+TQdXhBIoqOdwG7jextFktSjIuJe06VWI9k0WRCbiNU94A6ExDpWIkwIy3lbTREB+pRzWqtFXEMCG',
    'encSecKey': 'b903de64d64abbc7a70f62c9b420f4b37501b24795125bc741eb60f0b05de3ecd2f22f9a278258eb1b62a3f4dedabbe12543c86b0124342f712dc0713c69c9f29b736c906b7c2051b4aeb107275542f20ed242177c9967bc3f770aa29c2f2b03db51ffb58da6fbb122cebc12dcac840b40e89ce79e4762344de568046b09a87e'
}
# 添加用户id、名字、以及喜欢的歌曲到user_love_songs数据库中


def get_user_music(uid, user_name):
    data = []
    url = 'http://music.163.com/weapi/v1/play/record?csrf_token='
    user_data['uid'] = uid
    user_data['type'] = '0'
    # response = requests.post(url, headers=headers, data=user_data)
    response = Downloader.postData(url, headers, user_data)
    response = response.content
    json_text = json.loads(response.decode("utf-8"))
    song_list = []
    try:
        json_all_data = json_text['allData']
        # print(json_all_data)
        for json_music in json_all_data:
            json_song = json_music['song']
            # print(json_song, end='\n')
            song_name = json_song['name']   # 歌曲名字
            song_id = json_song['id']  # 歌曲ID
            # 演唱者名字
            ar = json_song['ar']
            artist_name = ar[0]['name']
            artist_id = ar[0]['id']
            song = (song_name, song_id, artist_id)
            song_list.append(song)
            # print('song_name: %s, song_id: %s, artist_name: %s, artist_id: %s \n' % (
            #     json_song_name, json_song_id, artist_name, artist_id))
            print(song, end='\n')

    except KeyError as e:
        print (e)
        print('id为', end="")
        print(uid, end="")
        print('的用户听歌排行不可查看~')
    except Exception as e:
        print('出现错误啦~错误是:', e)
    print(len(song_list))


get_user_music(123, 'hhh')
