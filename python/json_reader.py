import json

# Opening JSON file
f = open("../json/new_block.json", "r", )



# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json

list_cles = []
list_mail_fr = [] #1019
list_mail_en = [] #1651

#recuperation clés
for i in data[0]:
    list_cles.append(i)
#print(list_cles)

#tri/recuperation mail en/fr
for i in range(0,len(data)):
    if(data[i]["language"]=='fr'):
        list_mail_fr.append(data[i])
    else:
        list_mail_en.append(data[i])

#print(data[:]["_id"=='616f05117aa7db76cfd76ff7'])

    

# Closing file
f.close()
