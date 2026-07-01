# #!/usr/bin/env python3
# """
# Task 5: Complete RAG Pipeline
# Wire everything together - Retrieve, Augment, Generate!
# """
#
# import os
# import chromadb
# # from sentence_transformers import SentenceTransformer
# from langchain_openai import OpenAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_openai import ChatOpenAI
#
# print("🚀 Task 5: Complete RAG Pipeline")
# print("=" * 50)
#
# # Initialize all components
# # client_db = chromadb.PersistentClient(path="./chroma_db")
# # collection = client_db.get_or_create_collection("techcorp_rag")
# # model = SentenceTransformer("all-MiniLM-L6-v2")
#
#
#
# api_base = os.getenv("OPENAI_API_BASE")
# api_key = os.getenv("OPENAI_API_KEY")
# client_llm = ChatOpenAI(
#     api_key=api_key,
#     base_url=api_base,
#     model="gpt-4.1-mini",
#     temperature=0.3,
#     max_tokens=500
# )
#
# print("✅ All components loaded")
#
# def rag_pipeline(user_question):
#     """Complete RAG pipeline: Retrieve → Augment → Generate"""
#
#     print(f"\n📝 Question: '{user_question}'")
#     print("-" * 50)
#
#     # Step 1: RETRIEVE
#     print("1️⃣ RETRIEVE: Converting to embedding...")
#     query_embedding = model.encode(user_question).tolist()
#
#     # TODO 1: Perform semantic search to find relevant chunks
#     # Hint: Use collection.query(query_embeddings=[...], n_results=3)
#     results = collection.query(
#         query_embeddings=[___],  # Replace ___ with query_embedding
#         n_results=___  # Replace ___ with 3
#     )
#
#     retrieved_chunks = results['documents'][0]
#     metadatas = results['metadatas'][0]
#
#     print(f"   ✅ Retrieved {len(retrieved_chunks)} relevant chunks")
#     for i, meta in enumerate(metadatas):
#         print(f"      - {meta['source']} ({meta['section']})")
#
#     # Step 2: AUGMENT
#     print("\n2️⃣ AUGMENT: Building context...")
#
#     # TODO 2: Define system prompt for context-aware answers
#     # Hint: Already complete - review the prompt below
#     system_prompt = """You are TechCorp's helpful AI assistant.
# Answer ONLY based on the provided context.
# If the answer is not in the context, say: 'I don't have that information in the provided documents.'"""
#
#     context_text = "Context from TechCorp documents:\n\n"
#     for i, chunk in enumerate(retrieved_chunks, 1):
#         context_text += f"[Document {i}]\n{chunk}\n\n"
#
#     # TODO 3: Complete the user prompt with question
#     # Hint: Add user_question after "Question:"
#     user_prompt = f"{context_text}\nQuestion: {___}\n\nAnswer:"  # Replace ___ with user_question
#
#     print("   ✅ Context prepared with retrieved documents")
#
#     # Step 3: GENERATE
#     print("\n3️⃣ GENERATE: Creating answer...")
#
#     # TODO 4: Create messages for LLM with system and user prompts
#     # Hint: Use system_prompt and user_prompt
#     messages = [
#         {"role": "system", "content": ___},  # Replace ___ with system_prompt
#         {"role": "user", "content": ___}     # Replace ___ with user_prompt
#     ]
#
#     response = client_llm.invoke(messages)
#     answer = response.content
#
#     # TODO 5: Format response with source citations
#     # Hint: Use ', '.join(unique_sources) to list sources
#     sources = [meta['source'] for meta in metadatas]
#     unique_sources = list(set(sources))
#
#     final_response = f"{answer}\n\n📎 Sources: {', '.join(___)}"  # Replace ___ with unique_sources
#
#     return final_response
#
# # Test the complete pipeline
# def test_rag_pipeline():
#     """Test with sample questions"""
#
#     test_questions = [
#         "Can I bring my dog to the office?",
#         "How many vacation days do I get?",
#         "What is the remote work policy?"
#     ]
#
#     for question in test_questions:
#         answer = rag_pipeline(question)
#         print("\n" + "=" * 50)
#         print("💬 ANSWER:")
#         print(answer)
#         print("=" * 50)
#
# # Run the test
# try:
#     # First ensure we have documents in the database
#     if collection.count() == 0:
#         print("\n⚠️ No documents in database. Please run Task 2 first!")
#     else:
#         print(f"\n📚 Database has {collection.count()} chunks ready")
#         test_rag_pipeline()
#
#         print("\n" + "=" * 50)
#         print("🎉 RAG Pipeline Complete!")
#         print("   - Retrieval: Semantic search working")
#         print("   - Augmentation: Context injection ready")
#         print("   - Generation: LLM producing answers")
#         print("   - Citations: Sources included")
#         print("=" * 50)
#
#         # Create marker file
#         # os.makedirs("/root/markers", exist_ok=True)
#         # with open("/root/markers/task5_rag_complete.txt", "w") as f:
#         #     f.write("TASK5_COMPLETE:RAG_PIPELINE_READY")
#
# except Exception as e:
#     print(f"\n❌ Error: {e}")
#
# print("\n🎯 You've built a complete RAG system - from search to answers!")
# print("\n✅ Task 5 completed!")

#!/usr/bin/env python3
"""
Task 5: Complete RAG Pipeline
Wire everything together - Retrieve, Augment, Generate!
"""

# 这段代码实现了一个完整的RAG pipeline。首先利用OpenAIEmbeddings将用户问题向量化，
# 并通过Chroma向量数据库执行相似度检索获取Top-K相关文档；
# 然后将检索到的文档拼接到Prompt中形成上下文(Argumentation);
# 最后将System Prompt和User Prompt发送给ChatOpenAI完成答案生成(Generation)。
# 相比于原始实现方法，使用LangChain的Chroma vectorstore和OpenAIEMbeddings封装，
# 省去了手动生成Query Embedding和调用collection.query的步骤，
# 使代码更加符合生产环境中的RAG开发模式。
import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma

load_dotenv()

print("🚀 Task 5: Complete RAG Pipeline")
print("=" * 50)

# =========================
# OpenAI Config
# =========================

api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_API_KEY")

# =========================
# Embedding Model
# =========================

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key,
    base_url=api_base
)

# =========================
# Chroma Vector Store
# =========================

vectorstore = Chroma(
    collection_name="techcorp_rag",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# =========================
# LLM
# =========================

client_llm = ChatOpenAI(
    api_key=api_key,
    base_url=api_base,
    model="gpt-4.1-mini",
    temperature=0.3,
    max_tokens=500
)

print("✅ All components loaded")


def rag_pipeline(user_question):
    """
    Complete RAG pipeline:
    Retrieve → Augment → Generate
    """

    print(f"\n📝 Question: '{user_question}'")
    print("-" * 50)

    # ==========================================
    # 1️⃣ RETRIEVE
    # ==========================================

    print("1️⃣ RETRIEVE: Searching vector database...")

    # Chroma + OpenAIEmbeddings 自动完成：
    # query -> embedding -> similarity search

    results = vectorstore.similarity_search(
        query=user_question,
        k=3
    )

    retrieved_chunks = [doc.page_content for doc in results]
    metadatas = [doc.metadata for doc in results]

    print(f"   ✅ Retrieved {len(retrieved_chunks)} relevant chunks")

    for i, meta in enumerate(metadatas, 1):
        source = meta.get("source", "unknown")
        section = meta.get("section", "unknown")

        print(f"      {i}. {source} ({section})")

    # ==========================================
    # 2️⃣ AUGMENT
    # ==========================================

    print("\n2️⃣ AUGMENT: Building context...")

    system_prompt = """
You are TechCorp's helpful AI assistant.

Answer ONLY based on the provided context.

If the answer is not in the context, say:
"I don't have that information in the provided documents."
"""

    context_text = "Context from TechCorp documents:\n\n"

    for i, chunk in enumerate(retrieved_chunks, 1):
        context_text += f"[Document {i}]\n{chunk}\n\n"

    user_prompt = f"""
{context_text}

Question:
{user_question}

Answer:
"""

    print("   ✅ Context prepared with retrieved documents")

    # ==========================================
    # 3️⃣ GENERATE
    # ==========================================

    print("\n3️⃣ GENERATE: Creating answer...")

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = client_llm.invoke(messages)

    answer = response.content

    # ==========================================
    # Source Citations
    # ==========================================

    sources = [
        meta.get("source", "unknown")
        for meta in metadatas
    ]

    unique_sources = list(set(sources))

    final_response = (
        f"{answer}\n\n"
        f"📎 Sources: {', '.join(unique_sources)}"
    )

    return final_response


# ==========================================
# Test the complete pipeline
# ==========================================

def test_rag_pipeline():

    test_questions = [
        "Can I bring my dog to the office?",
        "How many vacation days do I get?",
        "What is the remote work policy?"
    ]

    for question in test_questions:

        answer = rag_pipeline(question)

        print("\n" + "=" * 50)
        print("💬 ANSWER:")
        print(answer)
        print("=" * 50)


# ==========================================
# Run
# ==========================================

try:

    collection = vectorstore._collection

    if collection.count() == 0:

        print("\n⚠️ No documents in database.")
        print("Please run Task 2 first!")

    else:

        print(f"\n📚 Database has {collection.count()} chunks ready")

        test_rag_pipeline()

        print("\n" + "=" * 50)
        print("🎉 RAG Pipeline Complete!")
        print("   - Retrieval: Semantic search working")
        print("   - Augmentation: Context injection ready")
        print("   - Generation: LLM producing answers")
        print("   - Citations: Sources included")
        print("=" * 50)

except Exception as e:

    print(f"\n❌ Error: {e}")

print("\n🎯 You've built a complete RAG system - from search to answers!")
print("\n✅ Task 5 completed!")