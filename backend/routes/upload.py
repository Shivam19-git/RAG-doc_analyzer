from fastapi import APIRouter, UploadFile, File
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings  

router = APIRouter()

# Folder to save uploads and index
UPLOAD_DIR = "uploads"
INDEX_DIR = "faiss_index"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Using a lightweight local embedding model
embeddings = FakeEmbeddings(size=384) 

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # 1. Save uploaded file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 2. Extract text from PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # 3. Chunk the document
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    
    # 4. Create FAISS vector store and save locally
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(INDEX_DIR)
    
    return {"message": "File processed and indexed successfully", "filename": file.filename}