import random
import time
import json

import requests
from requests.adapters import HTTPAdapter
from LogHandler import LogHandler

log = LogHandler('downloader', file=False)


def get_proxy():
    bak_url = 'http://123.207.35.36:5010/get/'
    url = 'http://127.0.0.1:5010/get'
    try:
        proxy = requests.get(url).text
    except Exception as e:
        print('本地获取代理失败，远程从获取')
        proxy = requests.get(bak_url).text
    return proxy


class Downloader(object):

    def __init__(self, *args, **kwargs):
        pass

    @property
    def user_agent(self):
        """
        return an User-Agent at random
        :return:
        """
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        return random.choice(ua_list)

    @property
    def header(self):
        """
        basic header
        :return:
        """
        return {'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

    def get(self, url, header=None, retry_time=5, timeout=30,
            retry_flag=list(), retry_interval=5, *args, **kwargs):
        """
        get method
        :param url: target url
        :param header: headers
        :param retry_time: retry time when network error
        :param timeout: network timeout
        :param retry_flag: if retry_flag in content. do retry
        :param retry_interval: retry interval(second)
        :param args:
        :param kwargs:
        :return:
        """
        headers = self.header
        if header and isinstance(header, dict):
            headers.update(header)
        while True:
            try:
                html = requests.get(url, headers=headers,
                                    timeout=timeout, **kwargs)
                if any(f in html.content for f in retry_flag):
                    raise Exception
                return html
            except Exception as e:
                print(e)
                retry_time -= 1
                if retry_time <= 0:
                    # 多次请求失败
                    resp = Response()
                    resp.status_code = 200
                    return resp
                time.sleep(retry_interval)

    def postData(url, headers, user_data):
        proxy = get_proxy()
        print("USER_DATA: %s" % user_data)
        # return requests.post(url, headers=headers, data=user_data, proxies={
        #     "http": "http://{}".format(proxy)})
        return requests.post(url, headers=headers, data=user_data)

    def getData(self, url, header=None, retry_time=10, timeout=3,
                retry_flag=list(), retry_interval=1, *args, **kwargs):
        headers = self.header
        if header and isinstance(header, dict):
            headers.update(header)
        while True:
            try:
                proxy = get_proxy()
                log.info('proxy: %s' % proxy)
                req = requests.get(url, headers=headers,
                                   timeout=timeout, proxies={
                                       "http": "http://{}".format(proxy)}, **kwargs)
                # print('content: %s' % (req.content[0:100]))
                data = json.loads(req.content)['comments']
                if any(f in data for f in retry_flag):
                    raise Exception
                return data
            except Exception as e:
                print(e)
                retry_time -= 1
                if retry_time <= 0:
                    # 多次请求失败
                    resp = Response()
                    resp.status_code = 200
                    return resp
                time.sleep(retry_interval)
