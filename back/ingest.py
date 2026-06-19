from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings
import tempfile
import os

def extract_text(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        loader = PyMuPDFLoader(tmp.name)
        docs = loader.load()
    os.unlink(tmp.name)
    return docs

def chunk_docs(docs):
    total_pages = docs[-1].metadata.get('total_pages', 1)
    if total_pages < 20:
        chunk_size = 500
        chunk_overlap = 50
    elif total_pages < 100:
        chunk_size = 1000
        chunk_overlap = 200
    else:
        chunk_size = 2000
        chunk_overlap = 400
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)

chroma_client = chromadb.EphemeralClient()
embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def embed_and_store(chunks, session_id):
    vectorstore = Chroma(
        client = chroma_client,
        collection_name = session_id,
        embedding_function=embeddings
        
    )
    vectorstore.add_documents(chunks)
   
