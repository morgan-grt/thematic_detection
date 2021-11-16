import json
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))



def read_file(filename):
    f = open(os.getcwd()+'/api/upload/'+filename, "r")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json

    list_cles = []
    list_mail_fr = [] #1019
    list_mail_en = [] #1651

    #recuperation cles
    for i in data[0]:
        list_cles.append(i)
    #print(list_cles)

    #tri/recuperation mail en/fr
    for i in range(0,len(data)):
        if(data[i]["language"]=='fr'):
            list_mail_fr.append(data[i])
        else:
            list_mail_en.append(data[i])

    # Closing file
    f.close()
    return list_cles, list_mail_fr, list_mail_en
    
