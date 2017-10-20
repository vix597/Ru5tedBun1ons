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

python3 manage.py collectstatic

if [ ! -d "/home/protected/database" ];
then
    mkdir /home/protected/database
    chgrp web /home/protected/database
    chmod g+w /home/protected/database
fi

python3 manage.py migrate

if [ -f "/home/protected/database/db.sqlite3" ];
then
    chgrp web /home/protected/database/db.sqlite3
    chmod g+w /home/protected/database/db.sqlite3
else
    echo "ERROR: Could not modify permission on db file"
    exit 1
fi

if [ -f "/home/protected/database/crapdb.sqlite3" ];
then
    chgrp web /home/protected/database/crapdb.sqlite3

    # Make this DB read-only
    chmod a-w /home/protected/database/crapdb.sqlite3
else
    echo "ERROR: Could not modify permissions on crapdb file"
    exit 1
fi

exit 0