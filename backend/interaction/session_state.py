# ---- SessionStateManager ----
class SessionStateManager:
    def __init__(self, max_attempts: int = 2):
        self.state = "start"
        self.attempts = 0
        self.max_attempts = max_attempts

    def update_state(self, intent: str):
        if self.state == "start" and intent == "greeting":
            self.state = "retrieving"
        elif self.state == "retrieving" and intent == "clarification":
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.state = "escalating"
        elif intent == "escalation":
            self.state = "escalating"
        elif intent == "goodbye":
            self.state = "closed"

    def reset(self, initial_state: str = "start"):
        self.state = initial_state
        self.attempts = 0
