import xml_reader as rxml
import json_reader as rjson
import json
import collections
from datetime import datetime

def search_in(label, item):
    item_split = item.split()
    label_split = label.split()

    label_bool = [False for lab in label_split] 

    for j in range(0, len(item_split) - len(label_split)):
        if label_split[0] == item_split[j]:
            label_bool[0] = True
            for k in range(1, len(label_split)):
                if label_split[k] == item_split[j+k]:
                    label_bool[k] = True

    return all(label_bool)


list_label_by_mail=[]
index = 0
for mail in rjson.list_mail_en:
    list_label=[]
    if (index > 10):
        break
    index +=1
    if index % 10 == 0:
        print(str(index) + "/" + str(len(rjson.list_mail_en)))

    for label in rxml.pref_labels_en:
        if ( search_in(label.lower(), mail['body'].lower()) or search_in(label.lower(), mail['subject'].lower()) ):
            list_label.append(label)
    occurrences = collections.Counter(list_label)
    list_label_by_mail.append((mail, occurrences))

f_pretty = open("../result/pretty/"+"result_pretty_"+str(int(datetime.timestamp(datetime.now())))+".json", "w", encoding="utf-8")
f = open("../result/inline/"+"result_"+str(int(datetime.timestamp(datetime.now())))+".json", "w", encoding="utf-8")

all_json = dict()

for i in range(0, len(list_label_by_mail)):
    part_json = dict()
    part_json["result"] = list_label_by_mail[i][1]
    part_json["mail"] = list_label_by_mail[i][0]
    all_json[i] = part_json


string_pretty = json.dumps(all_json, indent=2, ensure_ascii=False)
f_pretty.write(string_pretty)
f_pretty.close()

string = json.dumps(all_json)
f.write(string)
f.close()

