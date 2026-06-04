#!/bin/bash

mkdir -p ./pids

./mongodb.sh &
echo $! > ./pids/mongodb.pid

./backend.sh &
echo $! > ./pids/backend.pid

./server.sh &
echo $! > ./pids/server.pid

echo "All services started."
