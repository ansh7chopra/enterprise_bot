# utils/rag_search.py
import os
from langchain_pinecone import Pinecone as LangChainPinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.tools import Tool 

INDEX_NAME = "bot"
NAMESPACE  = "company-docs"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_embedder  = HuggingFaceEmbeddings(model_name=MODEL_NAME)
_vectorstore = LangChainPinecone.from_existing_index(
    index_name=INDEX_NAME,
    embedding=_embedder,
    namespace=NAMESPACE,
)

_llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

_rag_chain = RetrievalQA.from_chain_type(
    llm=_llm,
    retriever=_vectorstore.as_retriever(search_kwargs={"k": 8}),
    return_source_documents=False,
)
# @tool
def enterprise_search_tool(query: str) -> str:
    """Answer company-related queries using RAG search over internal documents."""
    return enterprise_search_tool(query)

enterprise_search_tool = Tool(
    name="CompanySearch",
    func=lambda q: _rag_chain.run(q),
    description="Use this tool to answer questions about the company using internal documents. Input should be a fully formed question."
)
