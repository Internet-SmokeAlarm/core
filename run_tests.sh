#!/bin/bash

export MODELS_BUCKET="fedlearn-models-bucket-test"

/usr/local/opt/python@3.8/bin/python3 -m unittest tests
