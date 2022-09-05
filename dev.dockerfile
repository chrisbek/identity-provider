FROM python:3.10
ARG MODE
ARG PROJECT_NAME
LABEL maintainer="Christopher Bekos <bekos.christopher@gmail.com>"
RUN mkdir -p /_config && \
    mkdir -p /$PROJECT_NAME
ENV PYTHONPATH /
RUN pip install --upgrade pip && \
  pip3 install poetry==1.1.10 && \
  apt-get update && apt-get install vim -y
RUN echo 'alias migrations=". /$PROJECT_NAME/scripts/migrations.sh"' >> ~/.bashrc


ARG DIR_WITH_MAIN
ARG NAME_OF_MAIN
ARG VARIABLE_NAME
ARG WORKER_CLASS
ARG WORKERS_PER_CORE
ARG MAX_WORKERS
ARG LIVE_RELOAD
ARG GRACEFUL_TIMEOUT
ARG TIMEOUT
ARG KEEP_ALIVE
ARG HOST
ARG PORT
ARG LOG_LEVEL
ARG RELOAD

ENV PROJECT_NAME=$PROJECT_NAME
ENV MODE=$MODE
ENV DIR_WITH_MAIN=$DIR_WITH_MAIN
ENV NAME_OF_MAIN=$NAME_OF_MAIN
ENV VARIABLE_NAME=$VARIABLE_NAME
ENV WORKER_CLASS=$WORKER_CLASS
ENV WORKERS_PER_CORE=$WORKERS_PER_CORE
ENV MAX_WORKERS=$MAX_WORKERS
ENV LIVE_RELOAD=$LIVE_RELOAD
ENV GRACEFUL_TIMEOUT=$GRACEFUL_TIMEOUT
ENV TIMEOUT=$TIMEOUT
ENV KEEP_ALIVE=$KEEP_ALIVE
ENV HOST=$HOST
ENV PORT=$PORT
ENV LOG_LEVEL=$LOG_LEVEL
ENV RELOAD=$RELOAD

WORKDIR /$PROJECT_NAME
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install && rm ./pyproject.toml ./poetry.lock