'''
Creates the crap database for the hacking
'''

import os
import sys
import sqlite3
from rustedbunions import settings
from flags import FLAGS

CRAPDB_SETUP = [
    "CREATE TABLE flags (flag text)",
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table1"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table2"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table3"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table4"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table5"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table6"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table7"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table8"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table9"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table10"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table11"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table12"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table13"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table14"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table15"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table16"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table17"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table18"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table19"][0]),
    "INSERT INTO flags VALUES ('{}')".format(FLAGS["flag_table20"][0]),
    "CREATE TABLE users (username text, password text, question text, answer text, paid integer)",
    "INSERT INTO users VALUES ('admin', 'H4ckm31FYOUC4n!@*&$#', 'I AM ADMIN', 'I AM ALWAYS WATCHING', 0)",
    "INSERT INTO users VALUES ('joey', 'Sup3rS3cr3t', 'Who is Your daddy', 'spiderman', 0)",
    "INSERT INTO users VALUES ('jackblack', 'Sch00lOfRock', 'THE PICK OF DESTINY', 'That is not a question', 0)",
    "INSERT INTO users VALUES ('SirPaysALot', 'IPayAL0t!', 'Did I pay?', 'Why yes, I did for sure!', 1)"
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
