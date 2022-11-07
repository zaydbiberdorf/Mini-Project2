from pymongo import MongoClient
import json
import os




# need to figure out how to do batch sizes
def get_coll(fileName, portNum):
    cl = MongoClient('localhost', portNum)

    db = cl["291db"]

    dblp = db["dblp"]

    dblp.delete_many({})


    os.system("mongoimport --db=291db --collection=dblp --file=" + fileName + " --batchSize=100000")


    return dblp
