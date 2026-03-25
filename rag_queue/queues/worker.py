from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

# 🔹 Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 🔹 Qdrant connection
qdrant = QdrantVectorStore.from_existing_collection(
    url="https://f75ff0dd-e683-4881-b4be-90a5237504c4.sa-east-1-0.aws.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.vSZBFprgQwG8MK_6UlJZffKzASfudqQs4Tx73XhWO2Q",
    collection_name="nitin_resume",
    embedding=embeddings
)

retriever = qdrant.as_retriever(search_kwargs={"k": 5})


# ✅ Proper worker function
def process_query(query: str):
    docs = retriever.invoke(query)

    if not docs:
        return "❌ No relevant data found"

    results = []
    for i, doc in enumerate(docs, 1):
        results.append(f"{i}. {doc.page_content}")

    return "\n\n".join(results)