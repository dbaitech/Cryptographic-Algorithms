import numpy as np
import random
import math


class LWESecretKey:
    def __init__(self, p, q, n):
        self.p = p
        self.q = q
        self.n = n

    def get_random_int(self, max):
        return int(random.randrange(max))

    def get_error(self):
        return int(random.randrange(-32, 32))

    def get_random_vector(self):
        s = np.array([])
        for i in range(self.n):
            s = np.append(s, self.get_random_int(self.q))
        return s

    def get_secret_key(self):
        return self.get_random_vector()

    def encrypt(self, plaintext, secret):
        a = self.get_random_vector()
        e = self.get_error()
        c = (np.inner(a, secret) + e + (math.floor(self.q / self.p) * plaintext)) % self.q
        return a, c

    def decrypt(self, ciphertext, secret):
        a = ciphertext[0]
        c = ciphertext[1]
        difference = (c - np.inner(a, secret)) % self.q
        base = math.floor(self.q / self.p)  # round to the nearest multiple of floor(q/p)
        return (round(difference / base)) % self.p

    def add(self, c1, c2):
        return c1[0] + c2[0], c1[1] + c2[1]


p = 2  # plaintext modulus
q = 2 ** 32  # ciphertext modulus
n = 840  # dimension of secret key

system = LWESecretKey(p, q, n)

# basic encrypt and decrypt
s = system.get_secret_key()
plaintext_1 = 1

ciphertext_1 = system.encrypt(plaintext_1, s)
decrypted_ciphertext = system.decrypt(ciphertext_1, s)

print('Plaintext: ', plaintext_1)
print('Decrypted ciphertext: ', decrypted_ciphertext)
assert plaintext_1 == decrypted_ciphertext

# homomorphic addition
plaintext_2 = 1
plaintext_sum = (plaintext_1 + plaintext_2) % p

ciphertext_2 = system.encrypt(plaintext_2, s)
sum = system.add(ciphertext_1, ciphertext_2)
decrypted_sum = system.decrypt(sum, s)

print('Plaintext sum: ', plaintext_sum)
print('Decrypted sum: ', decrypted_sum)
assert plaintext_sum == decrypted_sum
