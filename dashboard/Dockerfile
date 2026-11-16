
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 10000

CMD ["sh", "-c", "python -m streamlit run dashboard/app.py --server.address=0.0.0.0 --server.port=${PORT:-8501}"]
