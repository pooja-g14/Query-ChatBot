# Query-ChatBot

Features:
- Uses RAG to fetch the DB schema from the VectorDB based on the user's question
- Uses LLM to generate SQL queries from the fetched schema and the user's question
- Uses PostgreSQL to execute queries
- Uses LLM to craft human-readable responses

LLM - Open Source HF Model 
Embeddings - Open Source HF Model
VectorDB - Qdrant Cloud (Free tier)
