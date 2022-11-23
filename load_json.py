from pymongo import *
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
    mini_dblp = db["mini_dblp"]
    dblp.delete_many({})
    mini_dblp.delete_many({})

    import_docs(fileName, portNum) 

    print("imported documents") 
    # title, authors, abstract, venue and year
    db.dblp.drop_indexes()
    db.mini_dblp.drop_indexes()

    db.dblp.create_index(
       [
        ("title", TEXT),
        ("authors", TEXT),
        ("abstract", TEXT), 
        ("venue", TEXT),
        ("year", TEXT),
        ("id", TEXT)
        ]
    )
    db.dblp.create_index([("references", 1)], name="referencesIndex")
    db.dblp.create_index([("id", 1)], name="idIndex")
   
    db.mini_dblp.create_index([("keepId", 1)], name="miniKeepIdIndex")
    db.mini_dblp.create_index([("venue", 1)], name="miniVenueIndex")
    
    #make materialized view of id in top venues so later lookup stage can be performed on a smaller subset of documents
    db.dblp.aggregate([
        { "$match" : { "venue" : {"$ne" : ""}} }, 
        {
            "$group" : {
                "_id" : "$venue",
                "countVenue": {"$sum" : 1},
                "keepId" : {"$addToSet" : "$id"}
            }
        },  
        { "$sort" : {"countVenue" : -1}}, 
        { "$limit" : 3403},
        { "$unwind" : "$keepId"},
        { 
            "$project" : {
            "_id" : 0, 
            "keepId" : 1,
            "venue" : "$_id"
            }
        },
        { "$out" : "mini_dblp"}
    ])
    return db
