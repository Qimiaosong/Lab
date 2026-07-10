#!/usr/bin/env python3
"""Task 2: MCP and LangGraph Integration - Connecting MCP servers to agents"""

import os
import asyncio
from typing import TypedDict
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# ╔════════════════════════════════════════╗
# ║   MCP + LangGraph Integration Flow     ║
# ╚════════════════════════════════════════╝
#
#        [User Query]
#             │
#             ▼
#     ┌───────────────┐
#     │ LangGraph     │
#     │ React Agent   │
#     └───────┬───────┘
#             │
#       ┌─────┴─────┐
#       │MCP Client │
#       └─────┬─────┘
#             │
#       ┌─────┴─────┐
#       ▼           ▼
# ┌──────────┐ ┌─────────┐
# │MCP Server│ │   LLM   │
# │Calculator│ │Response │
# │   🔢     │ │   💬    │
# └──────────┘ └─────────┘
#
# MCP Tool Naming Convention:
# When tools are loaded, they follow pattern:
# Original: add, multiply
# In Agent: Automatically handled by MCP adapter

load_dotenv()
print("🔌 Task 2: MCP and LangGraph Integration\n")

# Import MCP adapter components
try:
    from langchain_mcp_adapters.client import MultiServerMCPClient
except ImportError:
    print("⚠️ Creating mock MCP client for learning (install 'pip install langchain-mcp-adapters' for real)")

    # Mock implementation for learning
    class MultiServerMCPClient:
        def __init__(self, servers):
            self.servers = servers

        async def get_tools(self):
            """Mock tools from calculator server"""
            def mock_add(a: float, b: float) -> float:
                """Add two numbers"""
                return a + b

            def mock_multiply(a: float, b: float) -> float:
                """Multiply two numbers"""
                return a * b

            # Return mock tools
            return [mock_add, mock_multiply]

# Initialize the LLM
model = ChatOpenAI(
    model="gpt-4.1-mini",
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)


print("Building MCP-integrated agent:\n")

# TODO 1: Initialize MultiServerMCPClient
# Hint: Configure calculator server with stdio transport
"""
这里其实是在做服务发现的准备工作。你告诉客户端：“请通过 python 命令去执行 task_1_mcp_basics.py 脚本
（启动你在 Task 1 写好的那个不需要 LLM 的计算器服务器）然后通过stdio（标准输入输出）和它建立数据通道。”

它看到 command: "python" 和 args: ["/Users/.../task_1_mcp_basics.py"]。
它会在底层偷偷调用 Python 内置的 subprocess 模块，真的在后台为你新开了一个终端进程，
去运行 task_1 的脚本！然后它通过 transport: "stdio"，把你当前 task_2 进程的标准输入/输出，
和后台那个 task_1 进程的标准输入/输出管道连接起来，实现跨进程通信。
"""
client = MultiServerMCPClient(
    {
        "calculator": {  # Replace ___ with "calculator"
            "command": "python",
            # In production, use full path to your server
            "args": ["/Users/songwen/Lab/lab7_MCP/task_1_mcp_basics.py"],
            "transport": "stdio",
        }
    }
)

async def run_agent_with_mcp():
    """Create and run agent with MCP tools"""

    # TODO 2: Get tools from MCP client
    # Hint: Call client.get_tools()
    """
    当这行代码执行时，对应了你日志里的第一条记录：
    INFO Processing request of type ListToolsRequest
    MCP Client 发送了 tools/list 请求，把 Task 1 里 calculator 服务器上的
    add、multiply 等工具的说明书（JSON Schema）全部拉取到了本地内存中。
    """
    tools = await client.get_tools()  # Replace ___ with client.get_tools()

    # TODO 3: Create react agent with tools
    # Hint: Use create_agent with model and tools
    agent = create_agent(model, tools)  # Replace ___ with create_agent

    print("✅ Agent created with MCP tools!\n")
    print("=" * 60)
    print("TESTING MCP-INTEGRATED AGENT:")
    print("=" * 60)

    # Test 1: Math query (should use MCP tools)
    print("\nTest 1: Math Query")
    math_response = await agent.ainvoke({
        "messages": "What is 25 plus 17?"
    })
    print(f"Response: {math_response['messages'][-1].content}")

    # Test 2: Another math query
    print("\nTest 2: Multiplication Query")
    multiply_response = await agent.ainvoke({
        "messages": "Calculate 8 times 9"
    })
    print(f"Response: {multiply_response['messages'][-1].content}")

    # Test 3: Complex math
    print("\nTest 3: Complex Math")
    complex_response = await agent.ainvoke({
        "messages": "What's (3 + 5) x 12?"
    })
    print(f"Response: {complex_response['messages'][-1].content}")

    # Test 4: Non-math query
    print("\nTest 4: Non-Math Query")
    general_response = await agent.ainvoke({
        "messages": "What is the capital of France?"
    })
    print(f"Response: {general_response['messages'][-1].content}")

# Run the agent
if __name__ == "__main__":
    print("Starting MCP + LangGraph integration...")

    # Run async function
    asyncio.run(run_agent_with_mcp())

    print("\n" + "=" * 60)
    print("💡 KEY CONCEPTS:")
    print("- MultiServerMCPClient connects to MCP servers")
    print("- client.get_tools() loads tools from servers")
    print("- create_react_agent builds agent with tools")
    print("- Agent automatically routes to appropriate tools")
    print("- MCP handles tool execution transparently")
    print("=" * 60)

    # Create marker file
    os.makedirs("/Users/songwen", exist_ok=True)
    with open("/Users/songwen/task2_integration_complete.txt", "w") as f:
        f.write("TASK2_COMPLETE")