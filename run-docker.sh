#!/usr/bin/env bash

# build a container called 'fraud'
docker build . -t fraud

# run the container with a bash shell
docker run -it fraud
