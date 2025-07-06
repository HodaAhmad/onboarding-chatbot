# This file defines the ConversationRouter responsible for decision flow
# depending on the user intent and session state.

class ConversationRouter:
    def __init__(self, retriever, escalation_handler):
        self.retriever = retriever
        self.escalation_handler = escalation_handler

    def route(self, intent: str, state: str, user_input: str, attempts: int) -> dict:
        """
        Route the conversation based on current state and intent.

        Returns:
            dict: {
                "action": one of ["retrieve", "escalate", "clarify", "close"],
                "message": optional message to display,
                "context": optional context if retrieved
            }
        """
        if state == "closed" or intent == "goodbye":
            return {"action": "close", "message": "Thank you for using the assistant. Goodbye!"}

        if state == "escalating" or intent == "escalation" or attempts >= 2:
            email = self.escalation_handler.generate_email(user_input)
            return {
                "action": "escalate",
                "message": "I'm unable to find the information you need. Please consider sending this email to the responsible contact:",
                "email": email
            }

        if state == "retrieving" and intent in ["information_request", "clarification"]:
            context = self.retriever.retrieve(user_input)
            return {
                "action": "retrieve",
                "context": context,
                "message": "Here is what I found based on your question."
            }

        return {"action": "clarify", "message": "Could you please clarify your question a bit more?"}
    


# ======================================
# This module tracks how many clarification attempts have occurred.

class RetryManager:
    def __init__(self, max_retries: int = 2):
        self.attempts = 0
        self.max_retries = max_retries

    def register_attempt(self):
        self.attempts += 1

    def reset_attempts(self):
        self.attempts = 0

    def should_escalate(self) -> bool:
        return self.attempts >= self.max_retries


# ---- Example Usage ----
if __name__ == "__main__":
    retry_manager = RetryManager(max_retries=2)
    retry_manager.register_attempt()
    retry_manager.register_attempt()

    if retry_manager.should_escalate():
        print("Trigger escalation logic")
    else:
        print("Continue normal response")