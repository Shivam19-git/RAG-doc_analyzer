from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from services.chat import chat_bot
from routes.upload import upload_file
import os


load_dotenv()

app = FastAPI()

# CORS
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

@app.get("/home")
def home():
    return {
        "message": "Hello FastAPI"
    }


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