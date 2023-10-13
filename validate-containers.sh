#!/bin/bash

# Define an array of service names and their corresponding ports
services=(
  "mimic3-server:9000"
  "whisper-server:9001"
  "rasa-server:9002"
  "webui-server:8080"
)

# Loop through the services and check if they are up
for service in "${services[@]}"; do
  service_name=$(echo "$service" | cut -d':' -f1)
  port=$(echo "$service" | cut -d':' -f2)

  # Check if the service is responding to pings
  if curl -s "http://localhost:$port" >/dev/null; then
    echo "$service_name is up and running on port $port"
  else
    echo "$service_name is not running on port $port"
  fi
done
