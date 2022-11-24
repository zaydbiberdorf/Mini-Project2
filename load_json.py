from pymongo import *
import pymongo
import json
import os
from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'Function {f.__name__} took {te-ts:2.4f} seconds')
        return result
    return wrap

@timing
def import_docs(fileName, portNum):
    cmd = f"mongoimport --db=291db --collection=dblp --port=60292 --file={fileName} --batchSize=10000 --numInsertionWorkers=20"
    os.system(cmd)

@timing
def get_coll(fileName, portNum): 
    cl = MongoClient('localhost', portNum)
    db = cl["291db"]
    dblp = db["dblp"]
    dblp.delete_many({})
    #import documents using mongoimport
    import_docs(fileName, portNum) 

    db.dblp.create_index(
        keys=[
        ("title", pymongo.TEXT),
        ("authors", pymongo.TEXT),
        ("abstract",  pymongo.TEXT), 
        ("venue", pymongo.TEXT),
        ("year", pymongo.TEXT)
        ],
        default_language="none",
        name="textIndex"
    )
    return db
