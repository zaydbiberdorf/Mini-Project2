# dblp-ref-1k.json

from os.path import exists
from pymongo import MongoClient
from load_json import get_coll
from Colors import colors
from operations import searchArticle, searchAuthor, listVenue, addArticle

def sysStartUp():
    # get user input (file name and portnumber)
    print("please provide the following:")
    fileName = 'dblp-ref-1k.json'  #input("File Name: ")
    portNum = 27017 #input("Port Number (d = defult): ")
    # allowing user to select defult portnumber (27017)
    if portNum == 'd':
        portNum = 27017
    
    if exists(fileName):
        # getting the collection based on user input
        dblp = get_coll(fileName, portNum)
        sysHandler(dblp)

    else:
        print(colors.HEADER + fileName + colors.FAIL + " file does not exist" + colors.ENDC)
        sysStartUp()

    


def sysHandler(dblp):
    while True:
        print(colors.HEADER + "\n Choose one of the following option: \n" + colors.ENDC)
        print("\t" + colors.HEADER + colors.BOLD + "[0] " + colors.ENDC +  "Search For Articles" )
        print("\t" + colors.HEADER + colors.BOLD + "[1] " + colors.ENDC +  "Search For Authors")
        print("\t" + colors.HEADER + colors.BOLD + "[2] " + colors.ENDC +  "List The Venues")
        print("\t" + colors.HEADER + colors.BOLD + "[3] " + colors.ENDC +  "Add an article")
        print(colors.FAIL + "\t[q] " + colors.ENDC + "Exit Program\n")

        userChoice = input(colors.OKGREEN + "\nselection: " + colors.ENDC)

        if userChoice == '0':
            searchArticle(dblp)
        elif userChoice == '1':
            searchAuthor(dblp)
        elif userChoice == '2':
            listVenue(dblp)
        elif userChoice == '3':
            addArticle(dblp)
        elif userChoice == 'q':
            print("good bye")
            exit()
    


if __name__ == "__main__":
    sysStartUp()




