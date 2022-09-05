#! /usr/bin/env sh
set -e

PROJECT_NAME=${PROJECT_NAME:-fast_api_poc}
DIR_WITH_MAIN=${DIR_WITH_MAIN:-app}
NAME_OF_MAIN=${NAME_OF_MAIN:-main}
DEFAULT_MODULE_NAME="$PROJECT_NAME.$DIR_WITH_MAIN.$NAME_OF_MAIN" # by default: fast_api_poc.app.main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app} # The default VARIABLE_NAME is app when the main.py has: app = FastAPI()
APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}
DEBUG_MODULE="$PROJECT_NAME.debug.main"

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-debug} # other options: {debug, warning, error, critical}
RELOAD=${RELEOAD:-true}

#poetry config virtualenvs.create false
#poetry install

if [ "$RELOAD" = true ]; then
	# Start Uvicorn with live reload
	exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
#	python -m $DEBUG_MODULE -m uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
else
	# Start Uvicorn without live reload
  exec uvicorn --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
fi
