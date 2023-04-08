#!/bin/bash

# Create a .image-registry-auth-config-env.sh file with environment variables
# set for REGISTRY_USERNAME, REGISTRY_PASSWORD and IMAGE_REGISTRY (optional).
# Using a password manager like LastPass with it's lpass CLI program to set the
# variables would be good for this.
source .image-registry-auth-config-env.sh

IMAGE_REGISTRY=${IMAGE_REGISTRY-"https://index.docker.io/v1/"}
CONFIG=.image-registry-auth-config.json
touch $CONFIG
chmod 600 $CONFIG
AUTH=$(echo -n "${REGISTRY_USERNAME}:${REGISTRY_PASSWORD}" | base64)
cat << EOF > $CONFIG
{
    "auths": {
        "$IMAGE_REGISTRY": {
            "auth": "${AUTH}"
        }
    }
}
EOF
