import re
from Colors import colors
from rich.console import Console
from rich.table import Table
<<<<<<< Updated upstream


def searchArticle(dblp):
    # Search for articles The user should be able to provide one or more keywords, 
    # and the system should retrieve all articles that match all those keywords (AND semantics). 
    # A keyword matches if it appears in any of title, authors, abstract, venue and year fields 
    # (the matches should be case-insensitive). For each matching article, display the id, the title, 
    # the year and the venue fields. The user should be able to select an article to see all fields 
    # including the abstract and the authors in addition to the fields shown before. If the article is 
    # referenced by other articles, the id, the title, and the year of those references should be also listed.
    keys = input(colors.OKGREEN + "search: " + colors.ENDC)
    # keys = re.split(r'\s+', keys)
    
    # keys = list(set(keys))
    # keys = [str(key) for key in keys]


    # creating tables
    table = Table(title="Article Search Result", show_header=True, header_style="bold magenta", padding=1)
    table2 = Table(title="Article Search Result", show_header=True, header_style="bold magenta", padding=1)

    # adding columns to table
    table.add_column("Number")
    table.add_column("id")
    table.add_column("title")
    table.add_column("venue")
    table.add_column("year")

    # adding columns to table2
    table2.add_column("id")
    table2.add_column("author")
    table2.add_column("title")
    table2.add_column("venue")
    table2.add_column("year")
    table2.add_column("abstract")
   
    
    ids = []
    # quering for the search key
    for doc in dblp.find({"$text": {"$search": keys}}, {"id": 1, "title": 1,  "venue": 1, "year": 1}):
        ids.append(doc['id'])
        table.add_row(str(len(ids)), str(doc['id']), str(doc['title']), str(doc['venue']), str(doc['year']))

    # if there is one or more matches:
    #       than print table and ask if they want to look at an article
    if len(ids) > 0:
        Console().print(table)
        print("If you would like to select an article please provide the number of article otherwise press enter")
        selectionNumber = input(colors.OKGREEN + "Number: " + colors.ENDC)
        

        
        
        if selectionNumber != "" and selectionNumber.isnumeric():
            for doc in dblp.find({"$or": [{"id": ids[int(selectionNumber) - 1]}, {"references": ids[int(selectionNumber) - 1]}]}, {"id": 1, "title": 1,  "venue": 1, "year": 1, "abstract": 1, "authors": 1}):
                table2.add_row(str(doc['id']), str(doc['authors']), str(doc['title']), str(doc['venue']), str(doc['year']))


            Console().print(table2)

    else:
        print(colors.WARNING + "No Matches" + colors.ENDC)
    
            


def searchAuthor(dblp):
    """
    For each author, list the author name and the number of publications. 
    The user should be able to select an author and see the title, year and 
    venue of all articles by that author. The result should be sorted based
    on year with more recent articles shown first.
    """

    key = input(colors.OKGREEN + "search: " + colors.ENDC)
    # key = ("/" + key + "/")

    # creating tables
    table = Table(title="Article Search Result", show_header=True, header_style="bold magenta", padding=1)
    table2 = Table(title="Article Search Result", show_header=True, header_style="bold magenta", padding=1)

    # adding columns to table
    table.add_column("Number")
    table.add_column("author")
    table.add_column("number of publications")


    # adding columns to table2
    
    table2.add_column("title")
    table2.add_column("year")
    table2.add_column("venue")
    


    # db.collection.count({$text:{$search:term}});


    authors = []
    # quering for the search key
    for doc in dblp.find({"$text": {"$search": key}}, {"id": 1, "authors": 1}):
        for author in doc["authors"]:
            if key in author:
                authors.append(author)
                table.add_row(str(len(authors)), str(author), str(dblp.count_documents({"authors": author})))

    
    Console().print(table)

    # if there is one or more matches:
    # than print table and ask if they want to look at an article
    if len(authors) > 0:
        Console().print(table)
        print("If you would like to select an article please provide the number of article otherwise press enter")
        selectionNumber = input(colors.OKGREEN + "Number: " + colors.ENDC)
        

        
        
        if selectionNumber != "" and selectionNumber.isnumeric():
            for doc in dblp.find({"authors": authors[int(selectionNumber) - 1]}, {"title": 1,  "venue": 1, "year": 1}):
                table2.add_row(str(doc['title']), str(doc['year']), str(doc['venue']))


            Console().print(table2)

    else:
        print(colors.WARNING + "No Matches" + colors.ENDC)
    


def listVenue(dblp):
    pass

def addArticle(dblp):

=======
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
                
                abstractExists = len(list(dblp.find({"id": info["id"], "abstract": {"$exists": "true"}})))  
                if abstractExists != 0:
                    print("More Info:\n\n"+"Abstract: "+info["abstract"])
                    for author in info["authors"]:
                        print("Author: ", author)

                print("YEAR:"+str(info["year"]))
                print("TITLE: "+str(info["title"]))
                print("VENUE: "+str(info["venue"]))


                
                refrences =  list(dblp.find({"references": info["id"]}, {"id": 1, "title": 1,  "venue": 1, "year": 1, "abstract": 1, "authors": 1}))
                for ref in refrences:
                    print("="  * 80)
                    print("title: ", ref["title"])
                    print("year: ", ref["year"])
                    print("venue: ", ref["venue"])
                    print("id: ", ref["id"])

                    
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
            "$match" : {'authors': {"$regex": keyword}} 
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
    dblp = db["dblp"]
>>>>>>> Stashed changes
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
    dblp.insert_one({"id": uid, "title": title, "authors": authors, "year": year, "abstract": "Null", "venue": "Null", "references": [], "n_citations": 0})
<<<<<<< Updated upstream
=======
    print(colors.HEADER+"Added article to dblp..."+colors.ENDC)

def exitProgram(dblp):
    pass






>>>>>>> Stashed changes
