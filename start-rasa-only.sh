#!/bin/bash

# 0. Clear console
clear;

# 1. Replace whisper.api Dockerfile
    # Specify the paths to the Dockerfiles
    source_dockerfile="./Dockerfile.whisper.api"
    destination_dockerfile="./whisper.api/Dockerfile"
    # Check if the source Dockerfile exists
    if [ -e "$source_dockerfile" ]; then
        # Copy the contents of the source Dockerfile to the destination Dockerfile
        cp "$source_dockerfile" "$destination_dockerfile"
        echo "[start-servers.sh] Contents of $source_dockerfile copied to $destination_dockerfile"
    else
        echo "[start-servers.sh] Source Dockerfile ($source_dockerfile) not found."
    fi

# 2. Download initial model for rasa
    # Define the URL of the file
    url="https://github.com/RasaHQ/rasa-x-demo/raw/master/models/model.tar.gz"
    # Define the destination directory
    destination="./rasa-bot/models/"
    # Check if the destination directory is empty
    if [ -z "$(ls -A $destination)" ]; then
    # Use curl to download the file
    curl -L "$url" -o "${destination}model.tar.gz"
    # Check if the download was successful
    if [ $? -eq 0 ]; then
        echo "[start-servers.sh] Rasa initial model download completed successfully to $destination"
    else
        echo "[start-servers.sh] Rasa initial model download failed to $destination"
    fi
    else
    echo "[start-servers.sh] Destination directory $destination is not empty. Skipping download."
fi

# freshly train model for rasa
# cd ./rasa-bot
# rm -rf models/;
# rasa train --domain domain.yml --config config.yml;
# cd ..

# 4. Check that the rasa model server is pointed at the right action server URL
endpoints_file="./rasa-bot/endpoints.yml"
wrong_url="http://0.0.0.0:5055/webhook"
url_line="url: \"$docker_url\""

if grep -q "^#*url: \"$wrong_url\"" "$endpoints_file"; then
    echo "Reminder: Please replace the URL \"$wrong_url\" with the Docker specific URL."
    exit 1
fi

# 5. Run Docker Compose which will build the images ands start the 4 servers
# for some reason webui has to be rebuilt explicitly
# docker compose up --build webui-server
docker compose -f "docker-compose-rasa-only.yml" up

