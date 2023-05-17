#!/bin/sh

# Image name
_IMAGE_NAME="ghcr.io/ansys/pysystemcoupling:${SYC_IMAGE_TAG:-latest}"

# Pull fluent image basedg  on tag
docker pull $_IMAGE_NAME

# Remove all dangling images
docker image prune -f
