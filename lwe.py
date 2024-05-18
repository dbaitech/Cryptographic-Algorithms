import numpy as np
import random
import math

q = 211  # prime to give the set of integers mod q
n = 11  # dimension of vectors
e = 3  # small arbitrary constant
m = int((1 + e) * (n + 1) * math.log(q, 10))


def get_random_int(max):
    return int(random.randrange(max))


def get_random_vector():
    s = np.array([])
    for i in range(n):
        s = np.append(s, get_random_int(q))
    return s


def alpha(n):
    return 1 / (np.sqrt(n) * np.log(n))


def get_chi_distribution_sample(n):
    beta = alpha(n)
    normal_sample = np.random.normal(0, beta / np.sqrt(2 * np.pi))
    reduced_sample = normal_sample % 1
    return reduced_sample


def get_private_key():
    return get_random_vector()


def get_public_key(s):
    public_key = []
    for i in range(m):
        a = get_random_vector()
        e = get_chi_distribution_sample(n)
        b = (np.inner(a, s) / q) + e
        public_key.append((a, b))
    return public_key


def get_random_subset_of_m():
    size = get_random_int(m)
    return random.sample(range(m), size)


def encrypt_bit(public_key, x):
    S = get_random_subset_of_m()
    a_sum = 0
    b_sum = 0
    for i in S:
        a_i = public_key[i][0]
        a_sum += a_i
        b_i = public_key[i][1]
        b_sum += b_i
    return a_sum, (x / 2) + b_sum

def decrypt_bit(private_key, a, b):
    result = b - (np.inner(a, private_key) / q)
    if abs(result) < 1/4:
        return 0
    else:
        return 1

sk = get_private_key()
pk = get_public_key(sk)
x = 0
encrypted_bit = encrypt_bit(pk, x)
print(decrypt_bit(sk, encrypted_bit[0], encrypted_bit[1]))