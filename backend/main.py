# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from RAG.rag_utils import generate_answer_with_rag
from dotenv import load_dotenv

from escalation.escalation_formatter import EscalationFormatter  

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

        result = generate_answer_with_rag(user_input, GOOGLE_API_KEY)
        print("🤖 Gemini RAG reply:", result["answer"])

        if result["needs_escalation"]:
            print("🚨 Escalation triggered for:", user_input)
            Topics=["International Affairs","Campus Life & Services", "Academic & Courses", "Admission & Enrollment"]
            prompt_escalation=f"According to the {user_input}, identify the topic from here: {Topics}. If the topic is not clear, use 'General'. The ouput should be only the given name topic such as 'Campus Life & Services' , do not anything else"
            topic= generate_answer_with_rag(prompt_escalation, GOOGLE_API_KEY)
            print("🔍 Identified topic for escalation:", topic)
            if topic != "General":
                print("🔍 Identified topic for escalation:", topic)
                ef = EscalationFormatter("data/List.xlsx", GOOGLE_API_KEY)
                escalation_prompt = ef.generate_email(user_input, topic=topic)  # Can add real topic detection later
                print("📧 Generated escalation email:\n", escalation_prompt)

                return {
                    "reply": result["answer"],
                    "escalation": True,
                    "email_draft": escalation_prompt
                }

        return {
            "reply": result["answer"],
            "escalation": False
        }

    except Exception as e:
        print("Gemini error:", str(e))
        return {"error": "Gemini failed to respond properly.", "details": str(e)}
