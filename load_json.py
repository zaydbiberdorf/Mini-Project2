from pymongo import *
import json
import os

# need to figure out how to do batch sizes
def get_coll(fileName, portNum):
    cl = MongoClient('localhost', portNum)
    db = cl["291db"]
    dblp = db["dblp"]
    dblp.delete_many({})

    objs = []     
    with open(fileName) as f:
        for line in f:
            objs.append(json.loads(line))

    # print("Completed appending to the insert list")
    dblp.insert_many(objs)
    # print("Completed insertion")
    
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
    # print("Completed index creation")

    return db
