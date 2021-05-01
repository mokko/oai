"""
USAGE
    For all verbs
    (1) alt constructors
    i = Identify.fromET(ET=lxml_object)    
    i = Identify.fromFile(path="file.xml") 
    i = Identify.fromXML(xml=xml)          

    (2) helpers
    ET = i.toET() # returns internal object as etree
    xml = i.toString() # returns internal object as xml 
    i.validate() # creates xml representation internally and validates that

    Specific to Identify
    i = Identify (
        baseURL="http://memory.loc.gov/cgi-bin/oai",
        repositoryName="This Is A Name",
        protocolVersion="2.0",     
        deletedRecord="transient",        
        granuality="",
    )

    Required unique properties; only set during construction
    bU = i.baseURL
    rN = i.repositoryName
    dR = i.deletedRecord
     g = i.granuality

    Getters & setters
    eD = i.earliestDatestamp
    i.earliestDatestamp = datestamp
    i.request = request # not sure yet how setter will look like
    
    Properties with multiplicity: 
    - adminEmail (required), 
    - compression (optional) and 
    - description (optional)
    
    d = i.description() # gets all description elements as list as per lxml
    i.description.append("<bl>b</bl>") # adds another description after existing descriptions
    for desc in i.description:
        #do something with desc

"""
from lxml import etree
from pathlib import Path
from verb import verb

class Identify (verb):
    def __init__(
        self,
        *,
        baseURL,
        deletedRecord="transient",
        granularity="YYYY-MM-DDThh:mm:ssZ",
        protocolVersion="2.0",
        repositoryName
    ):

        self.baseURL = baseURL
        self.deletedRecord = deletedRecord
        self.earliestDatestamp = "1900-01-01T12:00:00Z"
        self.granularity = granularity
        self.protocolVersion = protocolVersion
        self.repositoryName = repositoryName
        self.adminEmail = []
        self.description = []
        self.compression = []

    #
    # alt constructors
    #
        
    @classmethod
    def fromET(cls, *, ET):
        """expects an etree, returns Identify object"""
        baseURL = cls._xpath(cls, ET, "baseURL")
        repositoryName = cls._xpath(cls, ET, "repositoryName")
        protocolVersion = cls._xpath(cls, ET, "protocolVersion")
        deletedRecord = cls._xpath(cls, ET, "deletedRecord")
        granularity = cls._xpath(cls, ET, "granularity")
        
        self = cls(
            baseURL=baseURL,
            repositoryName=repositoryName,
            protocolVersion=protocolVersion,
            deletedRecord=deletedRecord,
            granularity=granularity,
        )

        self.earliestDatestamp = "1900-01-01T12:00:00Z"
        return self
    #
    # Properties
    # In Python 3.x I dont need @property and @xy.setter anymore. Yay!

    # getter, setter, no multiplicity
    # need a setter since the date can be unknown at the time of construction
    def earliestDatestamp(self, eD):
        self.earliestDatestamp = eD
        return eD

    def responseDate(self, rDate):
        self.responseDate = rDate
        return self.responseDate

    #
    # helpers
    #
    def toET(self):
        """Returns internal object as lxml etree object"""

        xml = """
        <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" 
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
        </OAI-PMH>"""
        ET = etree.fromstring(xml, verb.parser)
        # should we fill in current date?
        self.responseDate = "2002-02-08T12:00:01Z"
        self._subelement(parent=ET, name="responseDate")

        # very temporary solution, needs overhaul
        # represents the URL request
        requestN = etree.SubElement(ET, "request", verb="Identify")
        requestN.text = "URL" #todo

        identifyN = etree.SubElement(ET, "Identify")

        # required
        self._subelement(parent=identifyN, name="repositoryName")  
        self._subelement(parent=identifyN, name="baseURL")  
        self._subelement(parent=identifyN, name="protocolVersion")  
        self._subelementList(parent=identifyN, name="adminEmail")  
        self._subelement(parent=identifyN, name="earliestDatestamp")  
        self._subelement(parent=identifyN, name="deletedRecord")  
        self._subelement(parent=identifyN, name="granularity")  
        # optional
        self._subelementList(parent=identifyN, name="compression")  
        self._subelementList(parent=identifyN, name="description")  
        return ET

    def _xpath (self, ET, name):
        """ 
            Just making a method b/c code is so ugly.
            So far _xpath is specific to Identify
        """
        return ET.xpath(
            f"/o:OAI-PMH/o:Identify/o:{name}/text()", namespaces=verb.NSMAP
        )[0]

 
if __name__ == "__main__":
    i = Identify(
        baseURL="www.mmm.com", deletedRecord="transient", repositoryName="M3OAI"
    )
    print(i)
    print(i.baseURL)
    i.adminEmail.append("so@gmx.de")
    i.adminEmail.append("bla@email.com")
    print(i.earliestDatestamp)
    i.earliestDatestamp="2000-01-01T12:00:00Z"
    print (i.toString())
    for each in i.adminEmail:
        print(each)
    ET = i.toET()
    print (ET)
    print (i.toString())
    #i.fromFile(path="identify.xml")
    #print(i.toString())
