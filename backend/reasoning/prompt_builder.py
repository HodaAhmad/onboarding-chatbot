# Step 3: Reasoning Layer - PromptBuilder
# ========================================
# This module builds structured prompts for Gemini depending on the conversation phase.

def build_retrieval_prompt(context: str, question: str) -> str:
    return f"""
You are a university onboarding assistant for TUM. Use the provided context to answer the student's question.

Instructions:
- Respond formally and clearly.
- Do not invent or speculate.
- If the context does not contain the answer, say you are unable to help and recommend escalation.
- Important: Make sure to include the contact's email address in the final email body.

Context:
\"\"\"{context}\"\"\"

Question:
\"{question}\"

Answer:
""".strip()




def build_escalation_prompt(question: str, topic: str, contact_name: str, contact_email: str) -> str:
    return f"""
A student has an unresolved question that requires escalation. Below is an example email that a student might send.

---
Example:
Student's Question: "I need help understanding how to register for my courses."
Topic: Course Registration Your response should be a complete, polite email in the same format.

Contact: Dr. Eva Schmitt <eva.schmitt@tum.de>

Email:
Subject: Inquiry regarding Course Registration

Dear Dr. Schmitt,

I am a newly admitted student at TUM and I have a question regarding course registration. I would appreciate any guidance or information you can provide on how to proceed.

Best regards,
[Your Name]
---

Now, based on the student's question below, generate a similar escalation email:
Important: Make sure to include the contact's email address in the final email body.

Student's Question:
"{question}"

Topic: {topic}
Contact: {contact_name} <{contact_email}>

Your response should be a complete, polite email in the same format.
""".strip()

# New function for dynamic prompting based on intent
def build_intent_prompt(intent: str, user_input: str) -> str:
    print(f"🛠️ Building intent prompt for '{intent}' with input:\n{user_input}")
    if intent == "Chitchat":
        return f"""
You are a friendly university assistant. Reply warmly and briefly to this casual message:

"{user_input}"
""".strip()

    elif intent == "Clarification_Request":
        return f"""
The user is asking for clarification. Respond helpfully and politely, assuming they want to understand more about onboarding or your capabilities.

Message:
"{user_input}"
""".strip()

    elif intent == "OffTopic":
        return f"""
The user’s message is unrelated to TUM onboarding. Politely inform them that your role is limited to onboarding support.

Message:
"{user_input}"
""".strip()

    elif intent == "Navigation_Help":
        return f"""
The user is asking how to use the onboarding assistant. Explain that they can ask questions about studying, enrolling, housing, or support services at TUM.

Message:
"{user_input}"
""".strip()

    elif intent == "System_Issue_Report":
        return f"""
The user is reporting a technical issue. Acknowledge the problem and advise them to contact the TUM IT support team or relevant office.

Message:
"{user_input}"
""".strip()

    else:
        return f"""
You are a TUM onboarding assistant. Respond clearly and formally to this question.

Question:
"{user_input}"
""".strip()





# ---- Example Usage ----
if __name__ == "__main__":
    sample_context = "TUM students must register for courses by October 15."
    sample_question = "What’s the deadline to register for my courses?"
    print(build_retrieval_prompt(sample_context, sample_question))

    print("\n---\n")
    print(build_escalation_prompt(
        question=sample_question,
        topic="Course Registration",
        contact_name="Dr. Anna Keller",
        contact_email="anna.keller@tum.de"
    ))
