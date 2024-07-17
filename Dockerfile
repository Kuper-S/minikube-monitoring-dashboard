# Dockerfile
FROM python:3.8-slim

# Create a group and user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

CMD ["python", "app.py"]
