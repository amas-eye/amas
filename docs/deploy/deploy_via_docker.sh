#!/usr/bin/env bash

docker network create amas

docker run -d -p 4242:4242 --name opentsdb --network amas eacon/docker-opentsdb
docker run -d -p 27017:27017 --name mongo --network amas mongo
docker run -d -p 6379:6379 --name redis --network amas redis

docker run -d --name collector --network amas -p 8001:8001 eacon/argus_collector
docker run -d --name alert --network amas eacon/argus_alert
docker run -d --name statistics --network amas eacon/argus_statistics
docker run -d --name web --network amas -p 8080:8080 eacon/argus-web