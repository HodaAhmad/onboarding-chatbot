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
from utils import extract_program_from_messages

import google.generativeai as genai


#suported programss
VALID_PROGRAMS = ["MIM", "MMDT", "MIE"]

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
    program: str | None = None  


# === Final /chat endpoint ===
@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    try:
        ...
        user_input = chat.messages[-1].content
        print("User asked:", user_input)

        #Check if user selected program already
        chat_history = [msg.content for msg in chat.messages]

        #Use provided program from frontend if exists
        program_selected = chat.program or extract_program_from_messages(chat_history)
        print("[DEBUG] Extracted program:", program_selected)
        if user_input.strip().upper() in VALID_PROGRAMS:
            return {
                "reply": f"Thanks for confirming you're in the {program_selected} program! How can I help you today?",
                "escalation": False
            }

        if not program_selected:
            return {
                "reply": "Hello 👋 Before we continue, can you let me know which Masters program you're in?\n\n• Master in Management (MIM)\n• Management in Data & Technology (MMDT)\n• Information Engineering (MIE)",
                "program_requested": True
            }

        #Step 1: Detect intent
        intent = classify_user_input(user_input, GOOGLE_API_KEY)
        print("Detected intent:", intent) # What Gemini thinks the user's goal is

        #Step 2: Run RAG if it's an onboarding question OR a valid program was selected
        if intent in ["Onboarding_FAQ", "Clarification_Request"] or program_selected:
            result = generate_answer_with_rag(user_input, GOOGLE_API_KEY, program_selected)
            print("Gemini RAG reply:", result["answer"])

            if result["answer"].startswith("Sorry, I couldn't find"):
                print("No context retrieved from vector DB")
                return {
                    "reply": result["answer"],
                    "escalation": False
                }

            if result["needs_escalation"]:
                print("Escalation triggered for:", user_input)
                contact_file_path = "data/List.xlsx"
                topics = get_topic_list_from_excel(contact_file_path)
                topic = identify_topic_from_answer(result["answer"], GOOGLE_API_KEY)
                print("Identified topic for escalation:", topic)

                ef = EscalationFormatter(contact_file_path, GOOGLE_API_KEY)
                escalation_prompt = ef.generate_email(user_input, topic=topic)
                print("Generated escalation email:\n", escalation_prompt)

                return {
                    "reply": result["answer"],
                    "escalation": True,
                    "email_draft": escalation_prompt
                }

            return {
                "reply": result["answer"],
                "escalation": False
            }


        #Step 6: Handle non-RAG intents dynamically
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

