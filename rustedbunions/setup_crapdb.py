'''
Creates the crap database for the hacking
'''

import os
import sys
import sqlite3
from rustedbunions import settings

#
# NOTE: Make sure to change all these in deployment so answers can't just be taken from source
#
# -------------- INCLUDING THE CREDS FOR THE USERS ---------------
# 
CRAPDB_SETUP = [
    "CREATE TABLE flags (flag text)",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "INSERT INTO flags VALUES ('Flag={__PLACEHOLDER_FLAG__}')",
    "CREATE TABLE users (username text, password text, question text, answer text)",
    "INSERT INTO users VALUES ('Admin', 'H4ckm31FYOUC4n!@*&$#', 'I AM ADMIN', 'I AM ALWAYS WATCHING')",
    "INSERT INTO users VALUES ('Joey', 'Sup3rS3cr3t', 'Who is Your daddy', 'spiderman')",
    "INSERT INTO users VALUES ('JackBlack', 'Sch00lOfRock', 'THE PICK OF DESTINY', 'That is not a question')"
]

if __name__ == "__main__":
    if os.path.exists(settings.CRAPDB_PATH):
        print("DB is already setup")
        sys.exit(0)

    # Creates the file if it doesn't exist
    conn = sqlite3.connect(settings.CRAPDB_PATH)
    for query in CRAPDB_SETUP:
        try:
            conn.execute(query)
        except:
            print("Failed on query: ", query)
            conn.commit()
            conn.close()
            sys.exit(1)

    conn.commit()
    conn.close()
    sys.exit(0)
