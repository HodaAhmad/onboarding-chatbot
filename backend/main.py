# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from rag_utils import generate_answer_with_rag

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]

@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    try:
        if not GOOGLE_API_KEY:
            return {
                "reply": f"(Demo mode) You said: {chat.messages[-1].content}",
                "note": "No Gemini API key found. This is a dummy response."
            }

        user_input = chat.messages[-1].content
        print("📥 User asked:", user_input)

        reply = generate_answer_with_rag(user_input, GOOGLE_API_KEY)
        print("🤖 Gemini RAG reply:", reply)

        return {"reply": reply}

    except Exception as e:
        print("Gemini error:", str(e))
        return {"error": "Gemini failed to respond properly.", "details": str(e)}
