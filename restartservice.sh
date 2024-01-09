#!/bin/bash

# Stop and remove containers, networks, images, and volumes
docker-compose -f docker-compose-dev.yaml --profile ipfs down --volumes

# Remove all unused containers, networks, images (both dangling and unreferenced), and optionally, volumes
docker system prune -f

# Execute the bootstrap script
sh bootstrap.sh

# Execute the build-dev script
sh build-dev.sh

echo "Check EpochID on etherscan"
echo "ForceskipEpoch on Remix"
echo "Ok Bye"

