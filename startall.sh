#!/usr/bin/env bash

./mongodb.sh &
echo $! > mongodb.pid

./backend.sh &
echo $! > backend.pid

cd /home/jrsub/offline-gemma-rag/llama.cpp

./server.sh &
echo $! > llama.pid

wait
