# PLAN 생성
plan_content = f"""
# Plan

Topic: {topic}

Rules:
- Pro/Con 모두 존재
- 각 최소 2개 논거
- Judge 평가 필수
- 감정적 표현 최소화

Structure:
1. Pro 주장
2. Con 반박
3. Judge 평가
"""

with open("artifacts/plan.md", "w", encoding="utf-8") as f:
    f.write(plan_content)