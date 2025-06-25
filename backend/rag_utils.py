# rag_utils.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import google.generativeai as genai

from sentence_transformers import SentenceTransformer

class ChromaEmbeddingFunction:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.model.encode(input).tolist()

    def embed_query(self, input: str) -> list[float]:
        return self.model.encode([input])[0].tolist()

    def embed_documents(self, inputs: list[str]) -> list[list[float]]:
        return self.model.encode(inputs).tolist()


def generate_answer_with_rag(user_question: str, api_key: str) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-lite-001")

    embedding_model = ChromaEmbeddingFunction()
    vector_store = Chroma(
        persist_directory="vector_db",
        embedding_function=embedding_model,
        collection_name="rag_collection"
    )

    print(f"🔍 Querying vector DB with: {user_question}")
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(user_question)
    print(f"📚 Retrieved {len(docs)} relevant chunks")

    if not docs:
        return "Sorry, I couldn't find any relevant information."

    for i, doc in enumerate(docs):
        print(f"--- Chunk {i+1} ---\n{doc.page_content[:300]}...\n")

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a helpful onboarding assistant at TUM.
Use the following context to answer the user’s question.

Context:
{context}

Question:
{user_question}

Answer:"""

    response = model.generate_content(prompt)
    return response.text.strip()
