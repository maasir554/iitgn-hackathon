from fastapi import FastAPI, Request, HTTPException
import json
from solution import pushTablesInSequence, pdfFromLink, localPush

from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Go to /static to see the files"}



# POST endpoint to handle raw JSON
@app.post("/extract-and-push")

async def process_json(request: Request):
    # Read the raw JSON body
    raw_body = await request.body()

    data = json.loads(raw_body)
    
    """
        format of body: {
            pdfLink: string,
            startFrom: number,
            endBefore: number,
        }
    """
    
    print(data)
    
    try:
        
        if 'pdfLink' not in data:
          Exception("please provide ")  

        pdf_bin = pdfFromLink(data['pdfLink']);
        

        if 'startFrom' not in data:
            data['startFrom'] = 0
        
        if 'endBefore' not in data:
            data['endBefore'] = -1

        update = await pushTablesInSequence(pdf_bin, int(data['startFrom']), int(data['endBefore']), data['pdfLink'])

        return {
            "message": "All pages pushed successfully to database.",
            "data": data,
            "update": update
        }
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

#for local pdf

@app.post("/extract-local")
async def process_json(request: Request):
    # Read the raw JSON body
    raw_body = await request.body()

    data = json.loads(raw_body)
    
    """
        format of body: {
            pdfName: string,
            startFrom: number,
            endBefore: number,
        }
    """
    
    print(data)
    
    try:
        
        if 'pdfName' not in data:
          Exception("please provide ")  

        # pdf_bin = pdfFromLink(data['pdfLink']);
        

        if 'startFrom' not in data:
            data['startFrom'] = 0
        
        if 'endBefore' not in data:
            data['endBefore'] = -1

        update = await localPush(data['pdfName'], int(data['startFrom']), int(data['endBefore']), "doc1")

        return {
            "message": "All pages pushed successfully to database.",
            "data": data,
            "update": update
        }
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

