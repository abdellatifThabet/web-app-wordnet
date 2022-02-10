#!bin/bash

## first we  build the docker image
docker build -t flask-app .
## than we run the container
docker run -d -p5000:5000 --net=host flask-app
