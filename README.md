# PDF RAG Assistant

A  RAG assistant chatbot for both large PDFs and small page documents. Adaptive chunking and two-stage retrieval improve answers on long documents, while conversation history keeps follow-up questions in context.
## Design Choices Worth Noting

- **Adaptive chunking** — Chunk size and overlap scale with document length (500/50 for short PDFs, up to 2000/400 for 100+ page documents). This prevents over-fragmentation on small documents while preserving context in larger ones.
- **Two-stage retrieval** — A wide similarity search retrieves the top 80 candidate chunks, then a FlashRank cross-encoder reranks them to the top 10. This significantly improves retrieval quality on large documents where plain top-k vector search often returns loosely related chunks.
- **Multilingual embeddings** — Handles Hindi and English PDFs without language detection or branching logic.
- **Per-session isolated vector stores** — Every uploaded PDF gets its own ephemeral Chroma collection, preventing context leakage across users or documents.
- **Stateless API** — Conversation history is sent with every request instead of being stored in server memory, making the backend easier to scale.

## Tech Stack

- Vue 3
- Flask
- LangChain
- ChromaDB
- Gemini 2.5 Flash

## Pipeline

```text
PDF
  │
  ▼
Text Extraction
  │
  ▼
Adaptive Chunking
  │
  ▼
Embeddings
  │
  ▼
Per-Session Vector Store (ChromaDB)
  │
  ▼
Question + Conversation History
  │
  ▼
Retrieve Top 80 Chunks
  │
  ▼
FlashRank Reranking
  │
  ▼
Top 10 Chunks
  │
  ▼
Gemini 2.5 Flash
  │
  ▼
Answer
```
