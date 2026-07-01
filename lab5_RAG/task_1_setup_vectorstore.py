#!/usr/bin/env python3

import os
from dotenv import load_dotenv

# LangChain Chroma Wrapper
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

# OpenAI Embeddings
from langchain_openai import OpenAIEmbeddings

load_dotenv()

print("🔧 Task 1: Setting up Vector Store for RAG")
print("=" * 50)

# Initialize OpenAI Embedding Model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

print("✅ Embedding model loaded")

# Let LangChain manage ChromaDB
vectorstore = Chroma(
    collection_name="techcorp_rag",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

print("✅ Chroma vector store initialized")

# Test embedding
test_text = "Testing RAG setup"

test_embedding = embeddings.embed_query(test_text)

print(f"✅ Test embedding created: {len(test_embedding)} dimensions")

print("\n🎉 SUCCESS! Your vector store is ready for RAG!")
print(f"   - Collection: techcorp_rag")
print(f"   - Persist Directory: ./chroma_db")
print(f"   - Embedding Model: text-embedding-3-small")
print(f"   - Vector Dimensions: {len(test_embedding)}")
print("=" * 50)