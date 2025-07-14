import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredWordDocumentLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import Pinecone as LangChainPinecone
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
INDEX_NAME = "bot"
NAMESPACE = "company-docs"
DIMENSIONS = 384
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def embed_and_store_all():
    # 1. Load Word and Excel files
    word_loader = UnstructuredWordDocumentLoader("data/Chopra_Enterprise_Profile.docx")
    excel_loader = UnstructuredExcelLoader("data/Employees.xlsx")

    docs = word_loader.load() + excel_loader.load()
    print(f"📄 Loaded {len(docs)} documents")

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"🔹 {len(chunks)} chunks ready")

    # 3. Show first few chunks
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n🧩 Chunk {i+1}:\n{chunk.page_content[:500]}\n{'-'*50}")

    # 4. Embedding model
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    # 5. Connect to Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if INDEX_NAME not in pc.list_indexes().names():
        print(f"🔧 Creating index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSIONS,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
        )
    else:
        print(f"✅ Index '{INDEX_NAME}' already exists.")

    # 6. Store chunks in Pinecone
    vectorstore = LangChainPinecone.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME,
        namespace=NAMESPACE
    )
    print("✅ Documents embedded and stored in Pinecone.")

if __name__ == "__main__":
    embed_and_store_all()
