from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FlagGenerator

FLAGS = FlagGenerator.generate_flags()


class SentenceBot(Challenge):
    meta = ChallengeMetadata(
        challenge_id="sentence_bot",
        name="Sentence Bot",
        description="RE The Flag",
        price=0,
        value=FLAGS["sentence_bot_challenge"][1],
        flag=FLAGS["sentence_bot_challenge"][0],
        sort_order=0,
        js_function="sentenceBot()"
    )

    def __init__(self):
        super().__init__()
        self.solved = True
        self.purchased = True

    def check(self, answer):
        self.solved = True
        return True


Session.register_challenge(SentenceBot)
