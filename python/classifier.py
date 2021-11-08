import xml_reader as rxml
import json_reader as rjson



list_label_by_mail=[]
for mail in rjson.list_mail_en:
    list_label=[]
    for label in rxml.pref_labels_en:
        if ( label in mail['body'] ):
            list_label.append(label)
    list_label_by_mail.append(list_label)

print(list_label_by_mail)


