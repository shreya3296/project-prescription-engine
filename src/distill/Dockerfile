FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1 
ENV PIP_NO_CACHE_DIR=1 

RUN pip install pipenv==2023.11.15

WORKDIR /app

COPY Pipfile Pipfile.lock .
RUN pipenv sync --system

COPY bloom_distillation_v3.py .

ENTRYPOINT ["python", "/app/bloom_distillation_v3.py"]
