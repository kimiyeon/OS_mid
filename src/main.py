import os
from datetime import datetime
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_openrouter import ChatOpenRouter

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY must be set in .env")

MODELS = {
    "gpt4o_mini": "openai/gpt-4o-mini",
    "claude_haiku": "anthropic/claude-3-haiku",
    "gemini_flash": "google/gemini-pro"
}

SYSTEM_PROMPT = """
You are a structured multi-agent debate system.

Follow this framework:
1. Plan
2. Execution
3. Verification
4. Gate
5. Logging

Execution stage must contain:
- Pro Agent: argues in favor of the motion
- Con Agent: argues against the motion
- Judge Agent: evaluates both sides and decides which side was more persuasive

Rules:
- Both Pro and Con must present at least 2 arguments
- Arguments should be logical and respectful
- No emotional attacks
- Judge must evaluate based on:
  1. logical consistency
  2. strength of reasoning
  3. directness of rebuttal
  4. overall persuasiveness

At the end, output MUST include exactly these two lines:

Final Decision: PRO or CON
Winning Reason: <1-2 sentences, under 40 words, explaining why that side was more persuasive>

Before the final decision, provide these sections:
[Plan]
[Execution]
[Verification]
[Gate]
"""

def extract_decision_and_reason(text: str):
    decision = "UNKNOWN"
    reason = "No clear reason found."

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Final Decision:"):
            decision = stripped.replace("Final Decision:", "").strip()
        elif stripped.startswith("Winning Reason:"):
            reason = stripped.replace("Winning Reason:", "").strip()

    return decision, reason

def save_text(path: str, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def append_log(path: str, content: str):
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)

def run_model(model_label: str, model_name: str, topic: str):
    print(f"\n=== Running {model_label} ({model_name}) ===")

    model = ChatOpenRouter(
        model=model_name,
        temperature=0,
        api_key=api_key,
    )

    agent = create_deep_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
    )

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"Create a structured pro-con debate about: {topic}"
            }
        ]
    })

    final_output = ""
    if result.get("messages"):
        final_output = result["messages"][-1].content
    else:
        final_output = str(result)

    decision, reason = extract_decision_and_reason(final_output)

    return {
        "model_label": model_label,
        "model_name": model_name,
        "output": final_output,
        "decision": decision,
        "reason": reason,
    }

def main():
    os.makedirs("artifacts", exist_ok=True)
    os.makedirs("docs", exist_ok=True)

    topic = input("주제를 입력하세요: ").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    results = []

    for label, model_name in MODELS.items():
        try:
            result = run_model(label, model_name, topic)
            results.append(result)

            save_text(
                f"artifacts/debate_{label}.md",
                result["output"]
            )

        except Exception as e:
            error_text = f"Model: {label}\nError: {str(e)}"
            save_text(f"artifacts/debate_{label}.md", error_text)
            results.append({
                "model_label": label,
                "model_name": model_name,
                "output": error_text,
                "decision": "ERROR",
                "reason": str(e),
            })

    comparison_lines = []
    comparison_lines.append("# Model Comparison Result")
    comparison_lines.append("")
    comparison_lines.append(f"Topic: {topic}")
    comparison_lines.append("")

    for r in results:
        comparison_lines.append(f"## {r['model_label']} ({r['model_name']})")
        comparison_lines.append(f"- Final Decision: {r['decision']}")
        comparison_lines.append(f"- Winning Reason: {r['reason']}")
        comparison_lines.append("")

    comparison_text = "\n".join(comparison_lines)
    save_text("artifacts/model_comparison.md", comparison_text)

    log_text = f"""
## {timestamp}
- Topic: {topic}
- Models tested: {", ".join(MODELS.keys())}
"""
    for r in results:
        log_text += f"- {r['model_label']}: {r['decision']} | {r['reason']}\n"

    append_log("docs/ralph-log.md", log_text)

    print("\n=== Model Comparison Result ===\n")
    print(comparison_text)


if __name__ == "__main__":
    main()