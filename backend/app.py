from interaction.intent_classifier import IntentClassifier
from interaction.session_state import SessionStateManager
from control.conversation_router import ConversationRouter
from control.retry_manager import RetryManager
from control.rules_enforcer import RulesEnforcer
from reasoning.rag_retriever import RAGRetriever
from reasoning.llm_responder import LLMResponder
from reasoning.prompt_builder import build_escalation_prompt
from reasoning.prompt_builder import build_retrieval_prompt
from reasoning.escalation_formatter import EscalationFormatter


# Setup
api_key = "AIzaSyC-o2rdSWFw63JzM0GiXVUp115MdGFo_fA"
classifier = IntentClassifier(api_key)
state = SessionStateManager()
retry_mgr = RetryManager()
enforcer = RulesEnforcer()
retriever = RAGRetriever()
responder = LLMResponder(api_key)
formatter = EscalationFormatter("C:/Users/User/OneDrive - TUM/Desktop/TUM MMDT/First semester/Foundations of generative AI/Project/Versions/List.xlsx")
router = ConversationRouter(retriever, formatter)

# Conversation loop
while state.state != "closed":
    user_input = input("You: ")
    intent = classifier.classify(user_input)
    state.update_state(intent)

    result = router.route(intent, state.state, user_input, retry_mgr.attempts)

    if result["action"] == "retrieve":
        prompt = build_retrieval_prompt(result["context"], user_input)
        answer = responder.generate(prompt)
        print("Bot:", answer)

    elif result["action"] == "escalate":
        escalation_prompt = result["email"]
        answer = responder.generate(escalation_prompt)
        print("Bot:", result["message"])
        print("📩 Suggested Email:\n", answer)
        break

    elif result["action"] == "clarify":
        retry_mgr.register_attempt()
        print("Bot:", result["message"])

    elif result["action"] == "close":
        print("Bot:", result["message"])
        break





