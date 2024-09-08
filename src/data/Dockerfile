FROM python:3.8-slim-buster

ENV PIPENV_VENV_IN_PROJECT=1
ENV PYTHONUNBUFFERED=1 

RUN pip install --no-cache-dir pipenv==2023.10.3

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv sync --system

COPY extract_nhs_disease_data.py .
USER nobody

# data volume expected to be mounted here
VOLUME /app/data

ENTRYPOINT ["python", "/app/extract_nhs_disease_data.py"]
