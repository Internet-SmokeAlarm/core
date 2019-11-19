#!/bin/bash

rm -r build
mkdir build

sam build

sam package --s3-bucket fmlaas-core --output-template-file build/packaged.yaml

sam deploy --template-file build/packaged.yaml --stack-name fmlaas-core --capabilities CAPABILITY_NAMED_IAM
