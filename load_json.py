from pymongo import *
import json
import os

# need to figure out how to do batch sizes
def get_coll(fileName, portNum):
    cl = MongoClient('localhost', portNum)
    db = cl["291db"]
    dblp = db["dblp"]
    venue_col = db["venue_col"]
    dblp.delete_many({})
    venue_col.delete_many({})

    objs = []     
    with open("dblp-ref-1k.json") as f:
        for line in f:
            objs.append(json.loads(line))

    dblp.insert_many(objs)
    venue_col.insert_many(objs)
    
    # title, authors, abstract, venue and year
    db.dblp.drop_indexes()
    db.venue_col.drop_indexes() 
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
    db.venue_col.create_index(
        [
        ("title", TEXT),
        ("authors", TEXT),
        ("abstract", TEXT), 
        ("venue", TEXT),
        ("year", TEXT),
        ("id", TEXT)
        ]
    )

    return db
