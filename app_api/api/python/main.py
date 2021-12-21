import sys, time, os
import constants
import xml_reader as rxml
import json_reader as rjson
import classifier
import json
import numpy as np
from os.path import basename
from zipfile import ZipFile
from datetime import datetime
from multiprocessing import Process, Manager
from threading import Thread


def create_archive(filename, list_file):
    zip_filename = constants.BASE_PATH_RESULT + 'archive-' + filename + '.zip'
    zip_object = ZipFile(zip_filename, 'w')
    # Add multiple files to the zip
    for file in list_file:
        zip_object.write(file, basename(file))
    # close the Zip File
    zip_object.close()


def write_file(list_label_by_mail, filename_json, user_pretty):
    json_filename = constants.BASE_PATH_RESULT + 'result-' + filename_json
    f = open(json_filename, "w", encoding="utf-8")

    all_json = dict()

    for i in range(0, len(list_label_by_mail)):
        part_json = dict()
        part_json["result"] = dict()
        index = 0
        for k, v in list_label_by_mail[i][1].items():
            part_json["result"][index] = dict()
            part_json["result"][index]["name"] = k
            part_json["result"][index]["count"] = v
            index += 1
        part_json["mail"] = list_label_by_mail[i][0]
        all_json[i] = part_json
        
    if (user_pretty):
        string = json.dumps(all_json, indent=2, ensure_ascii=False)
    else:
        string = json.dumps(all_json)
        
    f.write(string)
    f.close()
    return json_filename


def main():
    sys.stdout.flush()
    arguments = json.loads(sys.argv[1])
    print(arguments)
    sys.stdout.flush()

    '''
    checks if file is valid
    '''
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
        filename_json = filename
        filename = filename.replace('.json', '')
        sys.stdout.flush()


    # get mails and skos labels
    list_cles, list_mail_fr, list_mail_en = rjson.read_file(filename_json)
    pref_labels_en, pref_labels_fr = rxml.read_skos()
    list_label_by_mail = list()

    '''
    checks if user want pretty format file
    '''
    user_pretty = False
    try:
        user_pretty = bool(arguments['user_pretty'] == 'true')
    except KeyError:
        print('Missing user pretty, keeping default value : False')
        sys.stdout.flush()


    '''
    prepare multiprocess
    checks if user has limited number of cpu used
    '''
    user_max_cpu = None
    try:
        user_max_cpu = int(arguments['user_max_cpu'])
        if user_max_cpu < 0:
            user_max_cpu = os.cpu_count()
    except KeyError:
        print('Missing max cpu')
        sys.stdout.flush()
        user_max_cpu = os.cpu_count()

    max_cpu = min(os.cpu_count(), user_max_cpu);

    '''
    resize list_mail if max_size
    checks if user has limited max email analysed
    '''
    user_max_size = None
    try:
        user_max_size = int(arguments['user_max_size'])
        if user_max_size < 0:
            user_max_size = len(list_mail_en)
    except KeyError:
        print('Missing max size')
        sys.stdout.flush()
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
            target=classifier.search, 
            args=(i, list_mail_for_process[i], pref_labels_en, list_label_by_mail))
        processes.append(process)

    # Start the processes     
    for p in processes:
        p.start()

    # Ensure all of the processes have finished
    for p in processes:
        p.join()

    json_filename = write_file(list_label_by_mail, filename_json, user_pretty)

    tend = time.time() - tbegin
    
    print('Work done, download is available')
    sys.stdout.flush()
    print('DURATION : ' + str(round(tend, 4)) + ' seconds')
    sys.stdout.flush()
    print('canDownload')
    sys.stdout.flush()
    return


main()
