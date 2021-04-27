"""
    #must contain exactly one
    baseURL # example in spec shows multiple baseURLs; are they really allowed?
    repositoryName
    protocolVersion
    earliestDatestamp
    deletedRecord
    granuality
    
    #one or more
    adminEmail
    
    #optional
    compression (multiple)
    description (multiple)

USAGE
    i = Identify.fromET(ET=lxml_object)    # alt constructor
    i = Identify.fromFile(path="file.xml") # alt constructor
    i = Identify.fromXml(xml=xml)          # alt constructor
    i = Identify (
        baseURL="http://memory.loc.gov/cgi-bin/oai",
        repositoryName="This Is A Name",
        protocolVersion="2.0",     # should default to 2.0
        earliestDatestamp="",   # might be set automatically later
        deletedRecord="",       # 
        granuality="",
    )
    # let's not allow setters for normal required unique elements
    # let's set them once and for all during construction
    bU = i.baseURL()           # getter, no setter
    rN = i.repositoryName()    # getter, no setter
    eD = i.earliestDatestamp() # getter, no setter
    dR = i.deletedRecord()     # getter, no setter
    g = i.granuality()         # getter, no setter

    # attributes that allow multiplicity:
    # adminEmail, compression and description
    
    d = i.description()         # gets all description elements as list as per lxml
    i.description("<bl>b</bl>") # setter, adds another description after existing descriptions
    for d in i.description:
        #do something with d

    #helpers
    xml = i.toXml() # returns xml representation
    i.validate() # creates xml representation internally and validates that
    
    we have two main options: 
    (1) take apart the xml into basic units, save it python style and assemble it back together
        as xml when needed.
    (2) save xml internally and process and return it as requested
        
    (1) might be safer and save resources; the latter is really unclear
    
    What happens if I use same principle on getRecords with big documents? They have to be in
    memory completely? Perhaps we can use sax or similar technology.
    
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

class Identify():
    def __init__(self, *, 
        baseURL,
        deletedRecord="transient",
        granuality="YYYY-MM-DDThh:mm:ssZ",
        protocolVersion="2.0",
        repositoryName): 

        self.baseURL = baseURL
        self.deletedRecord = deletedRecord
        self.earliestDatestamp = "1900-01-01T12:00:00Z"
        self.granuality = granuality
        self.protocolVersion = protocolVersion
        self.repositoryName = repositoryName
        self._adminEmail = []
        self._description = []
        self._compression = []
    
    #
    # constructors
    #
    @classmethod # as alternative constructor
    def fromFile(self, *, path):
        print("alt constructor later")
        return self
    
    @classmethod 
    def fromET(self, *, ET):
        print("alt constructor later")
        return self
    
    @classmethod 
    def fromXml(self, *, xml):
        print("alt constructor later")
        return self

    #
    # properties
    #

    #getter, setter, no multiplicity
    @property
    def earliestDatestamp(self):
        return self._earliestDatestamp

    #need a setter since this date is unknown at the time of construction
    @earliestDatestamp.setter
    def earliestDatestamp(self, eD):
        self._earliestDatestamp = eD
        return self._earliestDatestamp

    @property
    def responseDate(self):
        return self._responseDate

    @responseDate.setter
    def responseDate(self, rDate):
        self._responseDate = rDate
        return self._responseDate

    #getters, setters with multiplicity
    @property
    def adminEmail(self):
        return self._adminEmail
    
    @property
    def compression(self):
        return self._compression
    
    @property
    def description(self):
        return self._description

    #
    # helpers 
    #
    def toET(self):
        NSMAP = {"o" : "http://www.openarchives.org/OAI/2.0/"}
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
        self._subelement(parent=ET, name="responseDate")  # required

        # very temporary solution, needs overhaul
        # represents the URL request
        requestN = etree.SubElement(ET, "request", verb="Identify")
        requestN.text = "URL"

        identifyN = etree.SubElement(ET, "Identify")

        self._subelement(parent=identifyN, name="repositoryName")  # required
        self._subelement(parent=identifyN, name="baseURL")         # required
        self._subelement(parent=identifyN, name="protocolVersion") # required
        self._subelementList(parent=identifyN, name="adminEmail")  # required
        self._subelement(parent=identifyN, name="earliestDatestamp") # required
        self._subelement(parent=identifyN, name="deletedRecord")   # required
        self._subelement(parent=identifyN, name="granuality")      # required
        self._subelementList(parent=identifyN, name="compression") # optional
        self._subelementList(parent=identifyN, name="description") # optional
        return ET

    def _subelement(self, *, parent, name):
        N = etree.SubElement(parent, name).text = getattr(self, name)
        return N

    def _subelementList(self, *, parent, name):
        """
        returns last node;
        self.{name} is empty, no element is added
        """
        for item in getattr(self, name):
            N = etree.SubElement(parent, name).text = item
        return N
     
    def toString(self):
        return etree.tostring(i.toET(), pretty_print = True, xml_declaration = True, encoding='UTF-8') #standalone=True

    
if __name__ == "__main__":
    i = Identify(baseURL="www.mmm.com", deletedRecord="transient", repositoryName="M3OAI")
    print(i)
    print(i.baseURL)
    i.adminEmail.append("so") 
    i.adminEmail.append("bla@email.com") 
    for each in i.adminEmail:
        print(each)
    
    #print (i.toET())
    print (i.toString())