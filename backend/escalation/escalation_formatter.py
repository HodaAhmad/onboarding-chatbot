import pandas as pd
import google.generativeai as genai
from reasoning.prompt_builder import build_escalation_prompt

class EscalationFormatter:
    def __init__(self, contact_file: str, api_key: str):
        self.contacts_df = pd.read_excel(contact_file)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-lite-001")

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
            "name": "Ayşe Demir",
            "email": "ayse.demir@tum.de",
            "topic": "General"
        }

    def generate_email(self, user_question: str, topic: str) -> str:
        contact = self.match_contact(topic)
        prompt = build_escalation_prompt(
            question=user_question,
            topic=contact["topic"],
            contact_name=contact["name"],
            contact_email=contact["email"]
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()
