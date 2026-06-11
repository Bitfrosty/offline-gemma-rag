#!/bin/bash

mkdir -p ./pids ./logs ./mongodb-data

mongod --dbpath ./mongodb-data \
  --bind_ip 127.0.0.1 \
  > ./logs/mongodb.log 2>&1 &

echo $! > ./pids/mongodb.pid

echo "MongoDB started"
