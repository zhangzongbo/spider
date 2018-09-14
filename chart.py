from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import jieba
import matplotlib.pyplot as plt
#import seaborn as sns
from pyecharts import Geo, Style, Line, Bar, Overlap

f = open('爱情公寓_new.txt', encoding='utf-8')
data = pd.read_csv(f, sep=',', header=None, encoding='utf-8',
                   names=['date', 'nickname', 'city', 'rate', 'comment'])

city = data.groupby(['city'])
rate_group = city['rate']
city_com = city['rate'].agg(['mean', 'count'])
# print(city_com)
city_com.reset_index(inplace=True)
city_com['mean'] = round(city_com['mean'], 2)

# 热力图分析
data_map = [(city_com['city'][i], city_com['count'][i])
            for i in range(0, city_com.shape[0])]
# print(data_map)
style = Style(title_color="#fff", title_pos="center",
              width=1800, height=800, background_color="#404a59")

geo = Geo("《爱情公墓》粉丝人群地理位置", "数据来源：Python", **style.init_style)
geo.add_coordinate("东海", 118.75, 34.54)  # 数据仅供示例
geo.add_coordinate("临澧", 111.64, 29.44)
geo.add_coordinate("临颍", 113.93, 33.82)
geo.add_coordinate("丽江", 100.25, 26.86)
geo.add_coordinate("乌兰察布", 113.11, 41.03)
geo.add_coordinate("云阳", 108.67, 30.95)
geo.add_coordinate("京山", 113.10, 31.02)
geo.add_coordinate("什邡", 104.17, 31.13)
geo.add_coordinate("仙居", 120.73, 28.87)
geo.add_coordinate("兰陵", 117.85, 34.74)
geo.add_coordinate("共青城", 115.58, 29.19)
geo.add_coordinate("北碚", 106.40, 29.80)
geo.add_coordinate("南沙", 113.60, 22.77)
geo.add_coordinate("同安", 118.15, 24.73)
geo.add_coordinate("启东", 121.65, 31.82)
geo.add_coordinate("大足区", 105.72, 29.70)
geo.add_coordinate("大邑", 103.53, 30.58)
geo.add_coordinate("宁乡", 112.55, 28.25)
geo.add_coordinate("安吉", 119.68, 30.68)
geo.add_coordinate("安溪", 118.18, 25.07)
geo.add_coordinate("射洪", 105.31, 30.9)
geo.add_coordinate("崇左", 107.37, 22.42)
geo.add_coordinate("平遥", 112.18, 37.2)
geo.add_coordinate("惠东", 114.7, 22.97)
geo.add_coordinate("文昌", 110.72, 19.61)
geo.add_coordinate("桐城", 116.94, 31.04)
geo.add_coordinate("汶上", 116.49, 35.71)
geo.add_coordinate("沂南", 118.47, 35.54)
geo.add_coordinate("沭阳", 118.79, 34.12)
geo.add_coordinate("泗洪",  118.23, 33.46)
geo.add_coordinate("海安", 120.45, 32.57)
geo.add_coordinate("渑池", 111.75, 34.76)
geo.add_coordinate("湘西", 109.44, 28.18)
geo.add_coordinate("璧山", 106.20, 29.57)
geo.add_coordinate("甘南", 102.92, 34.99)
geo.add_coordinate("丽江", 100.25, 26.86)
geo.add_coordinate("盱眙", 118.54, 32.97)
geo.add_coordinate("睢宁", 117.89, 33.94)
geo.add_coordinate("綦江", 106.68, 28.88)
geo.add_coordinate("绵竹", 104.13, 31.44)
geo.add_coordinate("蒙自市", 103.50, 23.35)
geo.add_coordinate("西华", 114.48, 33.8)
geo.add_coordinate("赣榆", 119.04, 34.88)
geo.add_coordinate("辉南", 126.34, 42.55)
geo.add_coordinate("达州", 107.49, 31.21)
geo.add_coordinate("迁安", 118.68, 40.04)
geo.add_coordinate("金沙", 106.27, 27.44)
geo.add_coordinate("隆回", 110.97, 27.35)
geo.add_coordinate("黔南", 107.52, 26.26)
# geo.add_coordinate("丽江", 100.25, 26.86)
while True:
    try:
        attr, val = geo.cast(data_map)
        geo.add("", attr, val, visual_range=[0, 20],
                visual_text_color="#fff", symbol_size=20,
                is_visualmap=True, is_piecewise=True,
                visual_split_number=4)

    except ValueError as e:
        e = str(e)
        e = e.split("No coordinate is specified for ")[1]  # 获取不支持的城市名
        for i in range(0, len(data_map)):
            if e in data_map[i]:
                data_map.pop[i]
                break

    else:
        break
geo.render('爱情公墓.html')

# 折线+柱图分析
city_main = city_com.sort_values('count', ascending=False)[0:20]
# print(city_main)
attr = city_main['city']
v1 = city_main['count']
v2 = city_main['mean']
# print(attr,v1,v2)
line = Line("主要城市评分")
line.add("城市", attr, v2, is_stack=True, xaxis_rotate=30, yaxix_min=4.2,
         mark_point=['min', 'max'], xaxis_interval=0, line_color='lightblue',
         line_width=4, mark_point_textcolor='black', mark_point_color='lightblue',
         is_splitline_show=False)

bar = Bar("主要城市评论数")
bar.add("城市", attr, v1, is_stack=True, xaxis_rotate=30, yaxix_min=4.2,
        xaxis_interval=0, is_splitline_show=False)

overlap = Overlap()
overlap.add(bar)
overlap.add(line, yaxis_index=1, is_add_yaxis=True)
overlap.render('主要城市评论数_平均分.html')


# 词云分析
# 分词
comment = jieba.cut(str(data['comment']), cut_all=False)
wl_space_split = " ".join(comment).replace("NaN", "")

# print('wl_space_split: %s' % wl_space_split)

# 导入背景图
backgroud_Image = plt.imread('lan.jpg')
stopwords = STOPWORDS.copy()
# print("STOPWORDS.copy()",help(STOPWORDS.copy()))


wc = WordCloud(width=1024, height=768, background_color='white',
               mask=backgroud_Image, font_path="/home/xyl/var/download/SimHei.ttf",
               stopwords=stopwords, max_font_size=400,
               random_state=50)

wc.generate_from_text(wl_space_split)
plt.imshow(wc)
plt.axis('off')  # 不显示坐标轴
plt.show()
wc.to_file(r'laji.jpg')
