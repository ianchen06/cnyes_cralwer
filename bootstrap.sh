# This script sets up dev environment for you
set -ex
python -m venv cnyes_venv
. ./cnyes_venv/bin/activate
pip install -r requirements.txt
