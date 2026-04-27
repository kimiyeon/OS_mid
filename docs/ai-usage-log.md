# AI Usage Log

## 1. AI Usage (기록)

- ChatGPT를 사용하여 초기 코드 구조를 생성
  - multi-agent pipeline (Planning, Pro, Con, Judge, Verification, Gate, Logging)
- Dockerfile 및 requirements.txt 초안 생성
- pandas 기반 결과 분석 코드 생성

사용 프롬프트 예시:
- "multi-agent debate system을 python으로 구현해줘"
- "judge agent가 PRO/CON을 반드시 선택하도록 프롬프트 작성해줘"
- "pandas로 결과를 분석하는 코드 만들어줘"

---

## 2. Issues Found (문제 발견)

AI가 생성한 코드에서 다음과 같은 문제가 발생:

- indent 오류로 코드 실행 불가
- 일부 모델 API 오류 (Claude timeout, Gemini invalid model)
- Judge Agent 출력 형식 불일치
  → "Final Decision" 누락
- parsing 함수가 일부 출력에서 작동하지 않음
  → UNKNOWN 결과 발생

---

## 3. Fixes Applied (검증 및 수정)

문제를 해결하기 위해 다음과 같은 수정 수행:

- try/except 위치 수정 → 에러 처리 정상화
- Gemini 모델 제거 → invalid model 문제 해결
- Claude 모델 에러 처리 추가
- Judge prompt 강화:
  - 반드시 PRO/CON 선택하도록 수정
  - 출력 형식 강제
- parsing 함수 개선:
  - 다양한 출력 형식 처리 가능하도록 수정
- pandas 추가:
  - 모델 결과를 구조화 및 분석
- Ralph Mode 개선:
  - previous_log를 읽어 다음 iteration에 반영

---

## 4. Validation (검증 과정)

- 실행 결과를 artifacts 폴더에서 직접 확인:
  - model_comparison.md
  - decision_summary.csv
  - gate.json
- ralph-log.md를 통해 iteration별 변화 확인
- 각 모델이 PRO/CON을 정상적으로 출력하는지 검증

---

## 5. Understanding (이해)

다음 내용을 직접 이해하고 설명 가능:

- multi-agent 구조:
  Planning → Pro/Con → Judge → Verification → Gate → Logging
- Docker 동작 원리:
  - Python 환경 고정
  - 동일한 실행 환경 제공
- OpenRouter를 통한 다중 모델 호출 방식
- pandas를 이용한 결과 분석 구조

---

## 6. Reflection (결론)

AI는 초기 코드 생성과 구조 설계에 매우 유용했지만,
출력의 정확성과 안정성을 위해서는
사람의 검증과 수정이 필수적이었다.

특히 모델별 출력 형식 차이와 API 오류를 처리하는 과정에서
AI 코드의 한계를 확인할 수 있었다.