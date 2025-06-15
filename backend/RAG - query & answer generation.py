# RAG Pipeline for TUM onboarding Assistant


# ========== Installations ==========
#C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install langchain langchain-community langchain-text-splitters chromadb sentence-transformers
#C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install -U langchain-chroma
##C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install -U langchain-huggingface

#========== Imports ==========
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import google.generativeai as genai

# ========== Step 5.1: Loading  ==========
def load_vector_store(persist_dir, embedding_model):
    """
    Load ChromaDB vector store from disk.
    """
    return Chroma(persist_directory=persist_dir, embedding_function=embedding_model)





# ========== Step 5.2: Query & Generate Answer ==========
def ask_question_with_gemini(retriever, question, api_key):
    """
    Query ChromaDB and generate a Gemini response.
    """ 
    results = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in results)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite-001")

    prompt = f"""Use the following information to answer the question.

Context:
{context}

Question:
{question}

Answer:"""

    response = model.generate_content(prompt)
    print("\n🤖 Gemini Answer:\n", response.text)


# ========== Retrieval ==========
if __name__ == "__main__":
    # --- Configuration ---
    PERSIST_DIR = "vector_db"
    GEMINI_API_KEY = "AIzaSyC-o2rdSWFw63JzM0GiXVUp115MdGFo_fA"  # Or use environment variable
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


    # Load saved vector store
    vector_store = load_vector_store(PERSIST_DIR, embedding_model)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}  # Adjust number of chunks returned
    )

    user_question = "What are the study progress credit requirements at TUM?"

    results = retriever.get_relevant_documents(user_question)
    print(f"[DEBUG] Number of chunks retrieved: {len(results)}")  # <--- ADD THIS
    
    if not results:
        print("❗ No relevant documents found.")


    for i, doc in enumerate(results, 1):
        print(f"\n--- Retrieved Chunk {i} from Page {doc.metadata.get('page')} ---")
        print("Text:", repr(doc.page_content[:300]))
        print("Metadata:", doc.metadata)




#user_question = input("\n🧠 Enter your question: ")
#ask_question(retriever, "What are the credit requirements at TUM?", api_key)
