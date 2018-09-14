import jieba
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

text = open('aboutLove.txt', encoding='utf-8').read()
# data = pd.read_csv(f, sep=',', header=None, encoding='utf-8',
#                    names=['nickname', 'likeCount', 'comment'])
# data = pd.read_csv(f, sep=',', header=None, encoding='utf-8',
#                    names=['date', 'nickname', 'city', 'rate', 'comment'])

# comment = jieba.cut(str(data['comment']), cut_all=True)
comment = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(comment).replace("NaN", "")
# wl_space_split = " ".join(comment)
# print('wl_space_split: %s' % wl_space_split)

# 导入背景图
backgroud_Image = plt.imread('/home/xyl/var/pic/bear.png')
stopwords = STOPWORDS.copy()
# print("STOPWORDS.copy()",help(STOPWORDS.copy()))
# coloring = np.array(Image.open("/home/xyl/var/pic/bear.png"))
coloring = np.array(Image.open("lan.jpg"))

wc = WordCloud(background_color='white', mask=coloring, font_path="/home/xyl/var/download/SimHei.ttf",
               stopwords=stopwords, max_font_size=100, max_words=300, random_state=60, scale=1.5)
wc.generate_from_text(wl_space_split)
plt.imshow(wc)
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')  # 不显示坐标轴
plt.show()
wc.to_file(r'aboutLove.jpg')
