import xml.etree.ElementTree as ET





tree = ET.parse('assets\error_nmr_measurement.xml')
tree_end = ET.parse('assets\\xml_test_end.xml')
root = tree.getroot()
root_end = tree_end.getroot()

'''
# intermediate response

for i in root:
    #print(i.tag)
    #print(i.attrib)
    progress = i.iter('Progress')
    #print(progress)
    for j in progress:
        pass
        #print("response", j.attrib)
    #print("hallo")

# final response

for k in root_end:
    print(k.tag, k.attrib)

'''

for i in root:
    print(i.tag)
    error = i.iter("Error")
    print(error)
    for j in i:
        print("das ergebnis ist",j.tag)
        if j.tag == "Error":
            print("NEEEEEEEIIIIIIN")
        if j.tag != "Error":
            print("Es lebt")