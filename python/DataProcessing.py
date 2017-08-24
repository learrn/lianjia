# -*- coding: utf-8 -*-
"""
对数据源文件进行操作
"""
import csv
import sys
import time
import urllib2
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def gps_change(input, output):
    """
     通过百度地图API将获取到的百度地图坐标转为正确坐标
    :param input: 数据源文件
    :param output: 转换后的数据文件
    """
    flag = 1
    api = 'http://api.map.baidu.com/geoconv/v1/?coords={}&from=5&to=5&ak=r4lx3pCN4nw4YyUKpa9hHLtS2G3zXUAB'
    csvFile2 = open(output, 'w')
    writer = csv.writer(csvFile2, delimiter=',')

    with open(input) as csvfile:
        reader = [each for each in csv.DictReader(csvfile)]
    for row in reader:
        flag += 1
        print flag
        url = api.format('{},{}'.format(row[u'longitude'], row[u'latitude']))
        time.sleep(0.02)
        p = urllib2.urlopen(url)
        a = p.read()
        if eval(a)['status'] == 0:
            row[u'longitude'] = eval(a)['result'][0]['x']
            row[u'latitude'] = eval(a)['result'][0]['y']
        else:
            print 'error'
        writer.writerow([row[u'title'], row[u'community'], row[u'model'], row[u'area'], row[u'price'],
                         row[u'time'], row[u'link'], row[u'longitude'], row[u'latitude']])
    csvfile.close()
    csvFile2.close()


def average(input, output):
    """
    在数据源中添加一列用于记录平均租金价格(租金/面积)
    :param input: 数据源文件
    :param output: 修改后的数据文件
    """
    flag = 1
    csvFile2 = open(output, 'w')
    writer = csv.writer(csvFile2, delimiter=',')

    with open(input) as csvfile:
        reader = [each for each in csv.DictReader(csvfile)]
    for row in reader:
        flag += 1
        ave = int(row[u'price']) / int(re.sub("\D", "", row[u'area']))
        print flag, ave
        writer.writerow([row[u'title'], row[u'community'], row[u'model'], row[u'area'], row[u'price'], ave,
                         row[u'time'], row[u'link'], row[u'longitude'], row[u'latitude']])

    csvfile.close()
    csvFile2.close()


if __name__ == "__main__":
    gps_change('rent.csv', 'rent_gps.csv')
    average('rent_gps.csv', 'rent_ave.csv')
