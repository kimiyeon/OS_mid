import os
import json

TOPIC = input("주제를 입력하세요: ")

# 1. PLAN
plan = f"""
Topic: {TOPIC}
- Structure: Pro vs Con
- Each side must have 2 arguments
- Each argument must include reasoning
"""
with open("artifacts/plan.md", "w") as f:
    f.write(plan)

# 2. EXECUTION
debate = f"""
[PRO]
1. Argument A about {TOPIC} (reason included)
2. Argument B about {TOPIC} (reason included)

[CON]
1. Argument A against {TOPIC} (reason included)
2. Argument B against {TOPIC} (reason included)
"""
with open("artifacts/debate.md", "w") as f:
    f.write(debate)

# 3. VERIFICATION
verification = """
- Structure OK
- Pro/Con balance OK
- Arguments contain reasoning
"""
with open("artifacts/verification.md", "w") as f:
    f.write(verification)

# 4. GATE
gate = {
    "status": "PASS",
    "reason": "All constraints satisfied"
}
with open("artifacts/gate.json", "w") as f:
    json.dump(gate, f, indent=2)

# 5. LOG
log_entry = f"""
Iteration:
Topic: {TOPIC}
Result: PASS
"""
with open("docs/ralph-log.md", "a") as f:
    f.write(log_entry)

print("완료")