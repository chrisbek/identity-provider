#! /usr/bin/env sh
set -e

docker-compose rm -f
docker-compose --env-file ./server/project_conf.conf up --build --remove-orphans -d