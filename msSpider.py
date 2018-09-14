import requests
import time
import re
from bs4 import BeautifulSoup


def getHtml():
    BASE_URL = 'http://ms31.haixing8.cn/login.php?d=map.getonepage&u=21367898&s=19401688&v=3059&x=1&y=null&cp={}&main=1'
    mapList = list(range(15000, 19999))
    calcList = []
    for i in mapList:
        url = BASE_URL.format(i)
        # print('url: %s' % url)
        y = 0
        total = 0

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        tag_p = soup.select('p')[0]
        tag_a = tag_p.select('a')
        for ta in tag_a:
            # print(ta.text)
            if '高产县粮' in ta.text:
                y = y + 1
        s = 'page {},has {} city'.format(i + 1, y)

        calcList.append(y)
        if len(calcList) == 5:
            for x in calcList:
                total = total + x
            mark = s + ' page {} total has {} city'.format(i - 1, total)
            print(mark)
            if total > 4:
                # mark = '####>> page {} total has {} city'.format(i - 2, total)

                print(mark)
                with open('msjs-15000-19999.txt', 'a', encoding='utf-8') as f:
                    f.write(mark + '\n')
            del calcList[0]
        # print(s)

        time.sleep(1)


def getList():
    BASE_URl = 'http://ms31.haixing8.cn/login.php?d=map.getonepage&u=21367898&s=31657899&v=3059&x=1&y=null&cp={}&main=1'
    mapList = list(range(20000, 24000))
    for i in mapList:
        time.sleep(0.2)
        print("page:{}".format(i))
        url = BASE_URl.format(i)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        tag_p = soup.select('p')[0]
        tag_a = tag_p.select('a')[5: -5]
        for a in tag_a:
            sub_url = a['href']
            r = re.compile(r'\&type=(\d$)')
            searchUrl = r.search(sub_url)
            # and a.text != '村庄'
            if searchUrl and a.text != '村庄':
                map_type = searchUrl.group(1)
                city_type = num_to_string(int(map_type))
                city = a.text.strip('\n')
                html = requests.get(sub_url)
                sub_soup = BeautifulSoup(html.text, 'html.parser')
                line = sub_soup.text
                name = 'NO_NAME'
                scale = 0
                searchName = re.search(
                    r'君主名:(.*?) ', line, re.M | re.I)
                if searchName:
                    name = searchName.group(1)
                else:
                    print("No match!!")

                searchCity = re.search(
                    r'规模:(\d{1,4}).*', line, re.M | re.I)
                if searchCity:
                    # print("City group 1 :{}".format(searchCity.group(1)))
                    scale = int(searchCity.group(1))
                    if(scale > 80):
                        mark = "page:{}, scale:{},type:{}, city:{}|{}".format(
                            i + 1, scale, city_type, city, name)
                        print(mark)
                        with open('msjs-user-19000-24000.txt', 'a', encoding='utf-8') as f:
                            f.write(mark + '\n')
                else:
                    print("No match!!")


def num_to_string(num):
    '''这是多行注释
    1 == 4,4,4,6
    2 == 3,4,5,6
    3 == 5,3,4,6
    4 == 4,5,3,6
    5 == 3,3,3,9
    6 == 1,1,1,15
    7 == 0,0,0,18
    '''
    numbers = {
        1: "4,4,4,6",
        2: "3,4,5,6",
        3: "5,3,4,6",
        4: "4,5,3,6",
        5: "3,3,3,9",
        6: "1,1,1,15",
        7: "0,0,0,18",
    }

    return numbers.get(num, None)
# def getOneHtml(urlList):
#


if __name__ == "__main__":
    # getHtml()
    getList()
