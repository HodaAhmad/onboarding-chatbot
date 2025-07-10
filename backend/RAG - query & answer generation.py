# RAG Pipeline for TUM onboarding Assistant


# ========== Installations ==========
#C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install langchain langchain-community langchain-text-splitters chromadb sentence-transformers
#C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install -U langchain-chroma
##C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install -U langchain-huggingface

# RAG + Escalation Pipeline for TUM Onboarding Assistant

# ========== Imports ==========
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import google.generativeai as genai
import pandas as pd

# ========== Load Vector Store ==========
def load_vector_store(persist_dir, embedding_model):
    return Chroma(persist_directory=persist_dir, embedding_function=embedding_model)

# ========== Load Contacts from Excel ==========
def load_contacts(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

# ========== Build Structured Prompt ==========
def build_structured_prompt(context: str, question: str, contacts_df: pd.DataFrame) -> str:
    identity_tone = (
        "You are a smart, friendly, and professional onboarding assistant for new and international students "
        "at the Technical University of Munich (TUM). Your goal is to help students navigate administrative "
        "and onboarding-related tasks such as enrollment, visa, housing, course registration, and consultation hours. "
        "Use a warm, polite, and informative tone. Be concise but supportive. Assume no prior knowledge of TUM processes."
    )

    factual_grounding = (
        "Always base your answers strictly on the retrieved context provided below. "
        "Do not invent or assume information that is not present in the context. "
        "If a question cannot be answered using the provided context, follow the escalation protocol."
    )

    personalization_language = (
        "If prior user data (e.g., department or study program) is available, personalize responses accordingly. "
        "Support queries in English, German, or a mix of both. Respond in the same language style used by the student."
    )

    available_topics = contacts_df["Topic"].dropna().unique().tolist()
    topics_formatted = ", ".join(available_topics)

    escalation_protocol = (
        f"If you are unable to answer the student’s question confidently based on the context, identify the most relevant topic "
        f"from the following list: {topics_formatted}. Then suggest the correct administrative contact from the internal contact database. "
        "Generate a complete sample email the student can copy, adapted to the user’s issue based on their last question.\n\n"
        "Here is an example of the format to follow:\n"
        "Subject: Inquiry regarding course enrollment\n\n"
        "Dear Dr. Mayer,\n\n"
        "I am a newly admitted student at TUM and I have some questions about the course enrollment process, specifically regarding deadlines and prerequisites.\n\n"
        "Could you kindly guide me on how to proceed or let me know where I can find more details?\n\n"
        "Best regards,\n"
        "John Doe"
    )

    interactivity_guidance = (
        "If a response requires user input (like department selection), provide a clear list of options. "
        "Guide multi-step actions with simple instructions."
    )

    return f"""
You have the following identity and tone:
{identity_tone}

Consider the following rule about using the data:
{factual_grounding}

Personalization and language handling instructions:
{personalization_language}

Escalation protocol if the answer is not found in the context:
{escalation_protocol}

Guidance for interactivity:
{interactivity_guidance}

------------------------------
Retrieved Context:
{context}

User Question:
{question}

Answer:
""".strip()

# ========== Main Conversational Loop ==========
def conversation_loop(retriever, api_key, contacts_df):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite-001")

    prev_question = input("\n🧠 Enter your question: ")
    attempts = 0

    while True:
        results = retriever.invoke(prev_question)
        context = "\n\n".join(doc.page_content for doc in results)

        prompt = build_structured_prompt(context=context, question=prev_question, contacts_df=contacts_df)
        response = model.generate_content(prompt)
        print("\n🤖 Gemini Answer:\n", response.text)

        follow_up = input("\n📩 Is your question answered? (yes / no / rephrase): ").strip().lower()

        if follow_up in ["yes", "y"]:
            break
        elif follow_up == "rephrase":
            prev_question = input("Please rephrase your question: ")
            continue
        elif follow_up in ["no", "n"]:
            attempts += 1
            if attempts >= 2:
                print("\n🛎️ Please ask your question again or clarify your topic.")
        else:
            print("❓ I didn't understand that. Type 'yes', 'no', or 'rephrase'.")

# ========== Main Program ==========
if __name__ == "__main__":
    PERSIST_DIR = "vector_db"
    GEMINI_API_KEY = "AIza..."  # Use os.environ in production
    CONTACTS_FILE = "reference list of contacts.xlsx"

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = load_vector_store(PERSIST_DIR, embedding_model)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    contacts_df = load_contacts(CONTACTS_FILE)

    conversation_loop(retriever, GEMINI_API_KEY, contacts_df)
