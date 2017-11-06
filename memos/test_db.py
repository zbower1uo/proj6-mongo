import arrow
import pymongo
from pymongo import MongoClient

import config

CONFIG = config.configuration()


MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
    CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST, 
    CONFIG.DB_PORT, 
    CONFIG.DB)

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, CONFIG.DB)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

memo = { "type": "test_memo", 
       "date":  arrow.now().isoformat(),
       "text": "MEMO"
      }

def get():   
    records = [ ]
    for record in collection.find({"type": "test_memo"}):
        record['date'] = arrow.get(record['date']).isoformat()
        records.append(record)
    return records 

def same(real, expected):
    print(real, expected)
    return real == expected

def test_insertion():
    collection.insert(memo)
    col = get()
    assert same(col[0], memo)

def test_deletion():
    deleted = collection.delete_many(memo)
    print(deleted)
    assert deleted != 0

def test_empty():
    memos = get()
assert same(memos, [])

