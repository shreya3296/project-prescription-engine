FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1 
ENV PIP_NO_CACHE_DIR=1 

RUN pip install pipenv==2023.11.15

WORKDIR /app

COPY Pipfile Pipfile.lock .
RUN pipenv sync --system

COPY embeddings_biobert_harmonized.py .
USER nobody

ENTRYPOINT ["python", "/app/embeddings_biobert_harmonized.py"]
