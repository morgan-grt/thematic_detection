import sys, time, os
import constants
import xml_reader as rxml
import json_reader as rjson
import json
import numpy as np
import collections
from datetime import datetime
from multiprocessing import Process, Manager
from threading import Thread


def write_file(list_label_by_mail, filename):
    f = open(os.getcwd()+constants.BASE_PATH_RESULT
        +'result-'
        #+str(int(datetime.timestamp(datetime.now())))
        +filename, "w", encoding="utf-8")

    all_json = dict()

    for i in range(0, len(list_label_by_mail)):
        part_json = dict()
        part_json["result"] = list_label_by_mail[i][1]
        part_json["mail"] = list_label_by_mail[i][0]
        all_json[i] = part_json

    # string = json.dumps(all_json)
    string = json.dumps(all_json, indent=2, ensure_ascii=False)
    f.write(string)
    f.close()
    return


def search_in_naif(label, item):
    item_split = item.split()
    label_split = label.split()

    label_bool = [False for lab in label_split] 

    for j in range(0, len(item_split) - len(label_split)):
        if label_split[0] == item_split[j]:
            label_bool[0] = True
            for k in range(1, len(label_split)):
                if label_split[k] == item_split[j+k]:
                    label_bool[k] = True
                else:
                    break

    return all(label_bool)


def search_in(label, item):
    punctuation = ',.?!'
    return label in [words.strip(punctuation) for words in item.split()]


def work(id, list_mail, pref_labels_en, list_label_by_mail):
    index = 0
    for mail in list_mail:
        list_label=[]

        index +=1
        if index % max((len(list_mail) // 5), 1) == 0:
            print(str(index) + "/" + str(len(list_mail)))
            sys.stdout.flush()

        for label in pref_labels_en:
            if ( search_in_naif(label.lower(), mail['body'].lower()) 
              or search_in_naif(label.lower(), mail['subject'].lower()) ):
                list_label.append(label)
        occurrences = collections.Counter(list_label)
        list_label_by_mail.append((mail, occurrences))


def main():
    print(sys.argv)
    sys.stdout.flush()
    arguments = json.loads(sys.argv[1])
    print(arguments)
    sys.stdout.flush()
    filename = None;
    try:
        filename = arguments['filename']
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


    # get mails and skos labels
    list_cles, list_mail_fr, list_mail_en = rjson.read_file(filename)
    pref_labels_en, pref_labels_fr = rxml.read_skos()
    list_label_by_mail = list()

    # prepare multiprocess
    user_max_cpu = None
    try:
        user_max_cpu = int(arguments['user_max_cpu'])
    except KeyError:
        print('Missing max cpu')
        user_max_cpu = os.cpu_count()

    max_cpu = min(os.cpu_count(), user_max_cpu);


    # resize list_mail if max_size
    user_max_size = None#
    try:
        user_max_size = int(arguments['user_max_size'])
    except KeyError:
        print('Missing max size')
        user_max_size = len(list_mail_en)

    max_size = min(len(list_mail_en), user_max_size)
    list_mail_en = list_mail_en[:max_size]

    # separate mails equal part for multiprocess
    list_mail_for_process = np.array_split(list_mail_en, max_cpu)

    list_label_by_mail = Manager().list()
    processes = []

    tbegin = time.time()

    for i in range(0, max_cpu):
        process = Process(
            target=work, 
            args=(i, list_mail_for_process[i], pref_labels_en, list_label_by_mail))
        processes.append(process)

    # Start the processes     
    for p in processes:
        p.start()

    # Ensure all of the processes have finished
    for p in processes:
        p.join()

    print(len(list_label_by_mail))
    write_file(list_label_by_mail, filename)


    tend = time.time() - tbegin
    
    print('Work done, download is available')
    sys.stdout.flush()
    print('DURATION : ' + str(round(tend, 4)) + ' seconds')
    sys.stdout.flush()
    print('canDownload')
    sys.stdout.flush()
    return


main()
