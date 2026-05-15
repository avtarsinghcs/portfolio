from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

import shutil
import os

from rag_pipeline import (
    ingest_pdf,
    query_rag
)


app = FastAPI()

UPLOAD_DIR = "uploaded_pdfs"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@app.get("/")
def home():

    return {
        "message": "RAGBOT API RUNNING"
    }


@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = ingest_pdf(
        pdf_path=file_path,
        source_id=file.filename
    )

    return result


@app.post("/ask")
async def ask_question(
    question: str
):

    result = query_rag(
        question
    )

    return result
