#!/bin/bash

if [ -d "venv" ];
then
    echo; echo "***Activate existing venv***"; echo
    source ./venv/bin/activate
else
    echo; echo "***Create new venv***"; echo
    virtualenv --system-site-packages ./venv 
    source ./venv/bin/activate

    # Only run pip on initial setup.
    pip3 install -r requirements.txt
fi

python3 manage.py migrate
python3 manage.py runserver

exit 0