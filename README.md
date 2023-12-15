# Dani's Robot Server - DRS

A combination of Docker services to provide a conversational agent (e.g. one embodied by a Pepper humanoid social robot)with conversational abilities:

1. Speech Recognition → **Whisper**
2. Natural Language Understanding → **Rasa**
3. Speech Synthesis → **Bark**
4. Web GUI → **PHP**

# Clients

1. [Pepper Robot (NaoQi Python)](https://github.com/Crowd-Computing-Oulu/drs-naoqi-client)
2. [WatchOS (Swift)](https://github.com/Crowd-Computing-Oulu/watchos-drs-client)
3. Pepper Robot (Android) - Soon
   
## Usage

1. Make sure python 3.8 is installed, as it is needed for Rasa
     1. MacOS: `brew install python@3.8`
2. Install Rasa: `python3.8 -m pip install rasa`
3. Train Rasa Model: `sudo rasa train`
3. Make sure you have [Docker](https://docs.docker.com/desktop/) installed and running
4. Start the containers with `start-servers.sh`
5. Validate that all containers are running with `validate-containers.sh`

# Interacting with containers
Example:
`sudo docker exec -it conversational-agent-server /bin/bash`

Trying Rasa locally without Docker
`export SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True`
`sudo python3.11 -m pip install scikit-learn dask --break-system-packages --ignore-requires-python`

Curl Rasa Test
`curl --request POST http://localhost:5005/webhooks/rest/webhook --header 'content-type: application/json' --data '{ }"message": "hi" }' `
