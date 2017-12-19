from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FLAGS

class Genetic(Challenge):
    meta = ChallengeMetadata(
        challenge_id="genetic",
        name="Nice Genes",
        description="How fit are you?",
        price=30,
        value=FLAGS["genes"][1],
        flag=FLAGS["genes"][0],
        js_function="geneticGenes()",
        sort_order=5
    )

    def check(self, answer):
        return False

Session.register_challenge(Genetic)
