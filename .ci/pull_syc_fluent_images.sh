#!/bin/bash

docker pull ghcr.io/pyansys/pysystem-coupling:${SYC_IMAGE_VERSION} &
docker pull ghcr.io/pyansys/pyfluent:${FLUENT_IMAGE_VERSION} &

# Wait for the background processes to finish
wait