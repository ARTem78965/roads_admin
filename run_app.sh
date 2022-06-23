#!/bin/bash

ENV_FILE_PATH=$1

if [ -f "$ENV_FILE_PATH" ]; then
    export $(cat "$ENV_FILE_PATH" | sed 's/#.*//g' | xargs)
fi

export POSTGRES_HOST=localhost

./venv/bin/python src/main.py
