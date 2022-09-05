ARG MODE
FROM python:3.9.5 as fast_api_base
LABEL maintainer="Christopher Bekos <bekos.christopher@gmail.com>"
RUN mkdir -p /_config && \
    mkdir -p /$PROJECT_NAME
WORKDIR /$PROJECT_NAME
ENV PYTHONPATH=/
COPY ./server/start_prod.sh ./server/start_dev.sh ./server/start.sh /_config/
RUN chmod +x /_config/start_prod.sh \
    && chmod +x /_config/start_dev.sh \
    && chmod +x /_config/start.sh

FROM fast_api_base AS fast_api_DEV
RUN pip3 install --no-cache-dir "uvicorn[standard]" pipenv && \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc libssl-dev
RUN export WORKON_HOME="/${PROJECT_NAME}/.venv" && \
    echo "source \$(pipenv --venv)/bin/activate" >> /root/.bashrc

#FROM fast_api_base AS fast_api_PROD
#RUN pip3 install --no-cache-dir "uvicorn[standard]" gunicorn && \
#    pip3 install pipenv && \
#    apt-get update && \
#    apt-get install -y --no-install-recommends gcc libssl-dev

FROM fast_api_${MODE} as fast_api_final
ARG PROJECT_NAME
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


