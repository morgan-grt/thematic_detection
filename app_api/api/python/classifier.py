import math
import re
import sys

import numpy as np


def distLevenshtein(chaine1, chaine2):
    taille_chaine1 = len(chaine1) + 1
    taille_chaine2 = len(chaine2) + 1
    levenshtein_matrix = np.zeros((taille_chaine1, taille_chaine2))
    for x in range(taille_chaine1):
        levenshtein_matrix[x, 0] = x
    for y in range(taille_chaine2):
        levenshtein_matrix[0, y] = y

    for x in range(1, taille_chaine1):
        for y in range(1, taille_chaine2):
            if chaine1[x - 1] == chaine2[y - 1]:
                levenshtein_matrix[x, y] = min(
                    levenshtein_matrix[x - 1, y] + 1,
                    levenshtein_matrix[x - 1, y - 1],
                    levenshtein_matrix[x, y - 1] + 1
                )
            else:
                levenshtein_matrix[x, y] = min(
                    levenshtein_matrix[x - 1, y] + 1,
                    levenshtein_matrix[x - 1, y - 1] + 1,
                    levenshtein_matrix[x, y - 1] + 1
                )
    return (levenshtein_matrix[taille_chaine1 - 1, taille_chaine2 - 1])


def search_by_regex(label, item):

    match = re.findall(r"\b("+label+r")\b", item)

    if match:
        return True
    return False


def search_in_naif(label, item):
    threshold = 5
    item_split = item.split()
    label_split = label.split()

    label_bool = [False for lab in label_split]

    for j in range(0, len(item_split) - len(label_split)):
        if distLevenshtein(label_split[0], item_split[j]) <= math.floor(len(item_split[j]) / threshold):
            label_bool[0] = True
            for k in range(1, len(label_split)):
                if distLevenshtein(label_split[k], item_split[j + k]) <= math.floor(len(item_split[j + k]) / threshold):
                    label_bool[k] = True
                else:
                    break

    return all(label_bool)


def search_in(label, item):
    punctuation = ',.?!'
    return label in [words.strip(punctuation) for words in item.split()]


def search(id, list_mail, pref_labels, labels):
    index = 0
    for lang_mail, mail in list_mail:
        if id == 0:  # and index % 5 == 0:
            print("id:" + str(id) + " - mail | " + str(index + 1) + "/" + str(len(list_mail)))
            sys.stdout.flush()

        index_bis = 0
        for lang_label, label in pref_labels:
            index_bis += 1
            #if index_bis % max((len(pref_labels) // 1), 1) == 0:
            #    print("id:" + str(id) + " - label | " + str(index_bis) + "/" + str(len(pref_labels)))
            #    sys.stdout.flush()
            if lang_mail == lang_label and (search_by_regex(label.lower(), mail['body'].lower())
                                            or search_by_regex(label.lower(), mail['subject'].lower())):
                labels.append((index, label))
        index += 1
