import xml.etree.ElementTree as ET
import os 


def read_skos():

    tree = ET.parse(os.getcwd()+'/api/xml/skos.xml')

    label = ET.Element('prefLabel')
    root = tree.getroot()

    pref_labels_fr = []
    pref_labels_en = []

    for child in root:      
       for child2 in child:
           if(child2.tag =="{http://www.w3.org/2004/02/skos/core#}prefLabel"):
               if(child2.attrib["lang"] == "en"):
                   pref_labels_en.append(child2.text)
               else:
                    pref_labels_fr.append(child2.text)

    return pref_labels_en, pref_labels_fr
   
