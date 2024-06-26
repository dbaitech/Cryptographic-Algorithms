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

    @staticmethod
    def add(q, c1, c2):
        return np.add(c1[0], c2[0]) % q, (c1[1] + c2[1]) % q

    @staticmethod
    def multiply_scalar(q, scalar, c):
        return (scalar * c[0]) % q, (scalar * c[1]) % q

    def __get_error(self):
        return int(random.randrange(-32, 32))

    def __get_random_vector(self):
        s = np.array([])
        for i in range(self.n):
            s = np.append(s, random.randint(0, self.q - 1))
        return s
