# #!/usr/bin/env python3
# """
# 🧠 Task 1: Embeddings - Teaching Computers to Understand Meaning
# """
#
# import os
# from sentence_transformers import SentenceTransformer, util
#
# def main():
#     # TODO 1: Initialize model that converts text → meaningful numbers
#     # Replace ___ with: "all-MiniLM-L6-v2"
#     model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
#
#     # Scenario: User searching documentation
#     query = "forgot my password"
#
#     docs = [
#         "Password recovery: Use the 'Reset Password' link on login page",
#         "Vacation policy: Request time off 2 weeks in advance",
#         "Account security: Enable two-factor authentication",
#         "Login help: Contact IT if you cannot access your account"
#     ]
#
#     # TODO 2: Convert query and docs to embeddings
#     # Replace ___ with: model.encode(query)
#     query_emb = model.encode(query)
#     # Replace ___ with: model.encode(docs)
#     doc_embs = model.encode(docs)
#
#     # TODO 3: Find semantic matches
#     # Replace ___ with: util.cos_sim(query_emb, doc_embs)[0]
#     scores = util.cos_sim(query_emb, doc_embs)[0]
#
#     print(f"Query: '{query}'\n")
#     print("Results (score > 0.3 = relevant):")
#     for doc, score in zip(docs, scores):
#         marker = "✅" if score > 0.3 else "  "
#         print(f"{marker} [{score:.2f}] {doc}")
#
#     print("\n💡 Notice: Found 'Password recovery' and 'Login help'")
#     print("   Even though query didn't contain those exact words!")
#
#     os.makedirs("/Users/songwen", exist_ok=True)
#     open("/Users/songwen/task1_embeddings_complete.txt", "w").write("DONE")
#
# if __name__ == "__main__":
#     main()

# !/usr/bin/env python3
"""
🧠 Task 1: Embeddings - Teaching Computers to Understand Meaning (OpenAI Version)
"""
"""
原来的教程代码模型引用改成我这个API支持OpenAI的text-embedding
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()


def calculate_similarity(v1, v2):
    """
    计算两个向量的余弦相似度。
    由于 OpenAI 的向量已经过 L2 归一化，余弦相似度在数学上等价于两个向量的点积。
    """
    return sum(a * b for a, b in zip(v1, v2))


def main():
    # TODO 1: Initialize OpenAI client
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE")
    )

    # 定义要使用的 OpenAI 向量模型
    EMBEDDING_MODEL = "text-embedding-3-small"

    # Scenario: User searching documentation
    query = "forgot my password"

    docs = [
        "Password recovery: Use the 'Reset Password' link on login page",
        "Vacation policy: Request time off 2 weeks in advance",
        "Account security: Enable two-factor authentication",
        "Login help: Contact IT if you cannot access your account"
    ]

    print("🔄 Calling OpenAI API to generate embeddings...")

    # TODO 2: Convert query and docs to embeddings via OpenAI API
    # 1. 获取 Query 的向量
    query_response = client.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL
    )
    query_emb = query_response.data[0].embedding

    # 2. 批量获取 Docs 的向量 (OpenAI 支持传入列表，一次性返回多个向量)
    docs_response = client.embeddings.create(
        input=docs,
        model=EMBEDDING_MODEL
    )
    doc_embs = [item.embedding for item in docs_response.data]

    # TODO 3: Find semantic matches
    # 计算 Query 向量与每一个 Doc 向量的相似度得分
    scores = [calculate_similarity(query_emb, doc_emb) for doc_emb in doc_embs]

    print(f"\nQuery: '{query}'\n")
    print("Results (score > 0.3 = relevant):")

    # 遍历并打印结果
    for doc, score in zip(docs, scores):
        marker = "✅" if score > 0.3 else "  "
        print(f"{marker} [{score:.2f}] {doc}")

    print("\n💡 Notice: Found 'Password recovery' and 'Login help'")
    print("   Even though query didn't contain those exact words!")

    # 创建打卡文件
    os.makedirs("/Users/songwen", exist_ok=True)
    with open("/Users/songwen/task1_embeddings_complete.txt", "w") as f:
        f.write("DONE_WITH_OPENAI")


if __name__ == "__main__":
    main()