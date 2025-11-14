FROM python:3.10-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY app.py .
COPY .env.example .env
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/


RUN mkdir -p data chroma_db


EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:80/status')"

 
    
CMD ["python", "app.py"]
