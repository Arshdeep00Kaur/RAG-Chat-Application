from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

def run_indexing(uploaded_pdf_path):
    loader=PyPDFLoader(file_path=uploaded_pdf_path)
    doc=loader.load()    # pdf read

    # chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
    split_doc = text_splitter.split_documents(documents=doc)

    #vector embedding
    embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
    )

    # vector database
    vector_store = QdrantVectorStore.from_documents(
        documents=split_doc,
        url="http://localhost:6333",
        collection_name="Learning_vectors",
        embedding=embeddings,
        force_recreate=True
    )
    







