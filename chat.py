from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings 
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client= OpenAI()
def chat_with_pdf(query):
    # Fix: Remove 'client=' and just configure
    # Vector Embeddings
    embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
    )
    # vector database
    vector_db = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name="Learning_vectors",
        embedding=embeddings
    )

    

    # vector search in existing database
    search_results = vector_db.similarity_search(
        query=query,
        k=3  # Limit to top 3 results
    )

    print(f"Found {len(search_results)} relevant documents")

    # Create context from search results
    context = "\n\n".join([
        f"Page Number: {result.metadata.get('page', 'N/A')}\n"
        f"File Location: {result.metadata.get('source', 'N/A')}\n"
        f"Page Content:\n{result.page_content}"
        for result in search_results
]   )

    # Fix: Use f-string to properly include context and query
    system_prompt = f"""
    You are an intelligent AI agent.
    You give answers to user queries with page numbers and answer them beautifully.

    You should only answer user query based on the provided context and also navigate user to page number to know more.

    Context:
    {context}

    User Question: {query}

    Please provide a helpful answer with page references:
    """

    chat_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": query },
    ]
    )
    return chat_completion.choices[0].message.content
