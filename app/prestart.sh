#! /usr/bin/env bash

mkdir -m 777 /json

echo "install additional packages"

pip install --upgrade pip && \
pip install --no-cache-dir -r requirements.txt
