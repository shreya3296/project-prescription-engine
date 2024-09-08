FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1 
ENV PIP_NO_CACHE_DIR=1 

RUN pip install pipenv==2023.11.15

WORKDIR /app

COPY Pipfile Pipfile.lock .
RUN pipenv sync --system

# assuming that src is bind-mounted at /app
#COPY cli.py .
#USER nobody

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "/app/workflow/cli.py"]