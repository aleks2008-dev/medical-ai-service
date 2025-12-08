FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app

# Default environment variables (can be overridden)
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434
ENV MODEL_NAME=llama3.2:3b
ENV MODEL_PROVIDER=ollama
ENV MODEL_TEMPERATURE=0
ENV LOG_LEVEL=INFO
ENV DEBUG=False

CMD ["python", "main.py"]