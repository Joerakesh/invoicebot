#!/bin/bash

echo "STARTING INVOICEBOT..."

docker compose down

docker compose up --build -d

echo "WAITING FOR SERVER..."

sleep 8

xdg-open http://localhost:8000

echo "INVOICEBOT RUNNING"

docker compose logs -f
