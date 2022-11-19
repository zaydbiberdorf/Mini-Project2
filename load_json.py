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
    
    items = []
    with open(fileName, 'r', encoding='utf-8') as f:    
        for line in f:
            items.append(json.loads(line))

    dblp.insert_many(items)
    
    # title, authors, abstract, venue and year
    db.dblp.drop_indexes()
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

    return db
