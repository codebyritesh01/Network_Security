FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

RUN apt-get update && pip install --no-cache-dir -r requirements.txt

# Render provides the PORT environment variable
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]