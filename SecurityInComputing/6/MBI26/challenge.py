import string
import random

class AuthChallenge:
    def random_challenge(self):
        return ''.join([random.choice(string.ascii_letters) for i in range(8)])
    
