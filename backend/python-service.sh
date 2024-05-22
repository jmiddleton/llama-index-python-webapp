#!/bin/bash
#
# python-service    Start up python-service 
#

# set the python script name
SNAME=main.py

echo $"Starting $SNAME ..."
cd /data/llama-index-python-webapp/backend
$HOME/.local/bin/poetry run python $SNAME