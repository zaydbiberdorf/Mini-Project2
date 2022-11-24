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
    cmd = f"mongoimport --db=291db --collection=dblp --port={portNum} --file={fileName} --batchSize=10000 --numInsertionWorkers=20"
    os.system(cmd)

@timing
def get_coll(fileName, portNum): 
    cl = MongoClient('localhost', portNum)
    db = cl["291db"]
    dblp = db["dblp"]
    venue_col = db["venue_col"] 
    dblp.delete_many({})
    venue_col.delete_many({})
    #import documents using mongoimport
    import_docs(fileName, portNum) 

    #update year field to string
    db.dblp.update_many({},
        [{ "$set": { 
                "year": {"$toString": "$year"}
            }
        }]
    ) 
    #pre processing for venue
    venueQuery = False
    if venueQuery:
        db.dblp.aggregate([
            { "$match" : { "venue" : {"$ne" : ""}} }, 
            {
                "$group" : {
                    "_id" : "$venue",
                    "countVenue": {"$sum" : 1},
                    "keepIds" : {"$addToSet" : "$id"}
                }
            },  
            { "$sort" : {"countVenue" : -1}}, 
            { 
                "$project" : {
                    "_id" : "$id",
                    "venue" : "$_id",
                    "keepIds" : 1,
                    "countVenue" : 1
                }
            },
            { "$out" : "venue_col"}
        ]) 

    #create venue index
    db.venue_col.create_index([("_id", 1)])
    db.dblp.create_index([("references", 1)])
    #creat text indexes
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
