#!/usr/bin/env bash

./mongodb.sh &
echo $! > mongodb.pid

./backend.sh &
echo $! > backend.pid

./server.sh

wait
