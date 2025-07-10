import pandas as pd
import google.generativeai as genai
from reasoning.prompt_builder import build_escalation_prompt

# 📌 Intent classifier using Gemini
def classify_user_input(user_input: str, api_key: str) -> str:
    prompt = f"""
You are an intent classification system. Classify the user's message into one of the following **exact categories**:

1. Onboarding_FAQ
2. Clarification_Request
3. Chitchat
4. OffTopic
5. Navigation_Help
6. System_Issue_Report

Guidelines:
- Onboarding_FAQ: factual, TUM-related questions about academics, housing, enrollment, etc.
- Clarification_Request: user seems confused or wants help understanding something.
- Chitchat: greetings, thanks, or unrelated friendly conversation.
- OffTopic: unrelated to TUM onboarding.
- Navigation_Help: user asks how to use the assistant or platform.
- System_Issue_Report: technical error or issue mentioned.

IMPORTANT: Only return one category name. Do NOT explain or say anything else.

Message:
"{user_input}"
""".strip()

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-lite-001")
    response = model.generate_content(prompt)
    return response.text.strip()


# Extract unique topic names from Excel
def get_topic_list_from_excel(contact_file: str) -> list[str]:
    df = pd.read_excel(contact_file)
    return sorted(df["Topic"].dropna().unique().tolist())

# Ask Gemini to identify the exact topic based on answer
def identify_topic_from_answer(answer_text: str, api_key: str) -> str:
    """
    Uses Gemini to classify a student's onboarding-related question into a known topic.
    Includes few-shot examples and inline descriptions.
    """

    # 💬 Descriptions to help Gemini reason semantically
    topic_descriptions = {
        "International Affairs": "Topics related to international students, visas, or global mobility",
        "Campus Life & Services": "Questions about housing, cafeterias, sports, student services",
        "Academic & Courses": "Questions about programs, courses, professors, exams, ECTS, or credits",
        "Admission & Enrollment": "Application process, deadlines, requirements, enrollment status"
    }

    # 🧠 Few-shot examples to ensure clean topic output
    few_shot_examples = """
Examples:

Question: What is the minimum GPA required for admission?
Answer: The system could not find exact information about GPA requirements.
Admission & Enrollment

Question: Which courses does Professor Müller teach in the Computer Science department?
Answer: The assistant couldn't retrieve that info. It might require escalation.
Academic & Courses

Question: How can I register at the Studentenwerk for accommodation?
Answer: I recommend contacting housing services for details about accommodation.
Campus Life & Services
"""

    # 🧠 Prompt construction with descriptions + examples
    prompt_lines = [
        "You are an assistant that classifies a student's onboarding-related question into one of the following topics:\n"
    ]

    for topic, desc in topic_descriptions.items():
        prompt_lines.append(f"- {topic}: {desc}")

    prompt_lines.append(f"\n{few_shot_examples.strip()}\n")

    prompt_lines.append(f"""
Now classify the following case:

Answer:
\"\"\"{answer_text}\"\"\"
""")

    prompt = "\n".join(prompt_lines)

    # 🔍 Send to Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-lite-001")
    response = model.generate_content(prompt)
    topic = response.text.strip()

    # 🖨️ Debug print to inspect exact Gemini output
    print(f"🔍 Gemini classified topic as: '{topic}'")

    return topic



class EscalationFormatter:
    def __init__(self, contact_file: str, api_key: str):
        self.contacts_df = pd.read_excel(contact_file)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-lite-001")

    def match_contact(self, topic: str) -> dict:
        matches = self.contacts_df[self.contacts_df['Topic'].str.lower() == topic.lower()]
        print(f"👤 Matching contact for topic: {topic}")  # Debug topic before lookup
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
        print(f"📨 Building escalation email for topic '{topic}' and question:\n{user_question}")
        prompt = build_escalation_prompt(
            question=user_question,
            topic=contact["topic"],
            contact_name=contact["name"],
            contact_email=contact["email"]
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()
