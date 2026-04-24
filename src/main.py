import os
import json
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
    "gemini": "google/gemini-pro",
}


def build_model(model_name: str):
    return ChatOpenRouter(
        model=model_name,
        temperature=0,
        api_key=api_key,
    )


def invoke_agent(agent, prompt: str) -> str:
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    if result.get("messages"):
        return result["messages"][-1].content

    return str(result)


def create_agent(model_name: str, role_prompt: str):
    return create_deep_agent(
        model=build_model(model_name),
        system_prompt=role_prompt,
    )


PLANNING_PROMPT = """
You are the Planning Agent.

Your job:
- Analyze the debate topic.
- Define debate rules.
- Define evaluation criteria for the Judge Agent.
- Create a clear debate plan.

Output format:
[Plan]
- Topic Analysis:
- Debate Rules:
- Evaluation Criteria:
"""

PRO_PROMPT = """
You are the Pro Agent.

Your job:
- Argue in favor of the topic.
- Present at least 2 logical arguments.
- Use respectful and evidence-based reasoning.
- Do not attack the opposing side emotionally.

Output format:
[Pro Agent]
1. Argument:
   Reason:
2. Argument:
   Reason:
"""

CON_PROMPT = """
You are the Con Agent.

Your job:
- Argue against the topic.
- Present at least 2 logical arguments.
- Respond to the Pro Agent's main claims.
- Use respectful and evidence-based reasoning.

Output format:
[Con Agent]
1. Counterargument:
   Reason:
2. Counterargument:
   Reason:
"""

JUDGE_PROMPT = """
You are the Judge Agent.

Your job:
- Compare the Pro Agent and Con Agent outputs.
- Evaluate both sides based on:
  1. logical consistency
  2. strength of reasoning
  3. directness of rebuttal
  4. overall persuasiveness
- You MUST choose either PRO or CON.
- Do not remain neutral.

At the end, output exactly these two lines:
Final Decision: PRO or CON
Winning Reason: <1-2 sentences, under 40 words, explaining why that side was more persuasive>
"""

VERIFICATION_PROMPT = """
You are the Verification Agent.

Your job:
- Check whether the debate follows the plan.
- Check whether Pro and Con outputs both exist.
- Check whether Judge chose either PRO or CON.
- Check whether Winning Reason exists.
- Identify format or logic problems.

Output format:
[Verification]
- Pro exists:
- Con exists:
- Judge decision valid:
- Winning reason exists:
- Issues:
"""

GATE_PROMPT = """
You are the Gate Agent.

Your job:
- Decide whether the result should PASS or FAIL.
- PASS only if:
  1. Pro output exists
  2. Con output exists
  3. Judge selected PRO or CON
  4. Winning Reason exists
- Otherwise FAIL.

Output format:
Gate Status: PASS or FAIL
Gate Reason: <short reason>
"""

LOGGING_PROMPT = """
You are the Logging Agent.

Your job:
- Summarize what happened in this run.
- Record topic, model, final decision, and improvement points.

Output format:
[Logging]
- Topic:
- Model:
- Final Decision:
- Summary:
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


def run_pipeline(model_label: str, model_name: str, topic: str):
    print(f"\n=== Running {model_label} ({model_name}) ===")

    planning_agent = create_agent(model_name, PLANNING_PROMPT)
    pro_agent = create_agent(model_name, PRO_PROMPT)
    con_agent = create_agent(model_name, CON_PROMPT)
    judge_agent = create_agent(model_name, JUDGE_PROMPT)
    verification_agent = create_agent(model_name, VERIFICATION_PROMPT)
    gate_agent = create_agent(model_name, GATE_PROMPT)
    logging_agent = create_agent(model_name, LOGGING_PROMPT)

    plan = invoke_agent(
        planning_agent,
        f"Create a debate plan for this topic: {topic}"
    )

    pro_output = invoke_agent(
        pro_agent,
        f"""
Topic: {topic}

Debate Plan:
{plan}

Generate the Pro side argument.
"""
    )

    con_output = invoke_agent(
        con_agent,
        f"""
Topic: {topic}

Debate Plan:
{plan}

Pro Agent Output:
{pro_output}

Generate the Con side argument and rebuttal.
"""
    )

    judge_output = invoke_agent(
        judge_agent,
        f"""
Topic: {topic}

Debate Plan:
{plan}

Pro Agent Output:
{pro_output}

Con Agent Output:
{con_output}

Evaluate both sides and choose the more persuasive side.
"""
    )

    decision, reason = extract_decision_and_reason(judge_output)

    verification_output = invoke_agent(
        verification_agent,
        f"""
Topic: {topic}

Plan:
{plan}

Pro Agent Output:
{pro_output}

Con Agent Output:
{con_output}

Judge Agent Output:
{judge_output}
"""
    )

    gate_output = invoke_agent(
        gate_agent,
        f"""
Topic: {topic}

Verification Output:
{verification_output}

Judge Decision: {decision}
Winning Reason: {reason}
"""
    )

    logging_output = invoke_agent(
        logging_agent,
        f"""
Topic: {topic}
Model: {model_label} ({model_name})
Final Decision: {decision}
Winning Reason: {reason}

Plan:
{plan}

Pro:
{pro_output}

Con:
{con_output}

Judge:
{judge_output}

Verification:
{verification_output}

Gate:
{gate_output}
"""
    )

    full_report = f"""# Debate Report - {model_label}

## Topic
{topic}

## Planning Agent
{plan}

## Pro Agent
{pro_output}

## Con Agent
{con_output}

## Judge Agent
{judge_output}

## Verification Agent
{verification_output}

## Gate Agent
{gate_output}

## Logging Agent
{logging_output}
"""

    return {
        "model_label": model_label,
        "model_name": model_name,
        "plan": plan,
        "pro": pro_output,
        "con": con_output,
        "judge": judge_output,
        "verification": verification_output,
        "gate": gate_output,
        "log": logging_output,
        "decision": decision,
        "reason": reason,
        "report": full_report,
    }


def main():
    os.makedirs("artifacts", exist_ok=True)
    os.makedirs("docs", exist_ok=True)

    topic = input("주제를 입력하세요: ").strip()

    for iteration in range(2):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n===== Iteration {iteration + 1} =====")

        results = []

        for label, model_name in MODELS.items():
            try:
                result = run_pipeline(label, model_name, topic)
                results.append(result)
                save_text(f"artifacts/debate_{label}_iter{iteration + 1}.md", result["report"])

            except Exception as e:
                error_report = f"# Error Report - {label}\n\nModel: {model_name}\n\nError: {str(e)}\n"
                save_text(f"artifacts/debate_{label}_iter{iteration + 1}.md", error_report)

                results.append({
                    "model_label": label,
                    "model_name": model_name,
                    "decision": "ERROR",
                    "reason": str(e),
                    "report": error_report,
                })

        comparison_lines = [
            f"# Model Comparison Result - Iteration {iteration + 1}",
            "",
            f"Topic: {topic}",
            "",
        ]

        for r in results:
            comparison_lines.append(f"## {r['model_label']} ({r['model_name']})")
            comparison_lines.append(f"- Final Decision: {r['decision']}")
            comparison_lines.append(f"- Winning Reason: {r['reason']}")
            comparison_lines.append("")

        comparison_text = "\n".join(comparison_lines)
        save_text(f"artifacts/model_comparison_iter{iteration + 1}.md", comparison_text)
        save_text("artifacts/model_comparison.md", comparison_text)

        plan_text = f"""# Plan - Iteration {iteration + 1}

Topic: {topic}

System Framework:
1. Planning Agent
2. Execution Stage
   - Pro Agent
   - Con Agent
   - Judge Agent
3. Verification Agent
4. Gate Agent
5. Logging Agent

Models Tested:
{", ".join(MODELS.values())}
"""
        save_text("artifacts/plan.md", plan_text)

        verification_lines = [
            f"# Verification - Iteration {iteration + 1}",
            "",
            f"Topic: {topic}",
            "",
        ]

        all_valid = True

        for r in results:
            decision_valid = r["decision"] in ["PRO", "CON"]
            reason_valid = r["reason"] != "No clear reason found." and bool(r["reason"].strip())
            error_free = r["decision"] != "ERROR"

            if not (decision_valid and reason_valid and error_free):
                all_valid = False

            verification_lines.append(f"## {r['model_label']}")
            verification_lines.append(f"- Decision valid: {decision_valid}")
            verification_lines.append(f"- Winning reason present: {reason_valid}")
            verification_lines.append(f"- Error free: {error_free}")
            verification_lines.append("")

        verification_lines.append("## Overall")
        verification_lines.append(f"- PASS: {all_valid}")

        verification_text = "\n".join(verification_lines)
        save_text("artifacts/verification.md", verification_text)

        gate_data = {
            "status": "PASS" if all_valid else "FAIL",
            "reason": (
                "All models produced valid PRO/CON decisions with winning reasons."
                if all_valid
                else "Some models failed to produce a valid PRO/CON decision, winning reason, or returned an error."
            ),
            "criteria": [
                "Each model must output Final Decision as PRO or CON",
                "Each model must include Winning Reason",
                "No model should return ERROR",
            ],
            "model_results": {
                r["model_label"]: {
                    "model": r["model_name"],
                    "decision": r["decision"],
                    "reason": r["reason"],
                }
                for r in results
            },
            "timestamp": timestamp,
            "topic": topic,
            "iteration": iteration + 1,
        }

        with open("artifacts/gate.json", "w", encoding="utf-8") as f:
            json.dump(gate_data, f, ensure_ascii=False, indent=2)

        log_text = f"""
## Iteration {iteration + 1} - {timestamp}

### Input
- Topic: {topic}

### Model Results
"""

        for r in results:
            log_text += f"- {r['model_label']}: {r['decision']} | {r['reason']}\n"

        log_text += f"""
### Gate
- Status: {"PASS" if all_valid else "FAIL"}

### Problems Found
"""

        problems = []

        for r in results:
            if r["decision"] not in ["PRO", "CON"]:
                problems.append(f"- {r['model_label']} did not produce a valid PRO/CON decision.")
            if r["decision"] == "ERROR":
                problems.append(f"- {r['model_label']} returned an error: {r['reason']}")
            if r["reason"] == "No clear reason found.":
                problems.append(f"- {r['model_label']} did not provide a clear winning reason.")

        if problems:
            log_text += "\n".join(problems) + "\n"
        else:
            log_text += "- No major problems found.\n"

        log_text += """
### Next Improvement
- Strengthen Judge Agent output format if decisions are invalid.
- Replace unavailable model endpoints if model errors occur.
- Improve prompts if winning reasons are too vague.
"""

        append_log("docs/ralph-log.md", log_text)

        print("\n=== Model Comparison Result ===\n")
        print(comparison_text)


if __name__ == "__main__":
    main()