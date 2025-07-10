# rag_utils.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import google.generativeai as genai

from sentence_transformers import SentenceTransformer

# =============================================
# Custom embedding class using SentenceTransformer
# =============================================
class ChromaEmbeddingFunction:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.model.encode(input).tolist()

    def embed_query(self, input: str) -> list[float]:
        return self.model.encode([input])[0].tolist()

    def embed_documents(self, inputs: list[str]) -> list[list[float]]:
        return self.model.encode(inputs).tolist()


# =============================================
# Main function to generate an answer using RAG
# =============================================
def generate_answer_with_rag(user_question: str, api_key: str) -> str:
    genai.configure(api_key=api_key)
    print(f"📌 Running RAG for user question: {user_question}")
    model = genai.GenerativeModel("gemini-2.0-flash-lite-001")

    # 📌 Start RAG pipeline
    print(f"📌 Running RAG for user question: {user_question}")

    embedding_model = ChromaEmbeddingFunction()
    vector_store = Chroma(
        persist_directory="vector_db",
        embedding_function=embedding_model,
        collection_name="rag_collection"
    )


    # 🔎 Retrieve relevant documents from vector store
    print(f"🔍 Querying vector DB with: {user_question}")
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(user_question)

    # 📄 Report how many chunks were retrieved
    print(f"📚 Retrieved {len(docs)} relevant chunks")

    # ⚠️ No results found → fallback response
    if not docs:
        print("⚠️ No relevant documents found. Escalation might be needed.")
        return "Sorry, I couldn't find any relevant information."

    for i, doc in enumerate(docs):
        print(f"--- Chunk {i+1} ---\n{doc.page_content[:300]}...\n")

    # 📚 Build full context from top documents
    context = "\n\n".join([doc.page_content for doc in docs])

    # ✍️ Gemini prompt
    prompt = f"""
You are a helpful onboarding assistant at TUM.

Use the provided context to answer the student's question.

Instructions:
- Be confident and formal.
- If the context contains partial information, use what is available to help.
- Only recommend escalation if the context contains no useful details.
- Do not apologize unless absolutely nothing is available to assist.
- Do not speculate or make up facts.

Context:
{context}

Question:
{user_question}

Answer:"""

    # 🧠 Generate answer from Gemini
    response = model.generate_content(prompt)
    answer = response.text.strip()

    # 🧠 Show Gemini raw output
    print(f"🧠 Gemini response from context:\n{answer}")

    # ❗ Check for signs of uncertainty or short replies
    needs_escalation = any([
        "i am unable to help" in answer.lower(),
        "recommend escalation" in answer.lower(),
        "i apologize" in answer.lower(),
        "i do not have enough information" in answer.lower(),
        len(answer.strip()) < 30
    ])

    if needs_escalation:
        print("❗ Heuristic flagged this response as unclear – escalation recommended.")

    # ✅ Return the answer and whether escalation is needed
    return {
        "answer": answer,
        "needs_escalation": needs_escalation
    }
