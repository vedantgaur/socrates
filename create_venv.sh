#!/bin/sh

rm -rf venv
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
