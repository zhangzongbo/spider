import pymysql
import json


def connectdb():
    print('连接到mysql服务器...')
    db = pymysql.connect(host='localhost', port=3306,
                         user='root', passwd='123456', db='NCMComment')
    print('连接上了!')
    return db


def readfromdb(db, sql):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # INSERT INTO NCMComment.comment(user_id, user_name, like_count, content, `time`) VALUES(1314638279, '聂晓琦dw', 1, '不喜欢电影不喜欢歌曲 故事太过悲情 离我太接近', '2017-03-02 15:22:22');
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        for r in cursor:
            # print(r.replace(")", ""))
            # print(type(r))
            s = ('%s' % (r[0]))
            # print(s)
            with open('aboutLove.txt', 'a', encoding='utf-8') as f:
                f.write(s + '\n')
            # break
    except:
        # Rollback in case there is any error
        print ('读取数据失败! sql : %s' % sql)
        db.rollback()
# 保存到文本文档中


def save_to_txt():
    db = connectdb()
    sql = "SELECT content from NCMComment.comment WHERE song_id = '326705';"
    readfromdb(db, sql)


    # for i in range(1, 1001):
    #
    #     print("开始保存第%d页" % i)
    #     url = 'http://m.maoyan.com/mmdb/comments/movie/1175253.json?_v_=yes&offset=' + \
    #         str(i)
    #     print('url: %s' % url)
    #
    #     # html = get_one_page(url)
    #     for item in get_one_page(url):
    #         with open('爱情公寓.txt', 'a', encoding='utf-8') as f:
    #             f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ','
    #                     + str(item['rate']) + ',' + item['conment'] + '\n')
if __name__ == "__main__":
    save_to_txt()
