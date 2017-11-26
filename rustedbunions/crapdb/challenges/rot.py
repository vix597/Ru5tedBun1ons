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

        # Solve 50 of them to win
        self.num_to_solve = 50

        # They will have 1 minute to solve from purchase
        self.timeout = None

        # Number solved so far
        self.num_solved = 0

        # Number of seconds remaining to solve
        self.remaining_time = 0

        self.key = 0
        self.message = ""
        self.encrypted_message = ""

    def purchase(self, hacker_bucks):
        return_bucks = super().purchase(hacker_bucks)
        if not self.purchased:
            self.reset()
        return return_bucks

    def reset(self):
        now = datetime.utcnow()
        self.timeout = now + timedelta(minutes=self.ROT_TIMEOUT)
        self.remaining_time = (self.timeout - now).total_seconds()
        self.num_solved = 0
        self.generate_enc_message()

    def is_expired(self):
        if self.timeout:
            self.remaining_time = (self.timeout - datetime.utcnow()).total_seconds()
            print("is_expired() - Remaining Time: ", self.remaining_time)
            if self.remaining_time <= 0:
                return True
        return False

    def update(self):
        if self.is_expired():
            print("*****TIMER EXPIRED!")
            self.reset()
        elif self.timeout is None:
            self.reset()

    def to_json(self):
        obj = super().to_json()

        self.update()

        obj.update({
            "num_to_solve": self.num_to_solve,
            "num_solved": self.num_solved,
            "remaining_time": self.remaining_time,
            "encrypted_message": self.encrypted_message
        })
        return obj

    def generate_enc_message(self):
        # Pick a random shift b/w 1 and 25
        self.key = random.randint(1, 25)
        # Pick a random movie quote
        self.message = MOVIE_QUOTES[random.randint(0, len(MOVIE_QUOTES) - 1)].strip().lower()
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
        # Update will only change the message if the timer is expired
        self.update()

        if answer.strip().lower() == self.message:
            self.num_solved += 1
            if self.num_solved >= self.num_to_solve:
                self.solved = True
            else:
                # Create a new one to solve
                self.generate_enc_message()
            return True
        else:
            print("\"", answer.strip().lower(), "\" != \"", self.message, "\"", sep='')
        return False

Session.register_challenge(Rot)
