from dicttoxml import dicttoxml
from xml.etree import ElementTree as ET


class SpinsolveXmlBuilder:

    def __init__(self, protocol:str, values:dict):
        self.protocol:str = protocol
        self.values:dict = values

    def build_measurement(self):
    

        a = ET.Element('Message')
        b = ET.SubElement(a, 'Start')
        b.set("protocol", "1D PROTON")
        c = ET.SubElement(b, 'Option')
        xml = ET.dump(a)

        return xml



new = SpinsolveXmlBuilder("reaction", {"empty":"hallo"})
new.build_measurement()
        