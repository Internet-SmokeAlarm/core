#!/bin/bash

rm -r build
mkdir build

sam package --template-file template.yaml --s3-bucket fmlaas-core --output-template-file build/packaged.yaml
