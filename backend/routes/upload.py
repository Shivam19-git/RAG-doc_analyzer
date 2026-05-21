from fastapi import UploadFile, File, HTTPException
from utils.chunking import split_text_in_chunks
from pypdf import PdfReader

import os
import shutil


async def upload_file(file: UploadFile = File(...)):

    # backend/
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

    # backend/uploads/
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

    # Create uploads folder
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    try:

        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDFs are allowed"
            )

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        # Save PDF
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read PDF
        reader = PdfReader(file_path)

        raw_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                raw_text += text + "\n"

        # Chunk text
        chunks = split_text_in_chunks(raw_text)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "path": file_path,
            "chunks": len(chunks)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not save file: {str(e)}"
        )