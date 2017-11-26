import random
import hashlib

from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FLAGS

class BrutalForce(Challenge):
    meta = ChallengeMetadata(
        challenge_id="brutal_force",
        name="Brutal Force",
        description="Use the force",
        price=6,
        value=FLAGS["brutal_force_challenge"][1],
        flag=FLAGS["brutal_force_challenge"][0]
    )

    def __init__(self):
        super().__init__()
        random.seed() # uses current system time
        self.pin = random.randint(666, 9999) # The user's random PIN number
        self.pin_hash = hashlib.sha256(str(self.pin).encode('utf-8')).hexdigest()

    def to_json(self):
        obj = super().to_json()
        obj.update({
            "pin_hash": self.pin_hash
        })
        return obj

    def check(self, answer):
        try:
            answer = int(answer)
            if answer < 1 or answer > 9999:
                return False
        except ValueError:
            return False
        if answer == self.pin:
            self.solved = True
            return True
        return False

Session.register_challenge(BrutalForce)
