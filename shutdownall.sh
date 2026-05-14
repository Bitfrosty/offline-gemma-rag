#!/usr/bin/env bash

echo "Stopping services..."

kill $(cat mongodb.pid)
kill $(cat backend.pid)
kill $(cat llama.pid)

rm *.pid

echo "All services stopped."
