#!/bin/bash
# Builds a new static copy of the hug website
export SERVER='http://localhost:8000/'

git rm -rf static
git rm -rf website

mkdir static
mkdir website
mkdir website/learn

cp ../hug_website/hug_website/static/stylesheets -rf static
cp ../hug_website/hug_website/static/images -rf static
git add static

wget $SERVER -O index.html
wget "$SERVER"website/quickstart -O website/quickstart
wget "$SERVER"website/learn -O website/learn/index.html
wget "$SERVER"website/contribute -O website/contribute
wget "$SERVER"website/discuss -O website/discuss
wget "$SERVER"website/home -O website/home

wget "$SERVER"website/learn/architecture -O website/learn/architecture
wget "$SERVER"website/learn/routing -O website/learn/routing
wget "$SERVER"website/learn/type_annotation -O website/learn/type_annotation
wget "$SERVER"website/learn/directives -O website/learn/directives
wget "$SERVER"website/learn/output_formats -O website/learn/output_formats
wget "$SERVER"website/learn/extending -O website/learn/extending

wget $SERVER/404 -O 404.html --content-on-error

git add website

