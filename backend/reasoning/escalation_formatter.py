# Step 3: Reasoning Layer - EscalationFormatter
# ==============================================
# Looks up contact info and builds prompt for escalation email generation.

import pandas as pd
from reasoning.prompt_builder import build_escalation_prompt

class EscalationFormatter:
    def __init__(self, contact_file: str):
        self.contacts_df = pd.read_excel(contact_file)

    def match_contact(self, topic: str) -> dict:
        matches = self.contacts_df[self.contacts_df['Topic'].str.lower() == topic.lower()]
        if not matches.empty:
            row = matches.iloc[0]
            return {
                "name": row["Name"],
                "email": row["Email"],
                "topic": row["Topic"]
            }
        return {
            "name": "[Unavailable]",
            "email": "[Unavailable]",
            "topic": topic
        }

    def build_prompt(self, user_question: str, topic: str) -> str:
        contact = self.match_contact(topic)
        return build_escalation_prompt(
            question=user_question,
            topic=contact["topic"],
            contact_name=contact["name"],
            contact_email=contact["email"]
        )

    def generate_email(self, user_question: str) -> str:
            topic = "General" 
            return self.build_prompt(user_question, topic)


# ---- Example Usage ----
if __name__ == "__main__":
    ef = EscalationFormatter("../data/reference list of contacts.xlsx")
    prompt = ef.build_prompt(
        user_question="I'm confused about where to submit my visa documents.",
        topic="Visa"
    )
    print(prompt)