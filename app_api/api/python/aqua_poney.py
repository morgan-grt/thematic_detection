import json
import sys
import constants
import os
import json
from datetime import datetime


def aqua_poney(filename):
    f = open(constants.BASE_PATH_RESULT+filename, "r")

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    output_string = "["
    #print('{"insertDB":[')
    #sys.stdout.flush();

    escaped_char = "'"

    for index in data:
        index_string = "{"
        index_string += '"_id":"' + data[index]['mail'][1]['_id']['$oid'].replace('"', escaped_char) + '",'
        index_string += '"body":"' + data[index]['mail'][1]['body'].replace('"', escaped_char) + '",'
        index_string += '"subject":"' + data[index]['mail'][1]['subject'].replace('"', escaped_char) + '",'
        date = datetime.strptime(data[index]['mail'][1]['date'].replace('"', escaped_char), '%a, %d %b %Y %H:%M:%S %z')
        index_string += '"date": "' + str(date.isoformat()) + '",'
        index_string += '"fromName":"' + data[index]['mail'][1]['fromName'].replace('"', escaped_char) + '",'
        index_string += '"fromMail":"' + data[index]['mail'][1]['fromMail'].replace('"', escaped_char) + '",'
        index_string += '"language":"' + data[index]['mail'][1]['language'].replace('"', escaped_char) + '",'
        index_string += '"isCFP":"' + data[index]['mail'][1]['isCFP'] + '",'

        index_string += '"labels":['
        index_label = 0
        for key in data[index]['result']:
            name = data[index]['result'][key]['name']
            count = data[index]['result'][key]['count']
            index_string += '{"name":"' + str(name) + '","count":"' + str(count) + '"}'
            if index_label < len(data[index]['result']) - 1:
                index_string += ','
            index_label += 1
        index_string += ']}'

        if int(index) < len(data) - 1:
                index_string += ','
        output_string += index_string

        #print(index_string)
        #sys.stdout.flush()
    output_string += ']'

    #print('{"insertDB":' + output_string + "}")
    #sys.stdout.flush()

    res_f = open(constants.BASE_PATH_SEARCH+"search-"+filename, "w", encoding="utf-8")
    res_f.write(output_string)
    res_f.close()

    print('canInsert')
    sys.stdout.flush()


def main():
    args = sys.argv[1:]
    filename = None

    try:
        filename = args[0]
    except IndexError:
        print('No filename where given')
        print('Retry with a filename...')
        return
    
    aqua_poney(filename)


if __name__ == '__main__':
    main()