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

aws s3api create-bucket --bucket ${STAGE}-verge-ai-core --region us-east-1

# NOTE: Below, you need to include the correct Cognito User Pool Client ID, and User Pool ID.
# These values are used to authenticate with AWS Amplify Auth resources.
# Long-term, this needs to be defined somewhere outside of Amplify....

sam build
sam package --s3-bucket ${STAGE}-verge-ai-core --output-template-file build/packaged.yaml
sam deploy  \
    --template-file build/packaged.yaml \
    --stack-name ${STAGE}-verge-ai \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides Stage="${STAGE}" CognitoUserPoolClientId="3bhv5ffke7ss8of73qtmnokk8v" CognitoUserPoolId="us-east-1_gl75zuVtc"
