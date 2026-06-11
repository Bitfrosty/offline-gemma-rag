#!/bin/bash

mkdir -p ./pids ./logs

ollama run gemma4:e2b \
  > ./logs/ollama.log 2>&1 &

echo $! > ./pids/ollama-model.pid

echo "Ollama model gemma4:e2b started"
