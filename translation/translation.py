from mtranslate import translate
import xml.etree.ElementTree as ET
import sys


def translation(filename, initial_lang, final_lang):
    print(filename)
    tree = ET.parse(filename)

    root = tree.getroot()
    result_filename = final_lang + "-" + filename

    index = 0
    for child in root:
        index +=1
        for child2 in child:
            if child2.tag == "{http://www.w3.org/2004/02/skos/core#}prefLabel":
                if child2.attrib["lang"] == initial_lang:
                    if index % max((len(root) // 20), 1) == 0:
                        print("label: " + initial_lang 
                            + "->" + final_lang + " | " 
                            + str(index) + "/" 
                            + str(len(root)))
                    child2.attrib["lang"] = final_lang
                    child2.text = translate(child2.text, final_lang, initial_lang)

    tree.write(result_filename, encoding="UTF-8", xml_declaration=True)


def main():
    args = sys.argv[1:]
    default_initial_lang = "en"
    default_final_lang = "fr"
    print(args)
    initial_lang = None
    final_lang = None
    try:
        filename = args[0]
    except IndexError:
        print('No filename where given')
        print('Retry with a filename...')
        return

    try:
        initial_lang = args[1]
    except IndexError:
        print('No language where given, keeping default "en" -> "fr"')
        initial_lang = default_initial_lang
    if initial_lang == None:
        print('Language is not good, keeping default "en" -> "fr"')
        initial_lang = default_initial_lang

    try:
        final_lang = args[2]
    except IndexError:
        print('No final language where given, keeping final to: "fr"')
        final_lang = default_final_lang
    if final_lang == None:
        print('Language is not good, keeping final to: "fr"')
        final_lang = default_final_lang

    translation(filename, initial_lang, final_lang)


if __name__ == '__main__':
    main()