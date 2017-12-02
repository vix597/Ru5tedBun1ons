from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FLAGS

class Xor(Challenge):
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
        # NOTE: Change before deploy
        self.message = "this is not going to be the message used for deploy " + self.meta.flag
        self.key = "key" * (int(len(self.message) / 3) + 1)
        self.cipher = self.sxor(self.key, self.message)

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
        '''
        Don't need to check, the flag is in the message.
        '''
        self.solved = True
        return True

Session.register_challenge(Xor)
