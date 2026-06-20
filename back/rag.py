import os
from langchain_chroma import Chroma
from ingest import chroma_client, embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_compressors import FlashrankRerank

from langchain_classic.retrievers import ContextualCompressionRetriever

def get_rag_chain(session_id):
    vectorstore = Chroma(
        client=chroma_client,
        collection_name=session_id,
        embedding_function=embeddings
    )
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
    compressor = FlashrankRerank(top_n=5)
    retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )

    prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below. Prioritize direct definitions over secondary mentions.

Context: {context}

Question: {question}
""")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.environ.get("GEMINI_API_KEY")
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
