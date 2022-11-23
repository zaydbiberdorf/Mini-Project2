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
    with open("dblp-ref-1k.json") as f:
        for line in f:
            objs.append(json.loads(line))

    dblp.insert_many(objs)


    # os.system("mongoimport --db=291db --collection=dblp --file=" + fileName + " --batchSize=100000000")
    # with open(fileName) as file:
    #     file_data = json.load(file)

    # db.dblp.insert_many(file_data)
    # print("done pase one")
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


    return dblp
