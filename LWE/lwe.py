import numpy as np
import random
import math


class LWESecretKey:
    def __init__(self, p, q, n):
        self.p = p
        self.q = q
        self.n = n

    def get_secret_key(self):
        return self.__get_random_vector()

    def encrypt(self, plaintext, secret):
        a = self.__get_random_vector()
        e = self.__get_error()
        c = (np.inner(a, secret) + e + (math.floor(self.q / self.p) * plaintext)) % self.q
        return a, c

    def decrypt(self, ciphertext, secret):
        a = ciphertext[0]
        c = ciphertext[1]
        difference = (c - np.inner(a, secret)) % self.q
        base = math.floor(self.q / self.p)  # round to the nearest multiple of floor(q/p)
        return (round(difference / base)) % self.p

    def add(self, c1, c2):
        return np.add(c1[0], c2[0]) % self.q, (c1[1] + c2[1]) % self.q

    def multiply_scalar(self, scalar, c):
        return (scalar * c[0]) % self.q, (scalar * c[1]) % self.q

    def __get_random_int(self, max):
        return int(random.randrange(max))

    def __get_error(self):
        return int(random.randrange(-32, 32))

    def __get_random_vector(self):
        s = np.array([])
        for i in range(self.n):
            s = np.append(s, self.__get_random_int(self.q))
        return s
