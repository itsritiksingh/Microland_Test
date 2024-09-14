import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.utils.langchain import generate_response
from src.utils.ocr import convert_pdf_to_images

app = FastAPI()


class QueryModel(BaseModel):
    query: str


@app.post("/upload/")
async def upload_file(file: UploadFile = File()):

    contents = await file.read()
    path = convert_pdf_to_images(contents)

    return JSONResponse(content={"message": "Context Uploaded Successfully", "context": path})


@app.post("/ask")
async def ask_question(body: QueryModel = None):
    query = body.query

    ai_response = generate_response(query)
    if ai_response:
        return JSONResponse(content={"answer": ai_response})
    else:
        return JSONResponse(content={"answer": "I couldn't find a relevant answer in the document."})
