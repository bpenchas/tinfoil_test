FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Download the model at build time so it's baked into the image
ARG MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0
RUN python -c "from transformers import pipeline; pipeline('text-generation', model='${MODEL_NAME}')"

ENV MODEL_NAME=${MODEL_NAME}
EXPOSE 8000
CMD ["python", "app.py"]
