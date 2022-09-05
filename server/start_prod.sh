#! /usr/bin/env sh
set -e

# Default settings are valid when the following file exists: fast_api_poc/app/main.py:
PROJECT_NAME=${PROJECT_NAME:-fast_api_poc}
DIR_WITH_MAIN=${DIR_WITH_MAIN:-app}
NAME_OF_MAIN=${NAME_OF_MAIN:-main}
DEFAULT_MODULE_NAME="$PROJECT_NAME.$DIR_WITH_MAIN.$NAME_OF_MAIN" # by default: fast_api_poc.app.main
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}

VARIABLE_NAME=${VARIABLE_NAME:-app} # The default VARIABLE_NAME is app when the main.py has: app = FastAPI()
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

export GUNICORN_CONF=${GUNICORN_CONF:-"/$PROJECT_NAME/server/prod/gunicorn_conf.py"}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

pipenv install --deploy --system && \
  apt-get remove -y gcc libssl-dev && \
  apt-get autoremove -y && \
  pip3 uninstall pipenv -y

# Start Gunicorn
exec gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"
