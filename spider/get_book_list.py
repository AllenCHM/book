# -*- coding: utf-8 -*-

import sys

reload(sys)  # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
sys.setdefaultencoding('utf-8')


# 玄幻小说 https://www.dhzw.org/sort1/1.html
# 修真小说 https://www.dhzw.org/sort2/1.html
# 都市小说 https://www.dhzw.org/sort3/1.html
# 穿越小说 https://www.dhzw.org/sort4/1.html
# 网游小说 https://www.dhzw.org/sort5/1.html
# 科幻小说 https://www.dhzw.org/sort6/1.html

import requests
from lxml import etree
import pymongo
import time
import redis
import multiprocessing
import os


conn = pymongo.MongoClient('127.0.0.1', connect=False)
doc = conn['books']['dhzw']
r_conn = redis.StrictRedis('127.0.0.1')

headers = {
    'Host': 'www.dhzw.org',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}

def get_book_list_page(url):
    print 'get_url:', url
    r = requests.get(url, headers=headers)
    print r.status_code
    try:
        t = r.content.decode('gbk')
    except:
        raise EOFError('ttt')
    return t

def handle_page(response):
    h = etree.HTML(response)
    s = h.xpath('//div[@class="l"]/ul/li')
    book_list = []
    for i in s:
        # 作者id、作者名、书籍id、书名、最后更新时间、书籍分类
        url = i.xpath('.//span[@class="s2"]/a/@href')
        if url:
            auth_id = url[0].split('/')[-3]
            book_id = url[0].split('/')[-2]
        else:
            continue
        book_name = i.xpath('.//span[@class="s2"]/a/text()')[0]
        auth_name = i.xpath('.//span[@class="s4"]/text()')[0]
        category = i.xpath('.//span[@class="s1"]/text()')[0][1:-1]
        last_update = i.xpath('.//span[@class="s5"]/text()')[0]
        print 'get_one', auth_id, book_id, book_name,auth_name
        book_list.append({
            'auth_id': auth_id,
            'book_id': book_id,
            'book_name': book_name,
            'auth_name': auth_name,
            'category': category,
            'last_update': last_update,
        })
    return book_list

def handle_database(book_list):
    for i in book_list:
        doc.update({'auth_id':i['auth_id'], 'book_id':i['book_id']}, {'$set': i}, True)

def next_url(response):
    r_conn = redis.StrictRedis('127.0.0.1')

    h = etree.HTML(response)
    em = h.xpath('//em[@id="pagestats"]/text()')
    now_page, total_page = em[0].split('/')
    if int(now_page) < int(total_page):
        base_url = h.xpath('//div[@id="pagelink"]//a[@class="next"]/@href')
        if base_url:
            r_conn.lpush('need_spider', base_url[0])

def start_spider(url):
    print os.getpid(),'_____'
    r = get_book_list_page(url)
    next_url(r)
    print os.getpid(),'++++++'
    book_list= handle_page(r)
    print os.getpid(),'?????????'
    handle_database(book_list)

#

def fork_spider(lock):
    print os.getpid(),'fork --'
    r_conn = redis.StrictRedis('127.0.0.1')

    while True:
        # print os.getpid(), 'run  --'
        lock.acquire()
        url = r_conn.lpop('need_spider')
        lock.release()
        if not url:
            time.sleep(0.1)
            continue
        if r_conn.get(url):
           continue
        print os.getpid(), url
        try:
            start_spider(url)
            r_conn.set(url, 1)
        except IndexError:
            r_conn.rpush('need_spider', url)
        except EOFError:
            pass


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    for k in xrange(2, 7):
        for i in xrange(0, 200, 10):
            r_conn.lpush('need_spider', 'https://www.dhzw.org/sort{}/{}.html'.format(k, i))

    # lock = 1
    pool = multiprocessing.Pool(processes=20)
    for i in xrange(20):
        pool.apply_async(func=fork_spider, args=(lock, ) )
    pool.close()
    pool.join()