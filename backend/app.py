from fastapi import FastAPI
from pydantic import BaseModel
from interaction.intent_classifier import IntentClassifier
from interaction.session_state import SessionStateManager
from control.conversation_router import ConversationRouter
from control.retry_manager import RetryManager
from control.rules_enforcer import RulesEnforcer
from reasoning.rag_retriever import RAGRetriever
from reasoning.llm_responder import LLMResponder
from reasoning.prompt_builder import build_escalation_prompt, build_retrieval_prompt
from reasoning.escalation_formatter import EscalationFormatter
import os

app = FastAPI()

# Setup once
api_key = os.getenv("GOOGLE_API_KEY") or "AIzaSyC-o2rdSWFw63JzM0GiXVUp115MdGFo_fA"
classifier = IntentClassifier(api_key)
state = SessionStateManager()
retry_mgr = RetryManager()
enforcer = RulesEnforcer()
retriever = RAGRetriever()
responder = LLMResponder(api_key)
formatter = EscalationFormatter("data/List.xlsx")
router = ConversationRouter(retriever, formatter)

# Input model for chat
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(chat: ChatRequest):
    try:
        print("📩 Received:", chat.message)

        user_input = chat.message
        intent = classifier.classify(user_input)

        state.update_state(intent)
        result = router.route(intent, state.state, user_input, retry_mgr.attempts)

        if result["action"] == "retrieve":
            prompt = build_retrieval_prompt(result["context"], user_input)
            reply = responder.generate(prompt)
            return {"reply": reply}

        elif result["action"] == "escalate":
            prompt = result["email"]
            reply = responder.generate(prompt)
            return {"reply": result["message"], "email": reply}

        elif result["action"] == "clarify":
            retry_mgr.register_attempt()
            return {"reply": result["message"]}

        elif result["action"] == "close":
            return {"reply": result["message"]}

        retry_mgr.reset_attempts()

    except Exception as e:
        import traceback
        print("❌ ERROR:", str(e))
        traceback.print_exc()
        return {"error": "Internal Server Error", "detail": str(e)}
