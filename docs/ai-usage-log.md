# AI Usage Log

## 1. AI Usage

- ChatGPT를 사용하여 main.py 초기 구조 생성
- Dockerfile 및 requirements.txt 생성

## 2. Issues Found

- AI가 생성한 코드에서 indent 오류 발생
- 일부 모델에서 API 에러 발생
- Judge Agent가 출력 형식을 지키지 않음

## 3. Fixes Applied

- try/except 위치 수정
- Gemini 모델 제거
- parsing 함수 개선
- Judge prompt 강화

## 4. Reflection

AI는 빠른 코드 생성을 도와주었지만, 
출력의 정확성과 안정성을 위해 수동 수정이 필요했다.