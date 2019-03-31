'''
Flag generator.
'''
import os
import random

# NOTE: Change this
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


# Because init_instance is basically __init__() in this case b/c singleton
# pylint: disable=W0201
class FlagGeneratorSingleton:
    '''
    Class used to generate flags
    '''

    MIN_FLAG_LENGTH = 10  # 10 character minimum
    CHAR_REPLACE_MAP = {
        ' ': ["_", "-", ".", "/", "=", "*"],  # Characters used to replace white space
        'a': ['4', '@'],
        'o': ['0'],
        'e': ['3'],
        't': ['7', "+"],
        'l': ['1', '!'],
        's': ['5', '$'],
        'b': ['6', '8']
    }

    #       Flag name,          flag,      reward
    FLAGS = {
        "index_page_source":("flag{TEST1}", 7),
        "forgetful_page_source":("flag{TEST2}", 7),
        "no_user_login":("flag{TEST3}", 25),
        "no_password_login":("flag{TEST4}", 25),
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
        "stego1":("flag{TEST44}", 10),
        "stego2":("flag{TEST45}", 15),
        "stego3":("flag{TEST46}", 25),
        "github_issue":("flag{TEST47}", 10),
        "github_commit":("flag{TEST48}", 10),
        "paid_content_challenge": ("flag{TEST49}", 40),
        "xor_challenge": ("flag{TEST50}", 50),
        "dir_traveler": ("flag{TEST51}", 10),
        "genes": ("flag{TEST52}", 50)
    }

    #: The singleton instance of the web server
    _instance = None

    def __new__(cls):
        '''
        Create a new instance
        '''
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.init_instance()
        return cls._instance

    def init_instance(self):
        '''
        Initialize the instance of this singleton
        '''
        # Read in the words on import
        self.words = []
        self.generated_flags = {}
        self.max_flag_length = 0
        with open("hacker_ipsum.txt", "r") as f:
            self.words = f.read()
            self.words = self.words.splitlines()  # Splits up lines without the newline (f.readlines() includes the \n)

    def __len__(self):
        '''
        Return the number of flags total
        '''
        return len(self.FLAGS.keys())

    def _flag_jumbler(self, flag_content):
        '''
        Takes some flag content and randomly replaces some common characters
        with lookalikes. Acts as a second pass of randomization so flags
        cannot be guessed.
        '''
        new_flag_content = ""
        for char in flag_content:
            if char.lower() not in self.CHAR_REPLACE_MAP:  # It's not a character we're going to replace
                new_flag_content += char  # So just add it to the output
                continue  # And skip the next part
            elif char.lower() == ' ':  # It's the space character. Always replace those
                should_replace = 0
            else:
                # Decide if we should replace
                should_replace = random.random()  # Returns float b/w 0.0 and 1.0

            if should_replace <= 0.3:  # Replace 30% of the time
                new_flag_content += random.choice(self.CHAR_REPLACE_MAP[char.lower()])
            else:
                new_flag_content += char

        return new_flag_content

    def _generate_flag(self):
        '''
        Internal method to generate a single flag
        '''
        flag_str = "flag{{{}}}"

        words_copy = list(self.words)  # Make a local copy we can modify
        flag_content = []
        length = random.randint(2, 5)
        for _ in range(length):
            choice = random.choice(words_copy)
            words_copy.remove(choice)
            flag_content.append(choice)

        # Append some extra if needed
        while len(' '.join(flag_content)) < self.MIN_FLAG_LENGTH:
            choice = random.choice(words_copy)
            words_copy.remove(choice)
            flag_content.append(choice)

        flag_content = ' '.join(flag_content)  # Join with spaces

        # Jumble the flag
        flag_content = self._flag_jumbler(flag_content)

        return flag_str.format(flag_content)

    def generate_flags(self):
        '''
        Generate all the flags
        '''
        if self.generated_flags:
            return self.generated_flags
        if os.path.exists("flags.txt"):
            with open("flags.txt", "r") as fh:
                flags = fh.read().splitlines()

            for flag in flags:
                key, flg, val = flag.split(",")
                self.generated_flags[key] = (flg, val)

            self.max_flag_length = max([len(x[0]) for x in self.generated_flags.values()])
            return self.generated_flags

        for key, value in self.FLAGS.items():
            self.generated_flags[key] = (self._generate_flag(), value[1])

        self.max_flag_length = max([len(x[0]) for x in self.generated_flags.values()])

        with open("flags.txt", "w") as fh:
            for key, value in self.generated_flags.items():
                fh.write(key + "," + value[0] + "," + str(value[1]) + "\n")

        return self.generated_flags


FlagGenerator = FlagGeneratorSingleton()
