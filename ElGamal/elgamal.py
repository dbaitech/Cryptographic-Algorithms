import random


class ElGamal:
    def __init__(self, g, q):
        self.g = g  # generator
        self.q = q  # prime

    def encrypt(self, message, public_key, y):
        g, q, h = public_key
        assert 1 <= y <= q - 1
        shared_secret = pow(h, y, q)
        c1 = pow(g, y, q)
        c2 = (message * shared_secret) % self.q
        return c1, c2

    def decrypt(self, ciphertext, private_key):
        c1, c2 = ciphertext
        shared_secret = pow(c1, -1 * private_key, self.q)
        return (c2 * shared_secret) % self.q

    def generate_public_key(self, private_key):  # generator, order of cyclic group
        h = pow(self.g, private_key, self.q)
        return self.g, self.q, h

    def generate_private_key(self):
        return random.randint(1, self.q)
