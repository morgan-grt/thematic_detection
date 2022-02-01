import xml.etree.ElementTree as ET
import constants


def read_skos(filename, lang):

    tree = ET.parse(constants.BASE_PATH_XML+filename)

    root = tree.getroot()

    pref_labels = []

    for child in root:      
       for child2 in child:
           if(child2.tag =="{http://www.w3.org/2004/02/skos/core#}prefLabel"):
               if child2.attrib["lang"] == lang:
                   pref_labels.append((lang, child2.text))

    return pref_labels
   

def get_labels():
    pref_labels_en = read_skos("en-skos.xml", "en")
    pref_labels_fr = read_skos("fr-skos.xml", "fr")

    return pref_labels_en + pref_labels_fr