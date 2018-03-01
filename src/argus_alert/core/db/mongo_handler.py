# coding=utf-8
"""
"""


if __name__ == '__main__':
    pass

    from pymongo import MongoClient

    mg = MongoClient('mongodb://localhost:27017')
    db = mg['tutotial']
    collection = db['numbers']
    for e in collection.find():
        print(e)