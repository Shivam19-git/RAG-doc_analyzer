from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid, io, os, shutil
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


app = FastAPI()

#  Get the absolute path of the directory containing this main.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# to ensure that the upload directory exists
os.makedirs(BASE_DIR,exist_ok = True)


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base Model for text messages
class Message(BaseModel):
    text: str

# Define what file formats the RAG system is allowed to process
ALLOWED_TYPES = [
    "text/plain",               # .txt files
    "application/pdf",          # .pdf files
    "text/markdown"             # .md files
]

@app.get('/home')
def home():
    return {"message": "Hello, FastAPI"}

@app.post('/send')
async def received_text(message: Message):
    print("Received : ", message.text)
    return {
        "status": "success",
        "received_text": message.text
    }


@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "message": "File successfully saved to the backend folder", 
            "filename": file.filename,
            "path": file_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
    
    
    
    
    