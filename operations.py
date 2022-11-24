import re
from Colors import colors
from rich.console import Console
from rich.table import Table
import pprint
from functools import wraps
from time import time
import pymongo
from load_json import timing

''' 
Here's some test cases you guys can try for the 1.2 GB file:
search articles with keywords "Technology bRain"(number of results: 441 results),
"Database" (number of results: 33160), "John Research International"(number of results: 708)

search author with keyword "A"(number of results: 26445), "Dave" (number of results: 296), 
"Yao" (number of results: 1030), "Wang" (number of results: 7360)
'''

'''
 Search for articles The user should be able to provide one or more keywords, 
 and the system should retrieve all articles that match all those keywords (AND semantics). 
 A keyword matches if it appears in any of title, authors, abstract, venue and year fields 
 (the matches should be case-insensitive). For each matching article, display the id, 
 the title, the year and the venue fields. The user should be able to select an article to 
 see all fields including the abstract and the authors in addition to the fields shown before. 
 If the article is referenced by other articles, the id, the title, and the year of those 
 references should be also listed.   
'''
@timing
def searchArticle(db):
    print(colors.OKGREEN+"Search for Article"+colors.ENDC)
    keywords = input("Search for sapce separated keywords: ").split(" ") 
    key_str = ""
    for key in keywords:
        q_wrp = "\\"+"\"" + key.lower() + "\"" + "\\"
        key_str += q_wrp
 
    dblp = db["dblp"] 
    results = list(dblp.aggregate([
        { "$match" : { 
            "$text" : { "$search" : key_str } 
            } 
        } 
    ]))
    it = 0
    size = len(results)
    while it < size:
        i = it
        while i < (it+4) and i < size:
            print("="*80+"\n"         
            +colors.HEADER + "ARTICLE #"+ str(i) + colors.ENDC + "\n"
            +"ID: "+ str(results[i]["id"])+"\n"
            +"TITLE: "+ str(results[i]["title"]) + "\n"
            +"YEAR: "+ str(results[i]["year"]) + "\n"
            +"VENUE: "+ str(results[i]["venue"])
            )
            i += 1
        choice = input("select index for more information on the article or any other key to see next page")
        if choice.isdigit():
            article = results[int(choice)]
            print(colors.HEADER+"\nmore information about article #"+choice+" "+str(article["title"])+colors.ENDC+"\n")
            more_info = dblp.find({"id" : article["id"]})
            for info in more_info:
                
                abstractExists = len(list(dblp.find({"id": info["id"], "abstract": {"$exists": "true"}})))  
                if abstractExists != 0:
                    print("More Info:\n\n"+"Abstract: "+info["abstract"])
                    for author in info["authors"]:
                        print("Author: ", author)

                r_count = 0
                referencesExist = len(list(dblp.find({"id": info["id"], "references": {"$exists": "true"}})))  
                if referencesExist:
                    for ref in info["references"]:
                        print(ref)
                        full_ref = dblp.find({"id ": ref})
                        #NEED TO PRINT REFERENCE ARTICLE INFO HERE
                print("YEAR:"+str(info["year"]))
                print("TITLE: "+str(info["title"]))
                print("VENUE: "+str(info["venue"]))
            break
        else:
            it += 5 

@timing
def searchAuthor(dblp):
    pass

@timing
def listVenue(db):
    #query number of articles published for each venue
    dblp = db["dblp"]
    mini_dblp = db["mini_dblp"]
    n = 10 

    results = mini_dblp.aggregate([
        { "$match" : { "venue" : {"$ne" : ""}} }, 
        {
            "$lookup" : {
                "from" : "dblp",     
                "let" : {
                    "id" : "$keepId"
                },
                "pipeline" : [ 
                    {
                        "$match" : {
                            "references" : {"$exists" : "true"}, 
                            "$expr" : {"$in" : ["$$id", "$references"]}
                        }
                    },
                    {
                        "$project" : {
                            "_id" : 0,
                            "id" : 1,
                            "venue" : 1
                        }
                    }
                ],
                "as" : "referenced_by"
            }
        },
        {
            "$group" : {
                "_id" : "$venue",
                "countVenue" : {"$sum" : 1},
                "countReferences" : {"$sum" : {"$size" : "$referenced_by"}}
            }
        },
        { "$sort" : {"countReferences" : -1}},
        { "$limit" : n }
    ])

    for r in results:
        print("-"*45)
        print(r)
    return

def addArticle(db):
    
    uniqueId = "abc"
    title = "my article"
    authors = []
    year = "2022"

    article = {
        "abstract" : "",
        "authors" : authors,
        "n_citation" : 0,
        "title" : title,
        "venue" : "",
        "year" : year,
        "id" : uniqueId
    }
    dblp = db["dblp"]
    dblp.insert_one(article)

def exitProgram(dblp):
    pass