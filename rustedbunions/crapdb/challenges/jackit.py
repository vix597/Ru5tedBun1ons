from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FlagGenerator

FLAGS = FlagGenerator.generate_flags()


class JackIt(Challenge):
    meta = ChallengeMetadata(
        challenge_id="jackit_game",
        name="Game Programming Challenge",
        description="2D Side-scrolling game where you modify code to win",
        price=0,
        value=153,
        flag="",
        sort_order=1,
        js_function="jackIt()"
    )

    def __init__(self):
        super().__init__()
        self.solved = True
        self.purchased = True

    def check(self, answer):
        self.solved = True
        return True


Session.register_challenge(JackIt)
