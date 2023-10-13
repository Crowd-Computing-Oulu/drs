# use a python container as a starting point
FROM python:3.8

# install dependencies of interest
RUN python -m pip install rasa

# set workdir and copy data files from disk
# note the latter command uses .dockerignore
WORKDIR /app
ENV HOME=/app
COPY . .

# train a new rasa model
RUN rasa train nlu

# set the user to run, don't run as root
USER 1001

# set entrypoint for interactive shells
ENTRYPOINT ["rasa"]

# command to run when container is called to run
CMD ["run", "--enable-api", "--port", "5005"]