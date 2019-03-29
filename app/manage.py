#coding=utf-8
"""
@author: AllenCHM
@contact: chengchuanming@itssoft.net
@file: manage.py
@datetime: 3/27/2019 1:21 PM
"""

from __future__ import unicode_literals
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Flask, request, json
import pymongo
import re
import requests
from lxml import etree


app = Flask(__name__)

conn = pymongo.MongoClient('127.0.0.1', connect=False)
doc = conn['books']['dhzw']
dhzw_detail = conn['books']['dhzw_detail']


@app.after_request
def after_request(response):
    print 'sssssssssssssssssss'
    response.headers.add("Access-Control-Allow-Origin", '*')
    response.headers.add("Access-Control-Allow-Headers", "X-Requested-With")
    response.headers.add("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
    # response.headers.add("Access-Control-Allow-Methods", "POST,GET")
    # response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Allow-Headers", "x-requested-with,content-type")
    return response

@app.route('/api/search', methods=['POST', "GET"])
def search():
    keyword = request.args.get('kw', '')
    page = int(request.args.get('page', 1))
    if not keyword or not keyword.strip():
        return ''
    else:
        result = []
        for i in doc.find({"book_desc":{"$exists":True},
                             "book_name": {'$regex': re.compile('.*{}.*'.format(keyword))}},
                        {'_id':0}).skip((page-1)*20).limit(20):
            result.append(i)
        return json.dumps(result)

@app.route('/api/book', methods=["GET"])
def get_book():
    auth_id = request.args.get('auth_id', '')
    book_id = request.args.get('book_id', '')
    if not auth_id or not book_id:
        return ''
    else:
        result = []
        for i in dhzw_detail.find({"auth_id":auth_id, "book_id":book_id}, {'_id':0}).sort([("id",1)]):
            i['href'] = 'http://book.bigdatas.top/api/book_content/'+i['href'][26:]
            result.append(i)
        return json.dumps(result)

@app.route('/api/book_content/<auth_id>/<book_id>/<content_id>.html')
def get_content(auth_id, book_id, content_id):
    print auth_id, book_id, content_id
    r = requests.get('https://www.dhzw.org/book/{}/{}/{}.html'.format(auth_id, book_id, content_id))
    print r.status_code
    hxs = etree.HTML(r.content.decode('gbk'))
    restul = etree.tostring(hxs.xpath('//div[@id="BookText"]')[0], encoding = "utf-8", pretty_print = True, method = "html")
    return restul



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
