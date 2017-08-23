# -*- coding: utf-8 -*-
import csv
import re
import sys
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl

reload(sys)
sys.setdefaultencoding('utf-8')


def dataToDict(mKey, mValue, needSorted=False):
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


def aveAndArea(start, end):
    mdict, keys, price = dataToDict(mKey=u'area', mValue=u'ave', needSorted=True)
    # for key,value in mdict.items():
    areas = [re.sub("\D", "", key) for key in keys]
    plt.plot(areas, price, 'b*')
    plt.plot(areas, price, 'r')
    plt.xlim(start, end)
    plt.xlabel('areas')
    plt.ylabel('housing average price/area')
    plt.title('areas & ave')
    plt.legend()
    plt.savefig("aveAndArea.png")
    plt.show()


def aveAndCommunity(start, end=None, length=10):
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    price = []
    community = []
    mdict, _, _ = dataToDict(mKey=u'community', mValue=u'ave')
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
    plt.grid(True)
    plt.savefig("aveAndCommunity.png")
    plt.show()
    # plt.hist(sortDict[:10])


# aveAndArea(0, 150)
aveAndCommunity(0,10,length=10)
