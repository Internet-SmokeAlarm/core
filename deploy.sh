#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Argument 'stage' is required. Ex: 'bash deploy.sh dev'"
    exit 1
fi

STAGE=$1

confirm() {
    # call with a prompt string or use a default
    read -r -p "${1:-Are you sure? [y/N]} " response
    case "$response" in
        [yY][eE][sS]|[yY])
            true
            ;;
        *)
            exit 1
            ;;
    esac
}

if [[ $STAGE == *"prod"* ]]; then
  $(confirm)
fi

rm -r build || true
mkdir build

aws s3api create-bucket --bucket ${STAGE}-fedlearn-core --region us-east-1

sam build
sam package --s3-bucket ${STAGE}-fedlearn-core --output-template-file build/packaged.yaml
sam deploy  \
    --template-file build/packaged.yaml \
    --stack-name ${STAGE}-fedlearn \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides Stage=${STAGE}
