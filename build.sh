#!/bin/bash
set -e

docker build --tag wtfloris/argos:latest .

if [[ $1 == -y ]]; then
        docker compose up -d
        exit
fi

read -p "Run the container? [y/N]" -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker compose up -d
fi
