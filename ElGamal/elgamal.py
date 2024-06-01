import random
import math


class ElGamal:
    def __init__(self, g, q):
        self.g = g  # generator
        self.q = q  # modulus

    def generate_public_key(self, private_key):  # generator, order of cyclic group
        h = pow(self.g, private_key, self.q)
        return self.g, self.q, h

    def generate_private_key(self):
        return random.randint(1, self.q)

    @staticmethod
    def encrypt(message, public_key, y, exponential=False):
        g, q, h = public_key
        assert 1 <= y <= q - 1
        shared_secret = pow(h, y, q)
        c1 = pow(g, y, q)
        if exponential:
            c2 = (pow(g, message, q) * shared_secret) % q
        else:
            c2 = (message * shared_secret) % q
        return c1, c2

    def decrypt(self, ciphertext, private_key, exponential=True):
        c1, c2 = ciphertext
        shared_secret = pow(c1, -1 * private_key, self.q)
        # if exponential:
        #     return round(math.log(c2 * shared_secret, g))
        return (c2 * shared_secret) % self.q
