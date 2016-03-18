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
wget "$SERVER"website/quickstart -O website/quickstart.html
wget "$SERVER"website/learn -O website/learn/index.html
wget "$SERVER"website/contribute -O website/contribute.html
wget "$SERVER"website/discuss -O website/discuss.html
wget "$SERVER"website/home -O website/home.html
wget "$SERVER"website/acknowledge -O website/acknowledge.html
wget "$SERVER"website/latest -O website/latest.html


wget "$SERVER"website/learn/architecture -O website/learn/architecture.html
wget "$SERVER"website/learn/routing -O website/learn/routing.html
wget "$SERVER"website/learn/type_annotation -O website/learn/type_annotation.html
wget "$SERVER"website/learn/directives -O website/learn/directives.html
wget "$SERVER"website/learn/output_formats -O website/learn/output_formats.html
wget "$SERVER"website/learn/extending -O website/learn/extending.html

wget $SERVER/404 -O 404.html --content-on-error

git add website

