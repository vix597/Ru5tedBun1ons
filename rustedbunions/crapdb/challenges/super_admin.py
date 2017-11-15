from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FLAGS

class SuperAdmin(Challenge):
    meta = ChallengeMetadata(
        challenge_id="super_admin",
        name="Super Admin",
        description="Are you admin tho?",
        price=0,
        value=FLAGS["super_admin_challenge"][1],
        flag=FLAGS["super_admin_challenge"][0]
    )

    def __init__(self):
        super().__init__()
        self.solved = True
        self.purchased = True

    def check(self, answer):
        self.solved = True
        return True

Session.register_challenge(SuperAdmin)
