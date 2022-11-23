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
