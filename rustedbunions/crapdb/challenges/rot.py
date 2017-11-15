import os
import random
import string

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
        self.key = random.randint(1, 25) # pick a random shift b/w 1 and 25
        self.message = MOVIE_QUOTES[random.randint(0, len(MOVIE_QUOTES))].strip().lower()
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
        if answer.strip().lower() == self.message:
            self.solved = True
            return True
        return False

Session.register_challenge(Rot)
