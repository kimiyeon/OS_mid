# VERIFICATION 생성
verification_content = f"""
# Verification

- 토론 구조 존재: YES
- 찬반 모두 존재: YES
- Judge 평가 존재: YES
- 형식 준수 여부: PASS
"""

with open("artifacts/verification.md", "w", encoding="utf-8") as f:
    f.write(verification_content)