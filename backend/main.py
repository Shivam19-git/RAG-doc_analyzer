from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid, io
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


app = FastAPI()

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

# Extract text from bytes based on file type
async def extract_text(content : bytes, content_type : str)->str:
    if content_type in ["text/plain", "text/markdown"]:
        # .txt and MD files can be coded directly
        return content.decode('utf-8')
    elif content_type == "application/pdf":
        pdf_reader = PdfReader(io.BytesIO(content))
        text = " "
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + '\n'
        return text
    return ""

# Break the text into overlapping chunks
def get_text_chunks(text:str)->list[str]:
    # I use 1000 characters per chunk, with a 200 character overlap 
    # to ensure context isn't lost if a sentence is cut in half.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)

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

# ingestion endpoint for the Document Analyzer
@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    # 1. Validate the file type before doing any work
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file.content_type}. Please upload a txt, pdf, or md file."
        )

    # 2. Read file content directly into memory for fast processing
    content = await file.read()
    
    # 3. Generate a unique ID for this specific document 
    # (Crucial for metadata tagging in the vector database later)
    doc_id = str(uuid.uuid4())
    
    # --- Future Phase 2 placeholder ---
    # This is where we will pass 'content' into the text parsing and semantic chunking logic
    # 1. Turn raw bytes into a giant string of text
    raw_text = await extract_text(content, file.content_type)

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from document. It might be an image-based PDF.")
    #2. Slice the giant string into managable chunks
    chunks = get_text_chunks(raw_text)
    
    # ----------------------------------

    print(f"Ingested: {file.filename} | ID: {doc_id} | Size: {len(content)} bytes")

    # 4. Return the payload to React
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "document_id": doc_id,
        "message": "File successfully ingested into memory."
    }