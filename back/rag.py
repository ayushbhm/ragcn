import os

from langchain_community.vectorstores import Chroma
from ingest import chroma_client, embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def get_rag_chain(session_id):
    vectorstore = Chroma(
        client=chroma_client,
        collection_name=session_id,
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    
    prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below. If the answer isn't in the context, say so.

Context: {context}

Question: {question}
""")
    llm = ChatGoogleGenerativeAI(
        model = "gemini-3.1-flash-lite",
        google_api_key=os.environ.get("GEMINI_API_KEY")
    )
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        |prompt
        |llm
        |StrOutputParser()
    )
    return chain
    
    
    