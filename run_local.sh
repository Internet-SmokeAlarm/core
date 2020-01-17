#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Argument 'stage' is required. Ex: 'bash deploy.sh dev'"
    exit 1
fi

STAGE=$1

sam build
sam local start-api --parameter-overrides Stage=${STAGE}
