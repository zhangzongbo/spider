# -*- coding: utf-8 -*-

import os
import json
import base64
import time
import pymysql
import sys
import threading

import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from prettytable import PrettyTable
sys.path.append('Util')
from Util.Downloader import Downloader
from Util.LogHandler import LogHandler

BASE_URL = 'http://music.163.com/'
_session = requests.Session()

COMMENT_THRESHOLD = 10000

PAGE_LIMIT = 20

log = LogHandler('myspider', file=False)

size = 100
local_List = []


def create_thread(myList):
    threads = []

    for song in myList:
        thread = threading.Thread(
            target=get_comments_by_api, args=(song[1], song[0], song[2]))
        threads.append(thread)

    print("len: %s" % len(threads))
    for thread in threads:
        thread.start()

    for thread in threads:
        # wait for all
        # join()会等到线程结束，或者在给了 timeout 参数的时候，等到超时为止。
        # 使用 join()看上去 会比使用一个等待锁释放的无限循环清楚一些(这种锁也被称为"spinlock")
        thread.join()


def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
    # db = pymysql.connect("localhost", "root", "123456.", "TESTDB")
    db = pymysql.connect(host='localhost', port=3306,
                         user='root', passwd='123456', db='NCMComment')
    print('连接上了!')
    return db


def insertdb(db, sql):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # INSERT INTO NCMComment.comment(user_id, user_name, like_count, content, `time`) VALUES(1314638279, '聂晓琦dw', 1, '不喜欢电影不喜欢歌曲 故事太过悲情 离我太接近', '2017-03-02 15:22:22');
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        print ('插入数据失败! sql : %s' % sql)
        db.rollback()


def get_proxy():
    bak_url = 'http://123.207.35.36:5010/get/'
    url = 'http://127.0.0.1:5010/get'
    try:
        proxy = requests.get(url).text
    except Exception as e:
        print('本地获取代理失败，远程从获取')
        proxy = requests.get(bak_url).text
    return proxy


def get_song_list(artist_id, limit=50):
    """
    输入歌手id，返回该歌手的前50首热门歌曲。
    """
    url = 'http://music.163.com/artist?id={}'.format(artist_id)
    print(url)
    headers = {'user-agent': 'my-app/0.0.1'}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    ul = soup.select('ul.f-hide')[0]
    li = ul.select('li')
    # song_list 是一个列表，每个元素的第一项是歌曲名，第二项是歌曲id
    song_list = [(song.get_text(), song.select('a')[0]['href']) for song in li]

    return song_list[:limit]


def get_user_music():
    # header
    headers = {
        'Referer': 'http://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/66.0.3359.181 Chrome/66.0.3359.181 Safari/537.36'
    }
    # post的数据
    user_data = {
        'params': 'maXFUazSOArMKBBzgJl2it+Wqw6+wcl/8OVb3RdZMHyZFO8+xtDlJaArH2W21t9QbGeatUWr/8r95wNNOZVX/EUgxWYu22d4k/cvsYHwtDADhKKJ1+aF4EXsLm4b5xQsdMQrV4MpJQE8+s8dHEUYZAZngxcL0XeY6wqfMz7iv1TR+9uN4R7pnGLi7gsvFyHDvhcPora18zHOyPRmjMm71Hc78Zq82dd8XbdSwMwbAJQ=',
        'encSecKey': 'c50ec0da5f7f558e469c090bcc6a68457ec39e5ba787f363509405841ce7c95c84a62ca88839c790bdc28220770e5fd2478d61734070ab3068ee41aaede1dfe79dc989c282d6da8cd63d71e9b674d8b4c86bb1cd081c4284c7d5be1aed3878574c59789a46bdf4e5f6318c87105d7104c2098e6966cce7b2e6fec3ed7c25feef'
    }

    data = []
    url = 'http://music.163.com/weapi/v1/play/record?csrf_token='
    response = Downloader.postData(url, headers, user_data)
    response = response.content
    json_text = json.loads(response.decode("utf-8"))
    song_list = []
    try:
        json_all_data = json_text['allData']
        for json_music in json_all_data:
            json_song = json_music['song']
            song_name = json_song['name']   # 歌曲名字
            song_id = json_song['id']  # 歌曲ID
            # 演唱者名字
            ar = json_song['ar']
            artist_name = ar[0]['name']
            artist_id = ar[0]['id']
            song = (song_name, song_id, artist_id)
            song_list.append(song)

            print(song, end='\n')

    except KeyError as e:
        print (e)
        print('用户听歌排行不可查')
    except Exception as e:
        print('出现错误啦~错误是:', e)
    print(len(song_list))
    return song_list


def get_comments_by_api(song_id, song_name, artist_id, threshold=COMMENT_THRESHOLD):
    """
    这个接口不需要加密
    """
    db = connectdb()    # 连接MySQL数据库

    base_url = BASE_URL + \
        'api/v1/resource/comments/R_SO_4_{}'.format(song_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/66.0.3359.181 Chrome/66.0.3359.181 Safari/537.36'}
    base_req = requests.get(base_url, headers=headers)
    base_data = json.loads(base_req.content)
    total = base_data['total']
    offsetList = list(range(total))[0::20]
    url_list = []
    for offset in offsetList:
        url = BASE_URL + 'api/v1/resource/comments/R_SO_4_{}'.format(
            song_id) + '?limit=%s&offset=%s' % (PAGE_LIMIT, offset)
        url_list.append(url)
    url_list = url_list[0:501] + url_list[-501:]
    local_List = url_list
    log.info(len(url_list))
    for url in url_list:
        log.info("url: %s" % (url))
        try:
            down = Downloader()
            data = down.getData(url=url)
        except Exception as e:
            log.info(str(e))
            log.info("数据获取异常url: %s" % (url))
        else:
            for item in data:
                publishTime = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(int(item['time']) / 1000))
                content = item['content']
                content = content.replace("'", "''")
                sql = "REPLACE INTO NCMComment.comment(comment_id,user_id, user_name, like_count, content, song_id, song_name, artist_id, `time`) VALUES(%s,%s, '%s', %s, '%s',%s ,'%s' ,%s, '%s');" % (
                    item['commentId'], item['user']['userId'], item['user']['nickname'], item['likedCount'], content, song_id, song_name, artist_id, publishTime)
                insertdb(db, sql)


if __name__ == "__main__":
    # get_comments_by_api(song_id=553310243)
    # artist_id = 13193
    # song_list = get_song_list(artist_id)  # 传入歌手id
    song_list = get_user_music()
    song_list = song_list[80:100]
    log.info(song_list)
    create_thread(song_list)
