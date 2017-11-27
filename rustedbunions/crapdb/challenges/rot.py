import os
import random
import string
import json
import hashlib

from datetime import datetime
from datetime import timedelta

from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FLAGS

from rustedbunions import settings

MOVIE_QUOTES = []
WORDS = []

# Load all the movie quotes
with open(os.path.join(settings.BASE_DIR, "movie_quotes.txt")) as f:
    MOVIE_QUOTES.extend(f.readlines())

# Load all the 4 letter or longer words
with open(os.path.join(settings.BASE_DIR, "words_alpha.txt")) as f:
    for line in f.readlines():
        if len(line) >= 4:
            WORDS.append(line)

class Rot(Challenge):
    ALPHABET = string.ascii_lowercase
    ROT_TIMEOUT = 1 # 1 minute to solve

    meta = ChallengeMetadata(
        challenge_id="rot",
        name="ROT?",
        description="Ancient crypto",
        price=25,
        value=FLAGS["rot_challenge"][1],
        flag=FLAGS["rot_challenge"][0]
    )

    def __init__(self):
        super().__init__()
        random.seed() # uses current system time

        # Solve 50 of them to win
        self.num_to_solve = 50

        # They will have 1 minute to solve from purchase
        self.timeout = None

        # Number of seconds remaining to solve
        self.remaining_time = 0

        self.messages = []
        self.encrypted_messages = []
        self.message_hashes = []

    def purchase(self, hacker_bucks):
        return_bucks = super().purchase(hacker_bucks)
        if not self.purchased:
            self.reset()
        return return_bucks

    def reset(self):
        now = datetime.utcnow()
        self.timeout = now + timedelta(minutes=self.ROT_TIMEOUT)
        self.remaining_time = (self.timeout - now).total_seconds()
        self.generate_enc_messages()

    def is_expired(self):
        if self.timeout:
            self.remaining_time = (self.timeout - datetime.utcnow()).total_seconds()
            print("is_expired() - Remaining Time: ", self.remaining_time)
            if self.remaining_time <= 0:
                return True
        return False

    def update(self):
        if self.is_expired():
            self.reset()
        elif self.timeout is None:
            self.reset()

    def to_json(self):
        obj = super().to_json()
        self.update()

        obj.update({
            "num_to_solve": self.num_to_solve,
            "remaining_time": self.remaining_time,
            "encrypted_messages": self.encrypted_messages,
            "message_hashes": self.message_hashes
        })
        return obj

    def generate_enc_messages(self):
        self.messages = []
        self.encrypted_messages = []
        self.message_hashes = []

        for i in range(self.num_to_solve):
            # Pick a random shift b/w 1 and 25
            key = random.randint(1, 25)

            # Do we pick a movie quote, or some random words?
            if random.randint(0, 1):
                # Pick a random movie quote
                self.messages.append(MOVIE_QUOTES[random.randint(0, len(MOVIE_QUOTES) - 1)].strip().lower())
            else:
                # Make a random message
                self.messages.append(self.make_random_message())

            # Generate the crypto message
            self.encrypted_messages.append(self.shifttext(key, self.messages[i]))

            # Store the clear-text hash to send to the user
            self.message_hashes.append(hashlib.sha256(str(self.messages[i]).encode('utf-8')).hexdigest())

    def make_random_message(self):
        length = random.randint(5, 20)
        msg_list = []
        for i in range(length):
            msg_list.append(WORDS[random.randint(0, len(WORDS) - 1)].strip().lower())
        return ' '.join(msg_list)

    def shifttext(self, shift, msg):
        msg = msg.strip().lower()
        data = []
        for c in msg:
            if c.strip() and c in self.ALPHABET:
                data.append(self.ALPHABET[(self.ALPHABET.index(c) + shift) % 26])
            else:
                data.append(c)

        output = ''.join(data)
        return output

    def check(self, answer):
        # Update will only change the message if the timer is expired
        self.update()

        try:
            answer = json.loads(answer)
        except:
            print("Unable to parse provided JSON")
            return False

        if not isinstance(answer, list):
            print("The answer should be a list of all solved messages")
        elif set(answer) == set(self.messages):
            self.solved = True
            return True
        else:
            print("No match. Answers: ", answer)
            print("Messages: ", self.messages)
        return False

Session.register_challenge(Rot)
