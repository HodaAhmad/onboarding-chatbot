# RAG Pipeline for TUM onboarding Assistant


# ========== Installations ==========
#C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install langchain langchain-community langchain-text-splitters chromadb sentence-transformers
#C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install chromadb
##C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install -U langchain-huggingface
#C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install cryptography
#C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe -m pip install -U langchain-chroma

#========== Imports ==========
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_core.documents import Document  # optional, for clarity

import os


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


# ========== Step 1: Load ==========
def load_documents(folder_path):
    """
    Load PDF documents for processing.
    Each PDF is split by page into structured 'Document' objects.
    """
    all_docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            print(f"[LOAD] Reading: {filename}")
            docs = PyPDFLoader(path).load()
            all_docs.extend(docs)
    print(f"[LOAD] Total pages loaded: {len(all_docs)}")
    return all_docs

# ========== Step 2: Split ==========
def split_documents(documents, chunk_size=800, chunk_overlap=500):
    """
    Split large text into smaller 'chunks' while keeping context overlap.
    This helps the AI retrieve more accurate info later.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    print(f"[SPLIT] Total chunks created: {len(chunks)}")
    return chunks

# ========== Step 3: Embed ==========
def embed_chunks():
    """
    Use a local transformer model to create vector representations (embeddings).
    These are used to match future questions with the most relevant text.
    """
    embedding_model = ChromaEmbeddingFunction()
    print("[EMBED] Local embeddings created using HuggingFace model")
    return embedding_model

# ========== Step 4: Store ==========
def store_embeddings(chunks, embedding_model, persist_directory="vector_db"):
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory,
        collection_name="rag_collection"
    )
    print(f"[STORE] Vector store saved in '{persist_directory}' directory")

if __name__ == "__main__":
    ##PDF_FOLDER = r"C:/Users/User/OneDrive - TUM/Desktop/TUM MMDT/First semester/Foundations of generative AI/Project/Onboarding"
    PDF_FOLDER = 'data'
    PERSIST_DIR = "vector_db"

    documents = load_documents(PDF_FOLDER)
    chunks = split_documents(documents)
    model = embed_chunks()
    store_embeddings(chunks, model, persist_directory=PERSIST_DIR)

print("hello world")




