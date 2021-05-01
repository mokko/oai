"""
Generic parts of the verb for inheritance
"""
from lxml import etree
from pathlib import Path

class verb:
    # class variables
    parser = etree.XMLParser(remove_blank_text=True)
    xsdLoc = Path(__file__).parent.joinpath("oai_dc.xsd")
    NSMAP = {"o": "http://www.openarchives.org/OAI/2.0/"}

    @classmethod  # alternative constructor
    def fromFile(cls, *, path):
        ET = etree.parse(path, verb.parser)
        return cls.fromET(ET=ET)
 
    @classmethod
    def fromXML(cls, *, xml):
        ET = etree.fromstring(xml)
        return cls.fromET(ET=ET)

    def validate(self):
        """
        validate internal object; for now only internal object 
        
        i.validate()
        
        Dies if not valid with error message.
        
        Maybe validate should instead be in data provider?
        """
        ET = self.toET()
        
        if not hasattr(self, "xsd"):
            self.xsd = etree.parse(str(verb.xsdLoc))
        xmlschema = etree.XMLSchema(self.xsd)
        xmlschema.assertValid(ET)  # dies if it doesn't validate
 

    def _subelement(self, *, parent, name):
        """
        returns lxml xml fragment like this:
            <parent><name>text</name></parent> 
        for self.name
        """
        N = etree.SubElement(parent, name).text = getattr(self, name)
        return N

    def _subelementList(self, *, parent, name):
        """
        returns last node;
        self.{name} is empty, no element is added
        """
        N = None
        for item in getattr(self, name):
            N = etree.SubElement(parent, name).text = item
        return N

    def toString(self):
        return etree.tostring(
            self.toET(), pretty_print=True, encoding="unicode"
        )

    def toFile(self, *, path):
        """internal object to xml file"""
        ET = self.toET()
        tree = etree.ElementTree(ET) #UTF-8 not UTF8
        tree.write(path, pretty_print=True, encoding="UTF-8", xml_declaration=True)
