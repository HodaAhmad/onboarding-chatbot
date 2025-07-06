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
Topic: Course Registration
Contact: Dr. Eva Schmitt <eva.schmitt@tum.de>

Email:
Subject: Inquiry regarding Course Registration

Dear Dr. Schmitt,

I am a newly admitted student at TUM and I have a question regarding course registration. I would appreciate any guidance or information you can provide on how to proceed.

Best regards,
[Your Name]
---

Now, based on the student's question below, generate a similar escalation email:

Student's Question:
"{question}"

Topic: {topic}
Contact: {contact_name} <{contact_email}>

Your response should be a complete, polite email in the same format.
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
