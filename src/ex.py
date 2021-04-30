from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from Provider import Provider

templates = Jinja2Templates(directory="templates") # not srtictly necessary
app = Starlette(debug=True)
app.mount("/static", StaticFiles(directory="statics"), name="static")
p = Provider()

@app.route("/")
async def homepage(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)

@app.route("/oai")
async def oai(request):
    q = request.query_params
    print("GH")
    if (err := p.validate_request(q)):
        return err
    if q['verb'] == "GetRecord": 
        r = p.getRecord(request)
    elif q['verb'] == "Identify":
        r = p.identify(request)
    elif q['verb'] == "ListIdentifiers":
        r = p.listIdentifiers(request)
    elif q['verb'] == "ListMetadataFormats":
        r = p.listMetadataFormats(request)        
    elif q['verb'] == "ListRecords":
        r = p.listRecords(request)        
    elif q['verb'] == "ListSets":
        r = p.listSets(request)        
    else:
        return OAIError ("badVerb")
    return r # 


@app.route("/error")
async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)

#better start from commandlin: with uvicorn app:ex
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, debug=True)
