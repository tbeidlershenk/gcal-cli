#!/bin/bash

export CREDENTIALS_FILE="" # full path to your credentials.json file
export GCAL_CLI_HOME="" # full path to the gcal-cli directory
export CALENDAR_ID="" # your calendar ID to use

cd $GCAL_CLI_HOME
python3 gcal.py $@
