# rag_preprocess.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
import os

class ChromaEmbeddingFunction:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.model.encode(input).tolist()

    def embed_query(self, input: str) -> list[float]:
        return self.model.encode([input])[0].tolist()

    def embed_documents(self, inputs: list[str]) -> list[list[float]]:
        return self.model.encode(inputs).tolist()

# Step 1: Load your onboarding PDF
def load_docs(folder="data"):
    all_docs = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder, file))
            pages = loader.load()
            all_docs.extend(pages)
    print(f"📄 Loaded {len(all_docs)} pages.")
    return all_docs

# Step 2: Chunk the text
def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"✂️ Created {len(chunks)} chunks.")
    return chunks

# Step 3: Embed and store
def store_embeddings(chunks, path="vector_db"):
    embeddings = ChromaEmbeddingFunction()
    Chroma.from_documents(chunks, embedding=embeddings, persist_directory=path)
    print(f"✅ Vector DB saved to '{path}'.")

if __name__ == "__main__":
    docs = load_docs("data")
    chunks = chunk_docs(docs)
    store_embeddings(chunks, "vector_db")
