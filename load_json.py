from pymongo import *
import json
import os

# need to figure out how to do batch sizes
def get_coll(fileName, portNum):
    cl = MongoClient('localhost', portNum)
    db = cl["291db"]
    dblp = db["dblp"]
    dblp.delete_many({})

    print(fileName)
    cmd = f"mongoimport --db=291db --collection=dblp --port=60292 --file={fileName} --batchSize=10000"

    # print(cmd)
    os.system(cmd)
    
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
    db.dblp.create_index([("references", -1)], name="referencesIndex")

    return db
