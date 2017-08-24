# -*- coding: utf-8 -*-
"""
对数据进行可视化操作
"""
import csv
import re
import sys
import jieba
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
from wordcloud import WordCloud, STOPWORDS
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8')


def data_to_dict(mKey, mValue, needSorted=False):
    """
     将特定数据转换字典
    :param mKey:需要统计的属性，数据中可能有多条记录拥有相同的mKey
    :param mValue:拥有相同mKey的属性的平均值
    :param needSorted:是否需要根据mKey值进行排序
    :return:处理后的字典，键列表，值列表
    """
    temp = {}
    keys = []
    values = []
    with open('rent_ave.csv') as csvfile:
        reader = [each for each in csv.DictReader(csvfile)]
    for row in reader:
        tempKey = row[mKey]
        temp[tempKey] = '{},{}'.format(temp.get(tempKey, 'null'), row[mValue])
    if needSorted:
        a = sorted(temp.iteritems(), key=lambda d: int(re.sub("\D", "", d[0])))
    else:
        a = temp.iteritems()
    print a
    for key, value in a:
        narray = np.array(value.replace('null,', '').split(','), dtype=np.int)
        temp[key] = narray.mean()
        keys.append(key)
        values.append(temp[key])
    return temp, keys, values


def ave_and_area(start, end):
    """
    生成面积性价比的折线图，即面积与平均租金的关系
    :param start:面积下限
    :param end:面积上限
    :return:X轴为面积（从下限到上限）Y轴为平均租金的折线图
    """
    mdict, keys, price = data_to_dict(mKey=u'area', mValue=u'ave', needSorted=True)
    areas = [re.sub("\D", "", key) for key in keys]
    plt.plot(areas, price, 'b*')
    plt.plot(areas, price, 'r')
    plt.xlim(start, end)
    plt.xlabel(u'面积/平')
    plt.ylabel(u'每平米月平均租金/元')
    plt.title(u'面积性价比')
    plt.legend()
    plt.savefig("aveAndArea.png")
    plt.show()


def ave_and_community(start, end=None, length=10):
    """
    生成小区性价比的柱状图，即小区与平均租金的关系
    :param start:取值下限，如:性价比最高的小区start=0
    :param end:取值上限，如:性价比最高的小区end=10
    :param length:取值数目
    :return:小区性价比的柱状图
    """
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    price = []
    community = []
    mdict, _, _ = data_to_dict(mKey=u'community', mValue=u'ave')
    sortDict = sorted(mdict.iteritems(), key=lambda d: float(d[1]))
    for a, b in sortDict[start:end]:
        community.append(unicode(a))
        price.append(b)
    width = 0.4
    ind = np.linspace((length - 1) + 0.5, 0.5, length)
    ax = plt.figure(1).add_subplot(111)
    ax.barh(ind - width / 2, price, width, color='blue')
    ax.set_yticks(ind)
    ax.set_yticklabels(community)
    plt.xlabel(u"每平米月平均租金/元")
    plt.title(u"小区性价比")
    plt.grid(True)
    plt.savefig("aveAndCommunity.png")
    plt.show()


def jieba_clear_text(text):
    """
    对文本进行分词
    :param text: 文本
    :return: 分词后的结果
    """
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)
    for myword in liststr.split('/'):
        if len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ''.join(mywordlist)


def title_word_cloud():
    """
    生成标题的词云
    """
    text = ''
    wc = WordCloud(background_color='white',  # 设置背景颜色
                   stopwords=STOPWORDS,
                   max_words=1000,  # 设置最大现实的字数
                   font_path='C:/Python27/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf',
                   # 设置字体格式，如不设置显示不了中文
                   max_font_size=50,  # 设置字体最大值
                   random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                   )
    with open('rent_ave.csv') as csvfile:
        reader = [each for each in csv.DictReader(csvfile)]
    for row in reader:
        text += row[u'title'] + ' '
    print jieba_clear_text(text)
    wc.generate(jieba_clear_text(text))
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


def model_frequency():
    """
    生成户型的饼状图
    """
    temp_list = []
    with open('rent_ave.csv') as csvfile:
        reader = [each for each in csv.DictReader(csvfile)]
    for row in reader:
        text = row[u'model']
        temp_list.append(text)
    d = Counter(temp_list).most_common(6)
    a = [unicode(i[0] + '\n({})'.format(i[1]), "utf-8") for i in d]
    b = [i[1] for i in d]
    a.append(u'其他\n({})'.format(len(reader) - sum(b)))
    b.append(len(reader) - sum(b))
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'red', 'gray', 'green']
    explode = (0.1, 0, 0, 0, 0, 0, 0)

    plt.pie(b, labels=a, colors=colors, explode=explode,
            autopct='%1.1f%%', shadow=True)
    plt.axis('equal')
    plt.savefig('modelFrequency.png')
    plt.show()


if __name__ == "__main__":
    ave_and_area(0, 150)
    ave_and_community(0, 10, length=10)
    title_word_cloud()
    model_frequency()
