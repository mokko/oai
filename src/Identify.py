"""
USAGE
    # CONSTRUCTORS
    i = Identify (
        baseURL="http://memory.loc.gov/cgi-bin/oai",
        repositoryName="This Is A Name",
        protocolVersion="2.0",     
        deletedRecord="transient",        
        granuality="",
    )
    i = Identify.fromET(ET=lxml_object)    # alt constructor
    i = Identify.fromFile(path="file.xml") # alt constructor
    i = Identify.fromXML(xml=xml)          # alt constructor

    # no setters for normal required unique elements; only set during construction
    bU = i.baseURL
    rN = i.repositoryName
    dR = i.deletedRecord
    g = i.granuality

    #getter & setter
    eD = i.earliestDatestamp
    i.earliestDatestamp = datestamp
    i.request = request # not sure yet how setter will look like
    
    # attributes that allow multiplicity: 
    # adminEmail, compression and description
    
    d = i.description()         # gets all description elements as list as per lxml
    i.description.append("<bl>b</bl>") # adds another description after existing descriptions
    for desc in i.description:
        #do something with desc

    #helpers
    ET = i.toET() # returns internal object as etree
    xml = i.toString() # returns internal object as xml 
    i.validate() # creates xml representation internally and validates that
    
    we have two main options: 
    (1) take apart the xml into basic units, save it python style and assemble it back together
        as xml when needed.
    (2) save xml internally and process and return it as requested
        
    (1) might be safer and save resources; the latter is really unclear
    
    What happens if I use same principle on getRecords with big documents? They have to be in
    memory completely? Perhaps we can use sax or similar technology.
    
    #must contain exactly one
    baseURL # example in spec shows multiple baseURLs; are they really allowed?
    repositoryName
    protocolVersion
    deletedRecord
    granuality

    #one with setter
    earliestDatestamp
    
    #one or more
    adminEmail
    
    #optional
    compression (multiple)
    description (multiple)
<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
  <responseDate>2002-02-08T12:00:01Z</responseDate>
  <request verb="Identify">http://memory.loc.gov/cgi-bin/oai</request>
  <Identify>
    <repositoryName>Library of Congress Open Archive Initiative 
                    Repository 1</repositoryName>
    <baseURL>http://memory.loc.gov/cgi-bin/oai</baseURL>
    <protocolVersion>2.0</protocolVersion>
    <adminEmail>somebody@loc.gov</adminEmail>
    <adminEmail>anybody@loc.gov</adminEmail>
    <earliestDatestamp>1990-02-01T12:00:00Z</earliestDatestamp>
    <deletedRecord>transient</deletedRecord>
    <granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
    <compression>deflate</compression>
    <description>
      <oai-identifier 
        xmlns="http://www.openarchives.org/OAI/2.0/oai-identifier"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation=
            "http://www.openarchives.org/OAI/2.0/oai-identifier
        http://www.openarchives.org/OAI/2.0/oai-identifier.xsd">
        <scheme>oai</scheme>
        <repositoryIdentifier>lcoa1.loc.gov</repositoryIdentifier>
        <delimiter>:</delimiter>
        <sampleIdentifier>oai:lcoa1.loc.gov:loc.music/musdi.002</sampleIdentifier>
      </oai-identifier>
    </description>
    <description>
      <eprints 
         xmlns="http://www.openarchives.org/OAI/1.1/eprints"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/1.1/eprints 
         http://www.openarchives.org/OAI/1.1/eprints.xsd">
        <content>
          <URL>http://memory.loc.gov/ammem/oamh/lcoa1_content.html</URL>
          <text>Selected collections from American Memory at the Library 
                of Congress</text>
        </content>
        <metadataPolicy/>
        <dataPolicy/>
      </eprints>
    </description>
    <description>
      <friends 
          xmlns="http://www.openarchives.org/OAI/2.0/friends/" 
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/friends/
         http://www.openarchives.org/OAI/2.0/friends.xsd">
       <baseURL>http://oai.east.org/foo/</baseURL>
       <baseURL>http://oai.hq.org/bar/</baseURL>
       <baseURL>http://oai.south.org/repo.cgi</baseURL>
     </friends>
   </description>
 </Identify>
</OAI-PMH>
"""
from lxml import etree
from pathlib import Path

NSMAP = {"o": "http://www.openarchives.org/OAI/2.0/"}
xsdLoc = Path(__file__).parent.joinpath("oai_dc.xsd")


class Identify:
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
    @classmethod  # alternative constructor
    def fromFile(cls, *, path):
        ET = etree.parse(path)
        return cls.fromET(ET=ET)
        
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

    @classmethod
    def fromXML(cls, *, xml):
        ET = etree.fromstring(xml)
        return cls.fromET(ET=ET)

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

        parser = etree.XMLParser(remove_blank_text=True)
        xml = """
        <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" 
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
        </OAI-PMH>"""
        ET = etree.fromstring(xml, parser)
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

    #
    # so far this is specific to Identify
    #

    def _xpath (self, ET, name):
        """ 
            Just making a method b/c code is so ugly.
        """
        return ET.xpath(
            f"/o:OAI-PMH/o:Identify/o:{name}/text()", namespaces=NSMAP
        )[0]

    #
    # FOR INHERITANCE
    #

    def validate(self, *, fromET=None, fromXML=None):
        """
        validate internal object 
        
        i.validate()
        i.validate(fromET=ET)
        i.validate(fromXML=xml)
        
        Dies if not valid with error message.
        """
        ET = None
        if fromXML is not None:
            ET = self.toET(xml=fromXML)
        if fromET is not None:
            ET = fromET
            
        ET = self.toET()
        
        if not hasattr(self, "xsd"):
            self.xsd = etree.parse(str(xsdLoc))
        xmlschema = etree.XMLSchema(self.xsd)
        xmlschema.assertValid(ET)  # dies is doesn't validate
 

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
            self.toET(), pretty_print=True, xml_declaration=True, encoding="UTF-8"
        )  # standalone=True


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
