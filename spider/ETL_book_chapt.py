#coding=utf-8
"""
@author: AllenCHM
@contact: chengchuanming@itssoft.net
@file: ETL_book_chapt.py
@datetime: 3/27/2019 1:49 PM
"""

from __future__ import unicode_literals
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo

conn = pymongo.MongoClient('127.0.0.1', connect=False)
dhzw_detail = conn['books']['dhzw_detail']

for i in dhzw_detail.find({}, {'_id':1, "href":1}):
    id = i['href'].split('/')[-1].split('.')[0]
    dhzw_detail.update({'_id':i["_id"]}, {"$set":{'id': int(id)}})
    print id
