!#/usr/bin
set -o exit
pip install -r requirements.txt
flask db upgrade
flask seed run
