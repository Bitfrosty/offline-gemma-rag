#!/bin/bash

mkdir -p ./pids ./logs

source .venv/bin/activate

uvicorn server:app \
  --host 0.0.0.0 \
  --port 3000 \
  --reload \
  > ./logs/backend.log 2>&1 &

echo $! > ./pids/backend.pid

echo "Backend started on http://0.0.0.0:3000"
