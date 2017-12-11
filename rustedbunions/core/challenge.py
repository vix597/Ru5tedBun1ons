from core.util import ObjectId

class ChallengeNotSolvedError(Exception):
    pass

class NotEnoughHackerBucksError(Exception):
    pass

class ChallengeMetadata:

    def __init__(self, price=0, value=0, flag="", challenge_id="", name="", description="",
                 js_function="", sort_order=0):
        self.price = price
        self.value = value
        self.flag = flag
        self.challenge_id = challenge_id
        self.name = name
        self.description = description
        self.js_function = js_function
        self.sort_order = sort_order

    def to_json(self):
        # Flag not included to remain secret
        return {
            "price": self.price,
            "value": self.value,
            "challenge_id": self.challenge_id,
            "name": self.name,
            "description": self.description,
            "js_function": self.js_function,
            "sort_order": self.sort_order
        }

class Challenge:
    '''
    Base class for challenge
    '''

    meta = None

    def __init__(self):
        self.oid = ObjectId()
        self.solved = False
        self.purchased = False

    def to_json(self):
        return {
            "oid": self.oid,
            "meta": self.meta.to_json(),
            "solved": self.solved,
            "purchased": self.purchased
        }

    def purchase(self, hacker_bucks):
        if self.purchased:
            return hacker_bucks
        if hacker_bucks >= self.meta.price:
            self.purchased = True
            hacker_bucks -= self.meta.price
            return hacker_bucks
        raise NotEnoughHackerBucksError("{} requires ${} hacker bucks to play".format(
            self.meta.name,
            self.meta.price
        ))

    def from_other_challenge(self, other):
        self.solved = other.solved
        self.purchased = other.purchased

    def check(self, answer):
        '''
        Check the answer for a challenge. Returns true or false
        '''
        raise NotImplementedError()

    def get_flag(self):
        '''
        Returns the flag if the challenge has been solved
        '''
        if self.solved:
            return self.meta.flag
        raise ChallengeNotSolvedError("{} challenge has not been solved".format(self.meta.name))
