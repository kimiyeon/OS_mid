import os
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_openrouter import ChatOpenRouter

load_dotenv()

model = ChatOpenRouter(
    model="openai/gpt-4o-mini",  # 테스트용 (나중에 바꿔도 됨)
    temperature=0
)

agent = create_deep_agent(
    model=model,
    system_prompt="""
You are a structured debate agent.

For any topic, generate:
1. Plan
2. Execution (Pro/Con)
3. Verification
4. Gate
5. Logging summary
"""
)

topic = input("주제를 입력하세요: ")

result = agent.invoke({
    "messages": [
        {"role": "user", "content": f"Create a structured pro-con debate about: {topic}"}
    ]
})

print(result)