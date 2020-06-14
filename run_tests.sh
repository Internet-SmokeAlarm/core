#!/bin/bash

export MODELS_BUCKET="fedlearn-models-bucket-test"

python3 -m unittest tests
