from jieba.analyse import extract_tags
import numpy as npy
import jieba
# extract_tags提取词频前20的关键词存为列表tags中

text = open('qingtian.txt', encoding='utf-8').read()
tags = extract_tags(sentence=text, topK=10)
# 全切词，分别统计出这20个关键词出现次数，即词频，存为字典words_freq中
words = [word for word in jieba.cut(text, cut_all=True)]
words_freq = {}
for tag in tags:
    freq = words.count(tag)
    words_freq[tag] = freq
# 将该字典按词频排序
usedata = sorted(words_freq.items(), key=lambda d: d[1])
# 字典转为numpy数组并作矩阵转置，方便画图取用
tmp = npy.array(usedata).T
print(tmp)
