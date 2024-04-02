#!/bin/bash

# 1. Replace whisper.api Dockerfile
    # Specify the paths to the Dockerfiles
    source_dockerfile="./Dockerfile.whisper.api"
    destination_dockerfile="./whisper.api/Dockerfile"
    # Check if the source Dockerfile exists
    if [ -e "$source_dockerfile" ]; then
        # Copy the contents of the source Dockerfile to the destination Dockerfile
        cp "$source_dockerfile" "$destination_dockerfile"
        echo "Contents of $source_dockerfile copied to $destination_dockerfile"
    else
        echo "Source Dockerfile ($source_dockerfile) not found."
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
        echo "Download completed successfully."
    else
        echo "Error: Download failed."
    fi
    else
    echo "Destination directory is not empty. Skipping download."
fi

# 3. Run Docker Compose which will build the images ands start the 4 servers
# for some reason webui has to be rebuilt explicitly
    # docker compose up --build webui-server
    docker compose up

