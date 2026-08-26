from groq import Groq
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embeddings = FakeEmbeddings(size=384)
INDEX_DIR = "faiss_index"

class ChatRequest(BaseModel):
    prompt: str

async def chat_bot(prompt: str):
    context_text = ""

    # 1. Check if a FAISS index exists on disk
    if os.path.exists(INDEX_DIR):
        try:
            vector_store = FAISS.load_local(
                INDEX_DIR, 
                embeddings, 
                allow_dangerous_deserialization=True
            )
            
            # Retrieve the top 3 matching chunks
            docs = vector_store.similarity_search(prompt, k=3)
            context_text = "\n\n".join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"Error loading index: {e}")

    # 2. Build the context-grounded prompt
    if context_text.strip():
        system_prompt = (
            "You are a helpful assistant. Use the following context from the document to answer the question. "
            "If the question cannot be answered from the document, answer using your general knowledge.\n\n"
            f"Context:\n{context_text}"
        )
    else:
        system_prompt = "You are a helpful AI assistant."

    # 3. Call Groq
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as err:
        print(f"Groq API Error: {err}")
        return f"Service Notice: {str(err)}"






    ''' (old code)
    try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return "Sorry, I couldn't process your request at the moment."
        
    '''
    