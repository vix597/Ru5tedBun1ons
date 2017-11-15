import os
import random
import string
from datetime import datetime
from datetime import timedelta

from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FLAGS

from rustedbunions import settings

MOVIE_QUOTES = []

# Load all the movie quotes
with open(os.path.join(settings.BASE_DIR, "movie_quotes.txt")) as f:
    MOVIE_QUOTES.extend(f.readlines())

class Rot(Challenge):
    ALPHABET = string.ascii_lowercase
    ROT_TIMEOUT = 1 # 1 minute to solve

    meta = ChallengeMetadata(
        challenge_id="rot",
        name="ROT?",
        description="Ancient crytpo",
        price=25,
        value=FLAGS["rot_challenge"][1],
        flag=FLAGS["rot_challenge"][0]
    )

    def __init__(self):
        super().__init__()
        random.seed() # uses current system time

        # Solve between 10 and 50 to get the flag
        self.num_to_solve = random.randint(10, 50)

        # They will have 1 minute to solve from purchase
        self.timeout = None

        # Number solved so far
        self.num_solved = 0

        self.key = 0
        self.message = ""
        self.encrypted_message = ""

        # Generate the key, pick the message, and generate the encrypted message
        self.generate_enc_message()

    def purchase(self, hacker_bucks):
        super().purchase(hacker_bucks)
        self.timeout = datetime.utcnow() + timedelta(minutes=self.ROT_TIMEOUT)

    def to_json(self):
        obj = super().to_json()
        obj.update({
            "timeout": self.timeout,
            "encrypted_message": self.encrypted_message
        })
        return obj

    def generate_enc_message(self):
        # Pick a random shift b/w 1 and 25
        self.key = random.randint(1, 25)
        # Pick a random movie quote
        self.message = MOVIE_QUOTES[random.randint(0, len(MOVIE_QUOTES))].strip().lower()
        # Generate the crypto message
        self.encrypted_message = self.shifttext(self.key, self.message)

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
        # Has the timeout expired?
        check = datetime.utcnow()
        if check > self.timeout:
            # Reset the timeout
            self.timeout = datetime.utcnow() + timedelta(minutes=self.ROT_TIMEOUT)
            return False

        if answer.strip().lower() == self.message:
            self.num_solved += 1
            if self.num_solved >= self.num_to_solve:
                self.solved = True
            else:
                # Create a new one to solve
                self.generate_enc_message()
            return True
        return False

Session.register_challenge(Rot)
