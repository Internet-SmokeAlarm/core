#!/bin/bash

sam deploy --template-file build/packaged.yaml --stack-name fmlaas-core --capabilities CAPABILITY_IAM
