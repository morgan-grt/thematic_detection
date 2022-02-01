import json
import constants

def read_file(filename):
    f = open(constants.BASE_PATH_UPLOAD+filename, "r")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    list_cles = []
    list_mail = [] #1019 fr + 1651 en

    #recuperation cles
    for i in data[0]:
        list_cles.append(i)
    #print(list_cles)

    #tri/recuperation mail en/fr
    for i in range(0,len(data)):
        list_mail.append((data[i]["language"], data[i]))

    # Closing file
    f.close()
    return list_cles, list_mail
    
