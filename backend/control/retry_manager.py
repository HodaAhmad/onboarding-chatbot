# Step 2 Control Layer - RetryManager
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