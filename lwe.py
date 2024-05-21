import numpy as np
import random
import math

q = 211  # prime to give the set of integers mod q
n = 14  # dimension of vectors
epsilon = 0.005  # small arbitrary constant
m = int((1 + epsilon) * (n + 1) * np.log(q))


def get_random_int(max):
    return int(random.randrange(max))


def get_random_vector():
    s = np.array([])
    for i in range(n):
        s = np.append(s, get_random_int(q))
    return s


def alpha(n):
    return 1 / (np.sqrt(n) * (np.log(n))**2)


def get_chi_distribution_sample(n):
    beta = alpha(n)
    normal_sample = np.random.normal(0, beta / np.sqrt(2 * np.pi))
    # reduced_sample = normal_sample % 1
    sample_mod_q = normal_sample % q
    return sample_mod_q


def get_private_key():
    return get_random_vector()


def get_public_key(s):
    public_key = []
    test = []
    e_list = []
    for i in range(m):
        a_i = get_random_vector()
        e_i = get_chi_distribution_sample(n)
        b_i = np.inner(a_i, s) + e_i
        test.append(np.inner(a_i, s))
        e_list.append(e_i)
        public_key.append((a_i, b_i))
    print(e_list)
    return public_key, test, e_list


def get_random_subset_of_m():
    size = get_random_int(m)
    return random.sample(range(m), size)


def encrypt_bit(public_key, x, test, e_list):
    S = get_random_subset_of_m()
    a_sum = 0
    b_sum = 0
    test_sum = 0
    e_sum = 0
    for i in S:
        a_i = public_key[i][0]
        a_sum += a_i
        b_i = public_key[i][1]
        b_sum += b_i
        test_sum += test[i]
        e_sum +=  e_list[i]
    if x == 1:
        b_sum += math.floor(q / 2)
    print("sum of all <a_i,s> for i is: ", test_sum)
    print("e sum: ", e_sum)
    return a_sum, b_sum

def decrypt_bit(private_key, a, b):
    print("<a,s> is: ", np.inner(a, private_key))
    result = b - np.inner(a, private_key)
    print("Discrepancy: ", result)
    if abs(result) < math.floor(q / 4):
        return 0
    else:
        return 1

sk = get_private_key()
pk, test_list, e_i_list = get_public_key(sk)
x = 0
encrypted_bit = encrypt_bit(pk, x, test_list, e_i_list)
print(decrypt_bit(sk, encrypted_bit[0], encrypted_bit[1]))