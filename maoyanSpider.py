import requests
import time
import random
import json
import sys
sys.path.append('Util')
from Util.Downloader import Downloader

# 获取每一页数据


def get_one_page(url):

    down = Downloader()
    data = down.get(url=url)
    for item in data:
        yield{
            'date': item['time'].split(' ')[0],
            'nickname': item['nickName'],
            'city': item['cityName'],
            'rate': item['score'],
            'conment': item['content']
        }

# 解析每一页数据


def parse_one_page(html):

    data = json.loads(html)['cmts']  # 获取评论内容
    for item in data:
        yield{
            'date': item['time'].split(' ')[0],
            'nickname': item['nickName'],
            'city': item['cityName'],
            'rate': item['score'],
            'conment': item['content']
        }

# 保存到文本文档中


def save_to_txt():
    for i in range(1, 1001):

        print("开始保存第%d页" % i)
        url = 'http://m.maoyan.com/mmdb/comments/movie/1175253.json?_v_=yes&offset=' + \
            str(i)
        print('url: %s' % url)

        # html = get_one_page(url)
        for item in get_one_page(url):
            with open('爱情公寓.txt', 'a', encoding='utf-8') as f:
                f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ','
                        + str(item['rate']) + ',' + item['conment'] + '\n')
                # time.sleep(random.randint(1,100)/20)
                # time.sleep(2)

# 去重重复的评论内容


def delete_repeat(old, new):
    oldfile = open(old, 'r', encoding='utf-8')
    newfile = open(new, 'w', encoding='utf-8')
    content_list = oldfile.readlines()  # 获取所有评论数据集
    content_alread = []  # 存储去重后的评论数据集

    for line in content_list:
        if line not in content_alread:
            newfile.write(line + '\n')
            content_alread.append(line)


if __name__ == '__main__':
    # save_to_txt()
    delete_repeat(r'爱情公寓_old.txt', r'爱情公寓_new.txt')
