from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

# 🔹 SAME embeddings as indexing (IMPORTANT)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 🔹 Connect to Qdrant
qdrant = QdrantVectorStore.from_existing_collection(
    url="https://f75ff0dd-e683-4881-b4be-90a5237504c4.sa-east-1-0.aws.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.vSZBFprgQwG8MK_6UlJZffKzASfudqQs4Tx73XhWO2Q",
    collection_name="nitin_resume",
    embedding=embeddings
)

# 🔹 Simple retriever
retriever = qdrant.as_retriever(search_kwargs={"k": 5})

print("\n✅ Resume Search Ready (FREE MODE) | type 'exit' to quit\n")

# 🔹 Chat loop (NO LLM, direct answer from resume)
while True:
    query = input("🧑 Ask: ")

    if query.lower() in ["exit", "quit"]:
        print("👋 Exiting...")
        break

    # 🔹 Retrieve relevant chunks
    docs = retriever.invoke(query)

    if not docs:
        print("\n❌ No relevant data found\n")
        continue

    print("\n📄 Relevant Resume Content:\n")

    for i, doc in enumerate(docs, 1):
        print(f"{i}. {doc.page_content}\n")