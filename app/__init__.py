#coding=utf-8
"""
@author: AllenCHM
@contact: chengchuanming@itssoft.net
@file: __init__.py.py
@datetime: 3/26/2019 7:35 PM
"""

from __future__ import unicode_literals
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Flask, request, json
import pymongo
import re

app = Flask(__name__)

conn = pymongo.MongoClient('127.0.0.1', connect=False)
doc = conn['books']['dhzw']
dhzw_detail = conn['books']['dhzw_detail']


@app.route('/search', methods=['POST', "GET"])
def search():
    print '-----'
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

@app.route('/book', methods=["GET"])
def get_book():
    auth_id = request.args.get('auth_id', '')
    book_id = request.args.get('book_id', '')
    if not auth_id or not book_id:
        return ''
    else:
        result = []
        for i in dhzw_detail.find({"auth_id":auth_id, "book_id":book_id}, {'_id':0}):
            result.append(i)
        return json.dumps(result)

if __name__ == "__main__":
    app.run('0.0.0.0', port=80, debug=True)