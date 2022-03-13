#!/bin/bash
echo Installing Python 3
brew install python3

echo Installing Virtual Environment
python3 -m pip install virtualenv
python3 -m virtualenv venv

. venv/bin/activate

echo Installing required Python packages...
python3 -m pip install -r requirements.txt
echo Done!
