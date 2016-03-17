#!/bin/bash
# Builds a new static copy of the hug website

mkdir static
mkdir website

export SERVER='http://localhost:8000/'

wget $SERVER -O index.html
