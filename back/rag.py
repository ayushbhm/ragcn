import os
from langchain_chroma import Chroma
from ingest import chroma_client, embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_compressors import FlashrankRerank
from langchain_core.runnables import RunnableLambda
from langchain_classic.retrievers import ContextualCompressionRetriever

def get_rag_chain(session_id):
    vectorstore = Chroma(
        client=chroma_client,
        collection_name=session_id,
        embedding_function=embeddings
    )
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 80})
    compressor = FlashrankRerank(top_n=10)
    retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )

    prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below.

If the conversation history helps interpret the current question,
use it. Otherwise ignore it.

Conversation History:
{history}

Context:
{context}

Question:
{question}
""")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.environ.get("GEMINI_API_KEY")
    )

    chain = (
    {
        "context": lambda x: retriever.invoke(x["question"]),
        "question": RunnableLambda(lambda x: x["question"]),
        "history": RunnableLambda(lambda x: x["history"])
    }
    | prompt
    | llm
    | StrOutputParser()
)

    return chain
