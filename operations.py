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
    dblp = db["dblp"] 
    print(colors.OKGREEN+"Search for Article"+colors.ENDC)
    keywords = input("Search for sapce separated keywords: ").split(" ") 
    key_str = ""
    for key in keywords:
        q_wrp = "\\"+"\"" + key.lower() + "\"" + "\\"
        key_str += q_wrp
 
    results = list(dblp.aggregate([
        { "$match" : { 
            "$text" : { "$search" : key_str } 
            } 
        } 
    ]))
    it = 0
    size = len(results)
    print(colors.HEADER+"Number of Results: " + str(size)+colors.ENDC)
    while it < size:
        i = it
        while i < (it+4) and i < size:
            print("="*80+"\n"         
            +colors.HEADER + "ARTICLE #"+ str(i) + colors.ENDC + "\n"
            +"Id:\t"+ str(results[i]["id"])+"\n"
            +"Title:\t"+ str(results[i]["title"]) + "\n"
            +"Year:\t"+ str(results[i]["year"]) + "\n"
            +"Venue:\t"+ str(results[i]["venue"])
            )
            i += 1
        print("="*80)
        print(colors.HEADER+"Number of Results: " + str(size)+colors.ENDC)
        choice = input("select index for more information on the article or any other key to see next page")
        if choice.isdigit():
            article = results[int(choice)]
            print(colors.HEADER+"\nmore information about article #"+choice+" "+str(article["title"])+colors.ENDC+"\n")
            more_info = dblp.find({"id" : article["id"]})
            for info in more_info:

                print(colors.HEADER + "YEAR:  " + colors.ENDC + str(info["year"]))
                print(colors.HEADER + "TITLE: " + colors.ENDC + str(info["title"]))
                print(colors.HEADER + "VENUE: " + colors.ENDC + str(info["venue"]))
                
                abstractExists = len(list(dblp.find({"id": info["id"], "abstract": {"$exists": "true"}})))  
                if abstractExists != 0:
                    print("Abstract: "+info["abstract"])
                    for author in info["authors"]:
                        print("Author: ", author)
                else:
                    print(colors.HEADER+"Abstract: "+colors.ENDC+"No Abstract")

                r_count = 0
                referencesExist = len(list(dblp.find({"id": info["id"], "references": {"$exists": "true"}})))  
                if referencesExist:
                    for ref in info["references"]:
                        refs = db.dblp.aggregate([{
                            "$match" : { 
                                "$expr" : {"$eq" : ["$id", ref]} 
                            } 
                        }]) 
                        for r in refs:
                            print("="*80)
                            print("Article Referenced by Chosen Article:")
                            print(colors.HEADER+"Id: "+colors.ENDC+r["id"])
                            print(colors.HEADER+"Title: "+colors.ENDC+r["title"])
                            print(colors.HEADER+"Year: "+colors.ENDC+r["year"])
                            print("="*80)
                else:
                    print("No References!") 
            break
        else:
            it += 5 

''' 
 Search for authors The user should be able to provide a keyword  and see all authors 
 whose names contain the keyword (the matches should be case-insensitive). For each author,
 list the author name and the number of publications. The user should be able to select an 
 author and see the title, year and venue of all articles by that author. The result should 
 be sorted based on year with more recent articles shown first.
'''
@timing
def searchAuthor(db):
    dblp = db["dblp"]
    
    keyword = input("="*80+"\n"+colors.HEADER+"Artist Search: "+colors.ENDC)
    regex = f"{keyword}"
    results = list(dblp.aggregate([
        {
            "$match" : {"$text" : {"$search" : keyword}}
        }, 
        {
            "$unwind" : "$authors"
        },
        { 
            "$match" : {'authors': {"$regex": keyword, "$options" : "i"}} 
        }
    ]))
    unique_auth = set()
    unique_results = []
    for auth in results:
        if auth["authors"] not in unique_auth:
            unique_auth.add(auth["authors"])   
            unique_results.append(auth)
    it = 0
    numAuthors = len(unique_results)
    print("Number of authors: "+str(numAuthors))
    while it < numAuthors:
        i = it
        while i < (it+10) and i < numAuthors:
            author = unique_results[i]["authors"]
            publications = list(dblp.aggregate([
                {
                    "$match" : {
                    "$expr"  : {
                        "$in" : [author, "$authors"]
                        }
                    }
                }
            ])) 
            print("="*80)
            print(colors.HEADER+f" [{i}] "+"Author: "+author+colors.ENDC)
            print("# of publications: "+ str(len(publications)))
            i += 1
        choice = input("select index for more information on the article or any other key to see next page ")
        if choice.isdigit():
            auth = unique_results[int(choice)] 
            print("="*80)
            print(colors.HEADER+"Selected Author: "+colors.ENDC+auth["authors"])
            author_publications = list(dblp.aggregate([
                {
                    "$match" : {
                    "$expr"  : {
                        "$in" : [auth["authors"], "$authors"]
                        }
                    }
                },
                {
                    "$sort" : {"year": -1}
                }
            ])) 
            for p in author_publications:
                print(colors.HEADER+"published article: "+colors.ENDC+p["id"])
                published_article = dblp.find({"id": p["id"]})
                for pa in published_article:
                    print(colors.HEADER+"Title: "+colors.ENDC+pa["title"])
                    print(colors.HEADER+"Year: "+colors.ENDC+str(pa["year"]))
                    if pa["venue"] == "":
                        print(colors.HEADER+"Venue: "+colors.ENDC+"None")
                    else:
                        print(colors.HEADER+"Venue: "+colors.ENDC+pa["venue"])
                    print("="*80)
            break
        else:
            it += 10 
    print("="*80)

@timing
def listVenue(db):
    #query number of articles published for each venue
    dblp = db["dblp"]
    mini_dblp = db["mini_dblp"]
    n = 10 

    '''
    function not working
    '''
    return

    # results = mini_dblp.aggregate([
    #     { "$match" : { "venue" : {"$ne" : ""}} }, 
    #     {
    #         "$lookup" : {
    #             "from" : "dblp",     
    #             "let" : {
    #                 "id" : "$keepId"
    #             },
    #             "pipeline" : [ 
    #                 {
    #                     "$match" : {
    #                         "references" : {"$exists" : "true"}, 
    #                         "$expr" : {"$in" : ["$$id", "$references"]}
    #                     }
    #                 },
    #                 {
    #                     "$project" : {
    #                         "_id" : 0,
    #                         "id" : 1,
    #                         "venue" : 1
    #                     }
    #                 }
    #             ],
    #             "as" : "referenced_by"
    #         }
    #     },
    #     {
    #         "$group" : {
    #             "_id" : "$venue",
    #             "countVenue" : {"$sum" : 1},
    #             "countReferences" : {"$sum" : {"$size" : "$referenced_by"}}
    #         }
    #     },
    #     { "$sort" : {"countReferences" : -1}},
    #     { "$limit" : n }
    # ])
    # for r in results:
    #     print("-"*45)
    #     print(r)
    # return

def addArticle(db): 
    dblp = db["dblp"]
    # gettiing user input
    print("please provide the following: ")
    # ensuring uniqueness of id
    unique = False
    while(not unique):
        uid = input("id: ")
        if len(list(dblp.find({"id": uid}))) > 0:
            print(colors.WARNING + "id not unique, please try another" + colors.ENDC)
        else:
            unique = True
    title = input("title: ")
    authors = input("authors (if many seporate by a ','): ")
    authors = authors.split(",")
    year = input("year: ")
    
    # inserting into database 
    dblp.insert_one({"id": uid, "title": title, "authors": authors, "year": int(year), "abstract": "", "venue": "", "references": [], "n_citations": 0})
    print(colors.HEADER+"Added article to dblp..."+colors.ENDC)

def exitProgram(dblp):
    pass