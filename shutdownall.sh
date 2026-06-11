#!/bin/bash

echo "Stopping services..."

# Stop loaded Ollama model
if command -v ollama >/dev/null 2>&1; then
  echo "Stopping Ollama model gemma4:e2b..."
  ollama stop gemma4:e2b 2>/dev/null
fi

# Stop Uvicorn reload parent/child processes
echo "Stopping backend..."
pkill -f "uvicorn server:app" 2>/dev/null

# Stop MongoDB started from this project
echo "Stopping MongoDB..."
pkill -f "mongod --dbpath ./mongodb-data" 2>/dev/null

# Stop any tracked PID files
for pidfile in ./pids/*.pid; do
  [ -e "$pidfile" ] || continue

  pid=$(cat "$pidfile")

  if kill -0 "$pid" 2>/dev/null; then
    echo "Stopping PID $pid from $pidfile..."
    kill "$pid" 2>/dev/null
    sleep 1

    if kill -0 "$pid" 2>/dev/null; then
      echo "Force stopping PID $pid..."
      kill -9 "$pid" 2>/dev/null
    fi
  fi

  rm "$pidfile"
done

# Extra cleanup in case Ollama run is still attached
pkill -f "ollama run gemma4:e2b" 2>/dev/null

echo "Shutdown complete."
