# -*- coding: utf-8 -*-
import csv
import random
import re
import time

import bs4
import requests

from items import LianjiaItem
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

user_agent = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
]
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': user_agent[random.randint(0, 5)]
}

first_line = True


def get_latitude(url):  # 进入每个房源链接抓经纬度
    time.sleep(1)
    p = requests.get(url, headers=headers)
    html = p.text
    content = bs4.BeautifulSoup(html, "lxml")
    longitude = content.find('div', {'class': 'around js_content'})['longitude']
    latitude = content.find('div', {'class': 'around js_content'})['latitude']
    return [longitude, latitude]


def parse():
    url = 'http://sh.lianjia.com/zufang/'
    contents = requests.get(url, headers=headers)
    contents.encoding = 'utf-8'
    html = contents.text
    content = bs4.BeautifulSoup(html, "lxml")
    area_list = content.find('div', {'class': 'option-list gio_district'}).findAll('a')[1:-1]
    for area in area_list:
        # try:
        area_url = 'http://sh.lianjia.com/zufang/{}'.format(area['gahref'])
        detail_url(area_url)
        # yield scrapy.Request(url=area_url, headers=headers, callback=self.detail_url,
        #                      meta={"id1": area_han, "id2": area_pin})
        # except Exception:
        # pass


def detail_url(area_url):
    for i in range(1, 2):
        url = area_url + '/d{}'.format(str(i))
        print(url)
        # try:
        time.sleep(1)
        contents = requests.get(url, headers=headers)
        contents.encoding = 'utf-8'
        html = contents.text
        content = bs4.BeautifulSoup(html, "lxml")
        houselist = content.findAll('div', {'class': 'info-panel'})
        for house in houselist:
            #    try:
            item = LianjiaItem()
            item['title'] = house.find('h2').find('a')['title']
            item['community'] = house.find('a', {'class': 'laisuzhou'}).find('span')['title']
            a = house.find('div', {'class': 'where'}).text.split('\n')
            item['model'] = a[-3].replace('\t', '').replace(' ', '')
            item['area'] = a[-2].replace('\t', '').replace(' ', '')
            # item['focus_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[0]
            # item['watch_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[1]
            item['time'] = house.find('div', {'class': 'price-pre'}).text.replace('\n', '').replace('\t', '')
            item['price'] = house.find('div', {'class': 'price'}).find('span', {'class': 'num'}).text
            # item['average_price'] = house.xpath('div[1]/div[6]/div[2]/span/text()').pop()
            url_detail = 'http://sh.lianjia.com' + house.find('h2').find('a')['href']
            item['link'] = house.find('h2').find('a')['href']
            item['Latitude'] = get_latitude(url_detail)
            # if first_line:
            #     first_line = False
            #     csv_writer.writerow(item.keys())
            b = item.values()
            csv_writer.writerow([item['title'], item['community'], item['model'], item['area'], item['price'],
                                item['time'], item['link'], item['Latitude']])
            # except Exception:
            #    print(Exception.message)
            # except Exception:
            #    print(Exception.message)


csv_file = open("rent.csv", "wb")
csv_writer = csv.writer(csv_file, delimiter=',')
parse()
csv_file.close()
