import re
from Colors import colors
from rich.console import Console
from rich.table import Table


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
    pass

def listVenue(db):
    #query number of articles published for each venue
    dblp = db["dblp"]
    venue_col = db["venue_col"]
    # venue_col.update_many(
    #     {},
    #     { "$set": {"referenced_by": []} }
    # )  

    results = venue_col.aggregate([
        {
            # "$lookup" : {
            #     "from" : "dblp", 
            #     "localField" : "id",
            #     "foreignField": "id",
            #     "as" : "referenced_by"
            # },
            
            "$lookup" : {
                "from" : "dblp", 
                "let" : {
                    "id" : "$id", 
                    "refs": "$references" 
                },
                "pipeline" : [
                    # {"$match" : {"$expr" : {"$in" : ["id", "$$refs"]}}}
                    {"$match" : {"$expr" : {"$eq" : ["$id", "$$id"]}}}
                    # {"$match" : {"$expr" : {"$elem" : ["$id", "$$id"]}}}
                ],
                "as" : "referenced_by"
            }
        },
        {
            "$limit" : 3
        }
    ])
    for r in results:
        print(r["id"], "references",  r["references"], "referenced_by", r["referenced_by"])
    
    # print(r["_id"])

    '''
    dblp = db["dblp"]
    venue_col = db["venue_col"]
    
    #experiment
    results = dblp.aggregate([ 
        {
            "$group" : {
                "_id" : {
                    "venue" : "$venue"
                },
                "countVenue" : {"$sum" : 1}
            },
        },
        # {
        #     "$lookup" : {
        #         "from": "dblp",
        #         "pipeline" : [
        #             # {
        #             #     "$match" : {"_id" : {"$in" : "$references"}}
        #             # }
        #         ],
        #         "as": "refs"
        #     } 
        # }, 
        {
            "$sort" : {"countVenue" : -1}
        },
        {
            "$project" : {"_id" : 0, "venue" : "$_id.venue", "countVenue" : 1 }
        },
        {
            "$limit" : 10
        }
    ])

    for doc in results:
        print(doc)

    # results2 = dblp.aggregate([
    #     {} 
    # ])
    # for doc in results2:
    #     print(doc)
    

    '''
    '''
    results = dblp.aggregate([ 
            {
                "$group" : {
                    "_id" : {"venue" : "$venue"},
                    "countVenue" : {"$sum" : 1}
                }
            }, 
            {
                "$sort": {
                    "countVenue": -1
                } 
            },
            {
                "$limit": 5
            }, 
            {
                "$project" : {"venue" : "$_id.venue", "_id" : 0, "countVenue" : 1, "id" : "$_id.id"} 
            }

    ])
    for r in results:
        print(r) 
    '''

    '''
    #experiment
    results = dblp.aggregate([ 
        {
            "$lookup" : {
                "from" : "dblp",
                "let": {"venueVar": "$venue"},
                "pipeline" : [
                    {"$match": {"venue" : "$venueVar"}}
                ],
                "as" : "venueJoin"
            }
        },
        {
            "$limit": 5
        },
        {
            "$project" : {"_id" : 0, "id" : "$_id", "venue" : 1, "venueJoin" : 1, "venueVar" : 1} 
        }
    ])

    for doc in results:
        print(doc)

    '''
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