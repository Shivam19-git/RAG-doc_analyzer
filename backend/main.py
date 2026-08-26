from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from routes.upload import router as upload_router
from services.chat import chat_bot
from routes.upload import upload_file
import os


load_dotenv()

app = FastAPI(title="RAG-Doc Analyzer API")

# Configure CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)

@app.get("/")
def root():
    return {"status": "online", "message": "RAG-Doc Analyzer API"}

# Upload Route
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    result = await upload_file(file)

    return result


class ChatRequest(BaseModel):
    prompt: str

# Chat Route
@app.post("/chat")
async def chat(req: ChatRequest):

    ai_reply = await chat_bot(req.prompt)
    return {
        "response": ai_reply
    }