# from openai import OpenAI
#
#
# # 初始化客户端（替换成你的第三方API地址和Key）
# client = OpenAI(
#     base_url="https://xiaoai.plus/v1",
#     api_key="sk-ks7KvtvJ7LZo2FI2aFLjzgirJkJkxt638pSfxkpJPjFJkOhO"
# )
#
# # 发送请求
# completion = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Hello!"}
#     ]
# )
#
# # 打印返回结果
# print(completion.choices[0].message)

# 看这个中转站支持哪些模型
from openai import OpenAI

client = OpenAI(
    api_key="sk-ks7KvtvJ7LZo2FI2aFLjzgirJkJkxt638pSfxkpJPjFJkOhO",
    base_url="https://xiaoai.plus/v1"
)

models = client.models.list()

for model in models.data:
    print(model.id)


"""
claude-haiku-4-5-20251001
claude-haiku-4-5-20251001-thinking
claude-opus-4-1-20250805
claude-opus-4-1-20250805-thinking
claude-opus-4-20250514
claude-opus-4-20250514-thinking
claude-opus-4-5-20251101
claude-opus-4-5-20251101-thinking
claude-opus-4-6
claude-opus-4-7
claude-opus-4-7-thinking
claude-sonnet-4-20250514
claude-sonnet-4-20250514-thinking
claude-sonnet-4-5-20250929
claude-sonnet-4-5-20250929-thinking
claude-sonnet-4-6
claude-sonnet-4-6-thinking
dall-e-3
deepseek-chat
deepseek-r1
deepseek-r1-0528
deepseek-reasoner
deepseek-v3
deepseek-v3-0324
deepseek-v3.1
deepseek-v3.1-thinking
deepseek-v3.2
deepseek-v3.2-exp
deepseek-v3.2-exp-thinking
deepseek-v3.2-thinking
deepseek-v4-flash
deepseek-v4-flash-max
deepseek-v4-flash-none
gemini-2.5-flash
gemini-2.5-flash-image-preview
gemini-2.5-flash-lite
gemini-2.5-flash-nothinking
gemini-2.5-flash-thinking
gemini-2.5-pro
gemini-2.5-pro-nothinking
gemini-2.5-pro-thinking
gemini-3-flash-preview
gemini-3-flash-preview-thinking
gemini-3-pro-image-preview
gemini-3-pro-preview
gemini-3.1-flash-image-preview
gemini-3.1-flash-lite-preview
gemini-3.1-pro-preview
gemini-3.1-pro-preview-customtools
gpt-3.5-turbo
gpt-3.5-turbo-0125
gpt-3.5-turbo-1106
gpt-3.5-turbo-16k
gpt-3.5-turbo-16k-0613
gpt-4
gpt-4-0125-preview
gpt-4-0613
gpt-4-1106-preview
gpt-4-turbo
gpt-4-turbo-2024-04-09
gpt-4-vision-preview
gpt-4.1
gpt-4.1-2025-04-14
gpt-4.1-mini
gpt-4.1-mini-2025-04-14
gpt-4.1-nano
gpt-4.1-nano-2025-04-14
gpt-4o
gpt-4o-2024-05-13
gpt-4o-2024-08-06
gpt-4o-2024-11-20
gpt-4o-mini
gpt-4o-mini-2024-07-18
gpt-5
gpt-5-2025-08-07
gpt-5-chat
gpt-5-chat-latest
gpt-5-mini
gpt-5-mini-2025-08-07
gpt-5-nano
gpt-5-nano-2025-08-07
gpt-5-pro
gpt-5.1
gpt-5.1-2025-11-13
gpt-5.1-chat
gpt-5.1-chat-2025-11-13
gpt-5.2
gpt-5.2-2025-12-11
gpt-5.3-chat
gpt-5.4
gpt-5.5
gpt-image-1
gpt-image-2
o1
o1-2024-12-17
o1-mini
o1-mini-2024-09-12
o1-preview
o1-preview-2024-09-12
o3
o3-2025-04-16
o3-mini
o3-mini-2025-01-31
o3-mini-2025-01-31-high
o3-mini-2025-01-31-low
o3-mini-2025-01-31-medium
o3-mini-high
o3-mini-low
o3-mini-medium
o4-mini
o4-mini-2025-04-16
text-embedding-3-large
text-embedding-3-small
text-embedding-ada-002
tts-1
whisper-1
"""