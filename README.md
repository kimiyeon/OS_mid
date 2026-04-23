## 1. 프로젝트 개요

본 프로젝트는 사용자가 제시한 논쟁적 주제에 대해,
멀티 에이전트 기반으로 구조화된 찬반 토론을 수행하고,
제3의 Judge Agent가 설득력을 평가하는 시스템이다.

전체 시스템은 교수님이 제시한
**Plan → Execution → Verification → Gate → Logging**
프레임워크를 기반으로 설계되었으며,

Execution 단계에서
찬성과 반대 입장을 맡은 에이전트들이 실제 토론을 수행하도록 구성하였다.

## 2. 핵심 아이디어

단일 AI의 자기 평가는 편향될 수 있다는 문제를 해결하기 위해,
역할이 분리된 멀티 에이전트 구조를 사용하였다.

- Pro Agent: 찬성 입장 주장
- Con Agent: 반대 입장 주장 및 반박
- Judge Agent: 양측의 논리성과 설득력을 평가
- Logging Agent: 모든 과정 기록

이를 통해 하나의 모델이 아닌,
**상호작용 기반 판단 구조**를 구현하였다.

## 3. 시스템 아키텍처

전체 시스템은 다음과 같은 단계로 구성된다:

1. **Plan**
   - 사용자 주제를 분석
   - 토론 구조 및 제약 조건 설정

2. **Execution**
   - Pro Agent: 찬성 주장 생성
   - Con Agent: 반대 주장 및 반박
   - Judge Agent: 토론 결과 평가

3. **Verification**
   - 형식 준수 여부 검사
   - 논리적 오류 및 누락 확인

4. **Gate**
   - 기준 충족 여부 판단
   - 미달 시 재실행

5. **Logging**
   - 각 단계 결과 기록
   - 반복 과정 및 개선 사항 저장

## 4. Execution 구조

Execution 단계에서는 다음과 같은 멀티 에이전트 토론이 수행된다:

- **Pro Agent**
  - 주제에 대해 찬성 입장에서 논리적 주장 생성

- **Con Agent**
  - 반대 입장에서 반박 및 논리 제시

- **Judge Agent**
  - 양측의 주장에 대해
    - 논리성
    - 근거의 타당성
    - 반박의 적절성
  을 기준으로 평가 및 최종 판단

이 구조는 실제 법정의
검사–변호인–판사 구조에서 영감을 받았다.

## 5. 실행 예시시

입력:
낙태는 허용되어야 하는가

출력:
- Pro Agent: 찬성 입장에서 논리적 주장 생성
- Con Agent: 반대 입장에서 반박 및 논리 제시
- Judge Agent: 양측의 설득력을 평가
- Final Decision: 더 설득력 있는 입장 선택

## 6. 결과 저장 구조

artifacts/
- plan.md
- debate.md
- verification.md
- gate.json

docs/
- ralph-log.md

## 7. 핵심 기여

- Plan–Execution–Verification–Gate 구조를 실제 멀티 에이전트 시스템에 적용
- Execution 단계에서 역할 기반 토론 구조 설계
- 단일 AI가 아닌 상호작용 기반 판단 구조 구현
- 반복 실행 및 로그 기반 개선 과정 기록