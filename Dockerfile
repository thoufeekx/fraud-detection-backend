FROM python:3.10-slim

WORKDIR /app

COPY . .

# Set the PYTHONPATH to the app directory for module resolution
ENV PYTHONPATH=/app


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
