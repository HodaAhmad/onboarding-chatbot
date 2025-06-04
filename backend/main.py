from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables (for the OpenAI API key)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS so frontend can call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define message format
class ChatMessage(BaseModel):
    role: str
    content: str

# Define request format
class ChatRequest(BaseModel):
    messages: list[ChatMessage]

# Endpoint to handle chat requests
@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    if not openai.api_key:
        return {
            "reply": f"(Demo mode) You said: {chat.messages[-1].content}",
            "note": "No OpenAI API key found. This is a dummy response."
        }

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": m.role, "content": m.content} for m in chat.messages]
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
