from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
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

        model = genai.GenerativeModel("gemini-2.0-flash-lite-001")

        chat_history = [
            {"role": m.role, "parts": [m.content]} for m in chat.messages
        ]
        print("Sending to Gemini:", chat_history)

        response = model.generate_content(chat_history)
        print("Gemini responded:", response.text)

        return {"reply": response.text}

    except Exception as e:
        print("Gemini error:", str(e))
        return {"error": "Gemini failed to respond properly.", "details": str(e)}
