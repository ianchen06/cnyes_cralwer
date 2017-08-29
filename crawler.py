"""
   list_crawler.py
   ~~~~~~~~~~~~~~~
   This crawler gets the news list of cnyes.com

   author: Ian Chen <ianchen06@gmail.com>
"""
# coding: utf-8
import logging

import dateutil.parser as dp
import requests
from bs4 import BeautifulSoup
import peewee

db = peewee.MySQLDatabase('news',
        host='localhost',
        user='admin',
        password=''
        )

class Cnyes(peewee.Model):
    url     = peewee.CharField(primary_key=True)
    title   = peewee.CharField()
    dt      = peewee.IntegerField()
    content = peewee.TextField()

    class Meta():
        database = db

def get_list():
    # TODO:
    #      1. Add start and end time
    #      2. Add limit
    URL = "http://news.cnyes.com/api/v2/news?limit=30"

    res = requests.get(URL)
    cnyes_list = ["http://news.cnyes.com/news/id/%s"%doc['newsId'] for doc in res.json()['items']['data']]

    return cnyes_list

def get_detail(url):
    """
    args:
        url: str, url for cnyes news article

    return:
        news_dict: dict, cnyes news with fields extracted 
          
    """
    news_dict = {}

    #logging.info("Getting <%s>"%url)
    print("getting <%s>"%url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html5lib')

    news_dict['url']     = url
    news_dict['title']   = soup.select_one("main > h1 > span").text
    dt = soup.select_one("main > h1 > div > time").text
    news_dict['dt']      = int(dp.parse(dt).timestamp())
    news_dict['content'] = soup.find('div', attrs={'itemprop': 'articleBody'}).text

    return news_dict

def to_db(data_list):
    with db.atomic():
        res = Cnyes.insert_many(data_list).execute()
    return res

# Run following code, only if this file is run standalone,
# aka not imported by another file
if __name__ == '__main__':
    cnyes_list = get_list()
    news_list = []
    for link in cnyes_list:
        news_list.append(get_detail(link))
    res = to_db(news_list)
    print(res)


