# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from RAG.rag_utils import generate_answer_with_rag
from escalation.escalation_formatter import EscalationFormatter, get_topic_list_from_excel, identify_topic_from_answer
from reasoning.prompt_builder import build_intent_prompt
from escalation.escalation_formatter import classify_user_input 

import google.generativeai as genai

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# FastAPI setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]

# === Final /chat endpoint ===
@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    try:
        if not GOOGLE_API_KEY:
            return {
                "reply": f"(Demo mode) You said: {chat.messages[-1].content}",
                "note": "No Gemini API key found. This is a dummy response."
            }

        user_input = chat.messages[-1].content
        print("📥 User asked:", user_input) # Incoming user message
        
        # 🔍 Step 1: Detect intent
        intent = classify_user_input(user_input, GOOGLE_API_KEY)
        print("🎯 Detected intent:", intent) # What Gemini thinks the user's goal is

        # 📚 Step 2: Run RAG for TUM-related messages
        if intent in ["Onboarding_FAQ", "Clarification_Request"]:
            result = generate_answer_with_rag(user_input, GOOGLE_API_KEY)
            print("🤖 Gemini RAG reply:", result["answer"]) # Final RAG-based answer before escalation logic

            # 📭 Step 3: If no context retrieved, return fallback answer
            if result["answer"].startswith("Sorry, I couldn't find"):
                print("📭 No context retrieved from vector DB")  # Confirm DB miss
                return {
                    "reply": result["answer"],
                    "escalation": False
                }

            # 🚨 Step 4: Trigger escalation if needed
            if result["needs_escalation"]:
                print("🚨 Escalation triggered for:", user_input)
                print("🚨 Escalation triggered due to low-confidence answer")  # Escalation heuristic triggered
                contact_file_path = "data/List.xlsx"
                topics = get_topic_list_from_excel(contact_file_path)
                topic = identify_topic_from_answer(result["answer"], GOOGLE_API_KEY)
                print("🔍 Identified topic for escalation:", topic) # Topic Gemini matched from answer

                # ✉️ Always allow escalation, even for "General"
                ef = EscalationFormatter(contact_file_path, GOOGLE_API_KEY)
                escalation_prompt = ef.generate_email(user_input, topic=topic)
                print("📧 Generated escalation email:\n", escalation_prompt) # Final email draft preview

                return {
                    "reply": result["answer"],
                    "escalation": True,
                    "email_draft": escalation_prompt
                }

            # ✅ Step 5: Return regular answer if no escalation
            return {
                "reply": result["answer"],
                "escalation": False
            }

        # 💬 Step 6: Handle non-RAG intents dynamically
        else:
            prompt = build_intent_prompt(intent, user_input)
            model = genai.GenerativeModel("gemini-2.0-flash-lite-001")
            response = model.generate_content(prompt)

            return {
                "reply": response.text.strip(),
                "escalation": False
            }

    except Exception as e:
        print("Gemini error:", str(e))
        return {"error": "Gemini failed to respond properly.", "details": str(e)}

