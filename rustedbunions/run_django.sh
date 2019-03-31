#!/bin/bash

if [ -d "venv" ];
then
    echo; echo "***Activate existing venv***"; echo
    source ./venv/bin/activate
else
    echo; echo "***Create new venv***"; echo
    python3 -m venv ./venv
    source ./venv/bin/activate

    # Only run pip on initial setup.
    pip install -r requirements.txt
fi

python manage.py migrate
python manage.py runserver

exit 0