import sys
import collections

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


def search(id, list_mail, pref_labels_en, list_label_by_mail):
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