from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer

#Correct embedding function wrapper
class ChromaEmbeddingFunction:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.model.encode(input).tolist()

    def embed_query(self, input: str) -> list[float]:
        return self.model.encode([input])[0].tolist()

    def embed_documents(self, inputs: list[str]) -> list[list[float]]:
        return self.model.encode(inputs).tolist()

#Main retriever class using updated wrapper
class RAGRetriever:
    def __init__(self, persist_directory: str = "vector_db", model_name: str = "all-MiniLM-L6-v2"):
        self.persist_directory = persist_directory
        self.embedding_model = ChromaEmbeddingFunction(model_name=model_name)

        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )

        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

    def retrieve(self, query: str) -> str:
        """Retrieve top relevant chunks and return as formatted text."""
        results = self.retriever.invoke(query)
        if not results:
            return ""
        return "\n\n".join(doc.page_content for doc in results)


# ---- Example Usage ----
if __name__ == "__main__":
    rag = RAGRetriever()
    query = "How do I register for my first semester?"
    context = rag.retrieve(query)
    print("Retrieved Context:\n", context)
