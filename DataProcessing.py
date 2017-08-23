# -*- coding: utf-8 -*-
import csv
import sys
import time
import urllib2
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def gpsChange(input, output):
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

# a = p.text.split('"status":0,"result":')[-1].replace('[', '').replace(']}', '')
# print a
