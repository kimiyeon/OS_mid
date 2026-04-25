FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY PROMPT.md .
COPY docs/ ./docs

RUN mkdir -p artifacts

CMD ["python", "src/main.py"]