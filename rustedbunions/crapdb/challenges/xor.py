import string
import random

from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FLAGS

class Xor(Challenge):
    alnum = string.ascii_letters + string.digits

    meta = ChallengeMetadata(
        challenge_id="xor",
        name="XOR",
        description="The most exclusive 'or'",
        price=25,
        value=FLAGS["xor_challenge"][1],
        flag=FLAGS["xor_challenge"][0]
    )

    def __init__(self):
        super().__init__()
        random.seed() # uses current system time

        # NOTE: Change before deploy
        self.message = "the quick brown fox jumps over the lazy dog"
        self.key = ""
        self.cipher_key = None
        self.generate_key()
        self.cipher = self.sxor(self.cipher_key, self.message)

    def generate_key(self):
        key_len = 6
        for _ in range(key_len):
            self.key += self.alnum[random.randint(0, (len(self.alnum) - 1))]
        self.cipher_key = str(self.key) * (int(len(self.message) / len(self.key)) + 1)

    def sxor(self, s1, s2):
        # convert strings to a list of character pair tuples
        # go through each tuple, converting them to ASCII code (ord)
        # perform exclusive or on the ASCII code
        # then convert the result back to ASCII (chr)
        # merge the resulting array of characters as a string
        return bytes([(ord(a) ^ ord(b)) for a, b in zip(s1, s2)])

    def to_json(self):
        obj = super().to_json()
        obj.update({
            "cipher_text": str(self.cipher.hex())
        })
        return obj

    def check(self, answer):
        if answer.strip() == self.key or answer.strip() == self.cipher_key:
            self.solved = True
            return True
        return False

Session.register_challenge(Xor)
