import sys
sys.path.append ("../src")
from Identify import Identify

def test_init():
    i = Identify(
     baseURL="www.mmm.com/oai", deletedRecord="transient", repositoryName="M3OAI"
    )
    assert i
    assert i.baseURL == "www.mmm.com/oai"
    assert i.deletedRecord == "transient"
    assert i.repositoryName == "M3OAI"

def test_fromFile():
    i = Identify.fromFile(path="identify.xml")
    assert i
    
def test_fromXML():
    i = Identify(
     baseURL="www.mmm.com", deletedRecord="transient", repositoryName="M3OAI"
    )
    xml = i.toString()
    i = Identify.fromXML(xml=xml)
    assert i
    
def test_validate():
    i = Identify(
        baseURL="www.mmm.com", deletedRecord="transient", repositoryName="M3OAI"
    )
    i.adminEmail.append("m3@gmail.com")
    i.toFile(path="identify2.xml")
    print(i.toString())
    i.validate()

def test_validate2():
    i = Identify.fromFile(path="identify.xml")
    i.validate()