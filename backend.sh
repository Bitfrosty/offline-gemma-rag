#!/bin/bash

mkdir -p ./pids ./logs

source .venv/bin/activate

uvicorn server:app \
  --host 127.0.0.1 \
  --port 3000 \
  --reload \
  > ./logs/backend.log 2>&1 &

echo $! > ./pids/backend.pid

echo "Backend started on http://127.0.0.1:3000"
