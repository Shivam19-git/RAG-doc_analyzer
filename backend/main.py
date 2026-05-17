from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allowed origin
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

#Base Model
class Message(BaseModel):
    text : str


@app.get('/home')
def home():
    return {"message" : "Hello, FastAPI"}

@app.post('/send')
async def received_text(message:Message):
    print("Received : ", message.text)

    return{
        "status" : "success",
        "received_text" : message.text
    }

@app.post('/upload')
async def upload_file(file : UploadFile = File(...)):
    #Read file content
    content = await file.read()
    
    print("Filename : ", file.filename)
    print("Content-type : ", file.content_type)
    print("File size : ", len(content))

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content)
    }
