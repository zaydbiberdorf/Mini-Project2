from os.path import exists
from pymongo import MongoClient
from load_json import get_coll
from Colors import colors
from operations import searchArticle, searchAuthor, listVenue, addArticle, exitProgram

def sysStartUp():
    fileName = 'dblp-ref-1k.json'  #input("File Name: ")
    portNum = 60292  #input("Port Number (d = defult): ")
    if exists(fileName):
        db = get_coll(fileName, portNum)
        dblp = db["dblp"]
        sysHandler(dblp, db)
    else:
        print(colors.HEADER + fileName + colors.FAIL + " file does not exist" + colors.ENDC)
        sysStartUp() 

def sysHandler(dblp, db):
    while True:
        print(colors.HEADER + "\n Choose one of the following option: \n" + colors.ENDC)
        print("\t" + colors.HEADER + colors.BOLD + "[0] " + colors.ENDC +  "Search For Articles" )
        print("\t" + colors.HEADER + colors.BOLD + "[1] " + colors.ENDC +  "Search For Authors")
        print("\t" + colors.HEADER + colors.BOLD + "[2] " + colors.ENDC +  "List The Venues")
        print("\t" + colors.HEADER + colors.BOLD + "[3] " + colors.ENDC +  "Add an article")
        print(colors.FAIL + "\t[q] " + colors.ENDC + "Exit Program\n")

        # userChoice = input("choice: ") #input(colors.OKGREEN + "\nselection: " + colors.ENDC)
        userChoice = '1' #input(colors.OKGREEN + "\nselection: " + colors.ENDC)

        if userChoice == '1':
            searchArticle(db)
            break
        elif userChoice == '2':
            searchAuthor(dblp)
        elif userChoice == '3':
            listVenue(db)
            break 
        elif userChoice == '4':
            addArticle(db)
            break
        elif userChoice == 'q':
            print("good bye")
            exit()
    
if __name__ == "__main__":
    sysStartUp()



