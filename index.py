from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load PDF
pdf_path = Path(__file__).parent / "Nitin_Yadav_GenAI.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# Split
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(docs)

# Embeddings (FREE)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Qdrant Cloud
qdrant = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="https://f75ff0dd-e683-4881-b4be-90a5237504c4.sa-east-1-0.aws.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.vSZBFprgQwG8MK_6UlJZffKzASfudqQs4Tx73XhWO2Q",
    collection_name="nitin_resume"
)

print("✅ Stored successfully in Qdrant")