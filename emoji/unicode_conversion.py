import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
import xml.etree.ElementTree as ET
tree = ET.parse(os.path.join(__location__,'emoji4unicode.xml'))
root = tree.getroot()

unicode_dict = {}
lower_unicodes = set()

for category in root:
    for sub in category:
        for e in sub:
            softbank_ref = e.get('softbank')
            if softbank_ref is not None:
                softbank_ref = softbank_ref.lower()
            unicode_ref = e.get('unicode')
            if unicode_ref is not None:
                unicode_ref = unicode_ref.lower().replace('+','')  
                lower_unicodes.add(unicode_ref)
                unicode_dict[softbank_ref] = unicode_ref

print lower_unicodes 

def convert_unicode(string):
    if string.startswith("\U000"):
        #print string
        return string[5:]
    if string.startswith("\u"):        
        substring = string[2:].lower()
        if substring in lower_unicodes:
            return substring.lower()
        return unicode_dict[substring].lower()
    else: raise KeyError