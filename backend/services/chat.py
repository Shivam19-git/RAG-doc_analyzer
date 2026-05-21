from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


# OpenAI Client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
     base_url="https://api.groq.com/openai/v1"
)


# Request Model
class ChatRequest(BaseModel):
    prompt: str


async def chat_bot(prompt : str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )



    return response.choices[0].message.content