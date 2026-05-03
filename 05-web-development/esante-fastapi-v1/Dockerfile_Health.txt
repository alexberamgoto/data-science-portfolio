# health-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
ENV AUTH_SECRET_KEY=change_me_in_prod
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
