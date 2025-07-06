# Step 2: Control Layer - RulesEnforcer
# =======================================
# This module enforces institutional policies and conversation boundaries.

class RulesEnforcer:
    def __init__(self, allowed_topics=None):
        if allowed_topics is None:
            allowed_topics = [
                "admission", "enrollment", "housing", "visa", "student services",
                "consultation", "academic calendar", "course registration"
            ]
        self.allowed_topics = set(topic.lower() for topic in allowed_topics)

    def is_topic_allowed(self, topic: str) -> bool:
        return topic.lower() in self.allowed_topics

    def is_escalation_forced(self, state: str, attempts: int, max_allowed: int) -> bool:
        return state == "retrieving" and attempts >= max_allowed


# ---- Example Usage ----
if __name__ == "__main__":
    enforcer = RulesEnforcer()

    print(enforcer.is_topic_allowed("housing"))       # True
    print(enforcer.is_topic_allowed("food services"))  # False

    print(enforcer.is_escalation_forced("retrieving", 2, 2))  # True
    print(enforcer.is_escalation_forced("retrieving", 1, 2))  # False