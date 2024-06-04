#!/bin/bash

echo "Pulling pysystem-coupling Image Version ${SYC_IMAGE_VERSION}"
echo "Pulling pyfluent Image Version ${FLUENT_IMAGE_VERSION}"

docker pull ghcr.io/pyansys/pysystem-coupling:${SYC_IMAGE_VERSION} &
docker pull ghcr.io/pyansys/pyfluent:${FLUENT_IMAGE_VERSION} &

# Wait for the background processes to finish
wait