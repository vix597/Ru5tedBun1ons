import os
import sys
import sqlite3
from rustedbunions import settings

#
# TODO: Make sure to change all these in deployment so answers can't just be taken from source
#
CRAPDB_SETUP = [
    "CREATE TABLE flags (flag text)",
    "INSERT INTO flags VALUES ('Flag={Y0u_did_1t}')",
    "INSERT INTO flags VALUES ('Flag={This_Table_Has_a_few_flags}')",
    "INSERT INTO flags VALUES ('Flag={JustThreeActually!}')",
    "CREATE TABLE users (username text, password text, question text, answer text)",
    "INSERT INTO users VALUES ('Joey', 'Sup3rS3cr3t', 'Who is Your daddy', 'spiderman')"
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