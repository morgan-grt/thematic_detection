import sys
import os
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

def write_file(list_label_by_mail, filename):
    f = open(os.getcwd()+'/api/result/'+'result-'+filename, "w", encoding="utf-8")

    all_json = dict()

    for i in range(0, len(list_label_by_mail)):
        part_json = dict()
        part_json["result"] = list_label_by_mail[i][1]
        part_json["mail"] = list_label_by_mail[i][0]
        all_json[i] = part_json

    string = json.dumps(all_json)
    f.write(string)
    f.close()
    return

def work(filename):
    list_cles, list_mail_fr, list_mail_en = rjson.read_file(filename)
    pref_labels_en, pref_labels_fr = rxml.read_skos()

    list_label_by_mail=[]
    index = 0
    for mail in list_mail_en:
        list_label=[]
        # to limit number of emails in the run
        #if (index > 10):
        #    break
        index +=1
        if index % 10 == 0:
            print(str(index) + "/" + str(len(list_mail_en)))
            sys.stdout.flush()

        for label in pref_labels_en:
            if ( search_in(label.lower(), mail['body'].lower()) or search_in(label.lower(), mail['subject'].lower()) ):
                list_label.append(label)
        occurrences = collections.Counter(list_label)
        list_label_by_mail.append((mail, occurrences))

    write_file(list_label_by_mail, filename)
    return

def main():
    filename = None;
    try:
        filename = sys.argv[1]
    except IndexError:
        print('No Argument where given')
        sys.stdout.flush()
        return
    if (filename == None):
        print('File is null')
        sys.stdout.flush()
        return
    if (not '.json' in filename):
        print('File is not a json')
        sys.stdout.flush()
        return
    else:
        print('File is a json, pass')
        sys.stdout.flush()

    work(filename)
    print('Work done, download is available')
    sys.stdout.flush()
    print('canDownload')
    sys.stdout.flush()
    return
main()
