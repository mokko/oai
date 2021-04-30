"""
OAI Data Provider
"""
from starlette.responses import Response
from starlette.responses import JSONResponse

allowed_verbs = { #inspired by Brady's HTTP::OAI
    "GetRecord": {
            "identifier": "Required",
            "metadataPrefix": "Required",
    },
    "Identify" : {},
    "ListIdentifiers" : {
            "from" : "Optional",
            "until" : "Optional",
            "set" : "Optional",
            "metadataPrefix" : "Required",
            "resumptionToken" : "Exclusive",
    },
    "ListMetadataFormats" : {
            "identifier" : "Optional"
    },
    "ListRecords" : {
            "from" : "Optional",
            "until" : "Optional",
            "set" : "Optional",
            "metadataPrefix" : "Required",
            "resumptionToken" : "Exclusive",
    },
    "ListSets" : {
            "resumptionToken" : "Exclusive"
    }
}

class Provider:
    def __init__ (self): 
        print("GH")
    
    def validate_request(self, query):
        """
        Simple type-agnostic query param validation.
        
        Expects a query. Performs a series of tests.
        
        Returns OAI Error accordingly or nothing on successful validation.
        
        """
        if "verb" not in query:
            return JSONResponse({"Bad Verb":"No verb specified"})
        elif query["verb"] not in allowed_verbs: 
            return JSONResponse({"Bad Verb":"Illegal verb specified"})
        else:
            if "resumptionToken" in query and len(query) > 2:
                return JSONResponse({"Bad resumptionToken":"resumptionToken with too many other params"})
            verb = query["verb"]
            allowed_params = allowed_verbs[verb]
            for param in query:
                if param == "verb": pass
                elif param not in allowed_params:
                    return JSONResponse({"BadArgument":"illegal parameter"})
            for param in allowed_params:
                if allowed_params[param] == "Required":
                    if not param in query:
                        return JSONResponse({"BadArgument":"required parameter missing"})
            print(f"*query validates: {query}")
        #return None: is sign of success

    def getRecord(self, request): pass
    def identify(self,request):
        Identify()
        response = Response('<xml>toot</xml>', media_type='application/xml')
        print ("GGGGG")
        return response
        #await response(scope, receive, send)
    def listIdentifiers(self,request): pass
    def listMetadataFormats(self,request): pass
    def listRecords(self,request): pass
    def listSets(self,request): pass
