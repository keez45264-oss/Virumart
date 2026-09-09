# Phase 3: containerize the app
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["sh", "-c", "python db_init.py && python run.py"]