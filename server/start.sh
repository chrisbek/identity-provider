#! /usr/bin/env sh
set -e

if [ "$MODE" = DEV ]; then
  echo "--------------- Running in dev ---------------"
	sh /"$PROJECT_NAME"/server/start_dev.sh
elif [ "$MODE" = PROD ]; then
  echo "--------------- Running in prod ---------------"
	sh /"$PROJECT_NAME"/server/start_prod.sh
else
  echo "Incorrect mode argument: ${MODE}"
  exit 1
fi