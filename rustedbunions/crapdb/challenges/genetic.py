import random
import string

from core.challenge import Challenge, ChallengeMetadata
from core.session import Session
from flags import FLAGS

class Genetic(Challenge):
    chars = string.ascii_letters + string.digits + string.punctuation
    password_len = 9

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

    def __init__(self):
        super().__init__()
        random.seed()
        self.password = ""
        self.score = 0
        for _ in range(self.password_len):
            self.password += self.chars[random.randint(0, len(self.chars) - 1)]
        print("Password: ", self.password)

    def to_json(self):
        obj = super().to_json()
        obj.update({
            "score": self.score
        })
        return obj

    def get_fitness(self, answer):
        score = 0
        for i, c in enumerate(answer):
            if self.password[i] == c:
                score += 1
        self.score = (score / len(self.password)) * 100
        if self.score == 100:
            # Only solved when the score is 100
            self.solved = True

    def check(self, answer):
        answer = answer.strip()
        self.get_fitness(answer)
        return True

#Session.register_challenge(Genetic)
