# -*- coding: utf-8 -*-

import sys

reload(sys)  # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

import requests

import pymongo
from lxml import etree
import time
import multiprocessing
import os
import redis

conn = pymongo.MongoClient('127.0.0.1', connect=False)
doc = conn['books']['dhzw']
doc_detail = conn['books']['dhzw_detail']
r_conn = redis.StrictRedis('127.0.0.1')

headers = {
    'Host': 'www.dhzw.org',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}

url = 'https://www.dhzw.org/book/358/358318/'


def get_book_detail(url):
    r = requests.get(url, headers=headers)
    t = r.content.decode('gbk')

    h = etree.HTML(t)
    book_status = h.xpath('//div[@id="info"]//i/text()')[-1].split('：')[-1]
    # 书籍描述、书籍状态、章节信息（章节名、章节下载地址）
    book_desc = etree.tostring(h.xpath('//div[@id="info"]//div[@class="intro"]')[0])
    tmp = h.xpath('//div[@id="list"]//dd')
    book_chapter_list =[]
    for i in tmp:
        try:
            name = i.xpath('./a/@title')[0]
        except:
            continue
        print name
        href = i.xpath('./a/@href')[0]
        book_chapter_list.append({
            'name':name,
            'href':url+href
        })
    auth_id = url.split('/')[-3]
    book_id = url.split('/')[-2]
    doc.update({'auth_id':auth_id, 'book_id':book_id}, {'$set': {'book_desc': book_desc, 'book_status':book_status}})
    for i in book_chapter_list:
        doc_detail.update({'auth_id':auth_id, 'book_id':book_id, 'name':i['name']}, {'$set':i}, True)

def test(lock):
    print os.getpid(), 'fork --'
    r_conn = redis.StrictRedis('127.0.0.1')
    while True:
        lock.acquire()
        url = r_conn.lpop('need_spider_detail')
        lock.release()
        if not url:
            time.sleep(0.1)
            continue
        if r_conn.get(url):
            continue
        print os.getpid(), url
        try:
            get_book_detail(url)
            r_conn.set(url, 1)
        except IndexError:
            r_conn.rpush('need_spider_detail', url)
        except EOFError:
            pass


if __name__:
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    for i in doc.find():
        r_conn.lpush('need_spider_detail', 'https://www.dhzw.org/book/{}/{}/'.format(i["auth_id"], i["book_id"]))


    pool = multiprocessing.Pool(processes=20)
    for i in xrange(20):
        pool.apply_async(func=test, args=(lock,))
    pool.close()
    pool.join()
# get_book_detail(url)