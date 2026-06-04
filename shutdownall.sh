#!/bin/bash

for pidfile in ./pids/*.pid; do
  [ -e "$pidfile" ] || continue

  pid=$(cat "$pidfile")

  if kill -0 "$pid" 2>/dev/null; then
    echo "Stopping process $pid..."
    kill "$pid"
  else
    echo "Process $pid is not running."
  fi

  rm "$pidfile"
done

echo "Shutdown complete."
