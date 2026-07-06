#!/bin/bash

mkdir -p ./pids ./logs

MODEL_NAME="${1:-gemma4:e2b}"

ollama run "$MODEL_NAME" \
  > ./logs/ollama.log 2>&1 &

echo $! > ./pids/ollama-model.pid

echo "Ollama model $MODEL_NAME started"
