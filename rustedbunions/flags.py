'''
All the flags in one place so I only have to edit the one
file on deploy
'''

# NOTE: Change before deploy
FLAGS = {
    "index_page_source":("flag{TEST1}", 7),
    "forgetful_page_source":("flag{TEST2}", 7),
    "no_user_login":("flag{TEST3}", 25),
    "no_password_login":("flag{TEST4}", 25),
    "django_admin_flag":("flag{TEST5}", 10000),
    "django_settings_flag":("flag{TEST6}", 12),
    "super_admin_challenge":("flag{TEST7}", 15),
    "index_console_output":("flag{TEST8}", 10),
    "flag_table1":("flag{TEST9}", 1),
    "flag_table2":("flag{TEST10}", 1),
    "flag_table3":("flag{TEST11}", 1),
    "flag_table4":("flag{TEST12}", 1),
    "flag_table5":("flag{TEST13}", 1),
    "flag_table6":("flag{TEST14}", 1),
    "flag_table7":("flag{TEST15}", 1),
    "flag_table8":("flag{TEST16}", 1),
    "flag_table9":("flag{TEST17}", 1),
    "flag_table10":("flag{TEST18}", 1),
    "flag_table11":("flag{TEST19}", 1),
    "flag_table12":("flag{TEST20}", 1),
    "flag_table13":("flag{TEST21}", 1),
    "flag_table14":("flag{TEST22}", 1),
    "flag_table15":("flag{TEST23}", 1),
    "flag_table16":("flag{TEST24}", 1),
    "flag_table17":("flag{TEST25}", 1),
    "flag_table18":("flag{TEST26}", 1),
    "flag_table19":("flag{TEST27}", 1),
    "flag_table20":("flag{TEST28}", 1),
    "valid_creds_login":("flag{TEST29}", 25),
    "valid_sec_answer":("flag{TEST30}", 25),
    "brutal_force_challenge":("flag{TEST31}", 12),
    "rot_challenge":("flag{TEST32}", 37),
    "shortest_sqli":("flag{TEST33}", 17),
    "scoreboard_hacking":("flag{TEST34}", 50),
    "game1":("flag{TEST35}", 12),
    "game2":("flag{TEST36}", 12),
    "game3":("flag{TEST37}", 12),
    "game4":("flag{TEST38}", 12),
    "game5":("flag{TEST39}", 12),
    "game6":("flag{TEST40}", 17),
    "game7":("flag{TEST41}", 20),
    "game8":("flag{TEST42}", 22),
    "game9":("flag{TEST43}", 25),
    "stego1":("flag{TEST44}", 10),
    "stego2":("flag{TEST45}", 15),
    "stego3":("flag{TEST46}", 25),
    "github_issue":("flag{TEST47}", 10),
    "github_commit":("flag{TEST48}", 10),
    "paid_content_challenge": ("flag{TEST49}", 40),
    "xor_challenge": ("flag{TEST50}", 50),
    "dir_traveler": ("flag{TEST51}", 10)
}

# NOTE: Change before deploy
#               user       password        question         answer     paid?
CRAPDB_USERS = {
    "admin": "('admin', 'admin_password', 'sec_question', 'sec_answer', 0)",
    "user1": "('user1', 'user1_password', 'sec_question', 'sec_answer', 0)",
    "user2": "('user2', 'user2_password', 'sec_question', 'sec_answer', 0)",
    "user3": "('user3', 'user3_password', 'sec_question', 'sec_answer', 0)",
    "user4": "('user4', 'user4_password', 'sec_question', 'sec_answer', 0)",
    "paid1": "('paid1', 'paid1_password', 'sec_question', 'sec_answer', 1)",
    "paid2": "('paid2', 'paid2_password', 'sec_question', 'sec_answer', 1)",
    "paid3": "('paid3', 'paid3_password', 'sec_question', 'sec_answer', 1)"
}

MAX_FLAG_LENGTH = max([len(x) for x in FLAGS])
