
from core.challenge import Challenge, ChallengeMetadata
from core.session import Session, AuthenticatedSession
from flags import FLAGS

class PaidContent(Challenge):
    meta = ChallengeMetadata(
        challenge_id="paid_content",
        name="Paid Content",
        description="Pay for things you want!",
        price=25,
        value=FLAGS["paid_content_challenge"][1],
        flag=FLAGS["paid_content_challenge"][0]
    )

    def check(self, answer):
        if isinstance(answer, AuthenticatedSession):
            if answer.paid:
                self.solved = True
                return True
        return False

Session.register_challenge(PaidContent)
