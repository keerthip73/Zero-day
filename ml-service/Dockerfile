FROM python:3.13-slim

WORKDIR /app
COPY ml-service/requirements.txt ./ml-service/requirements.txt
RUN pip install --no-cache-dir -r ml-service/requirements.txt

COPY ml-service ./ml-service
COPY data ./data
COPY models ./models
COPY scripts ./scripts

ENV PYTHONPATH=/app/ml-service
RUN python scripts/prepare_data.py && python scripts/train_baseline.py
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--app-dir", "ml-service", "--host", "0.0.0.0", "--port", "8000"]
