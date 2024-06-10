import math
import random
import numpy as np
from elgamal import ElGamal
from LWE.lwe import LWESecretKey

g = 7  # generator
q = 2083  # prime


def regular_elgamal():
    print('------------------------------------------------')
    print('Regular Elgamal Encryption and Decryption Example:')
    elgamal_client = ElGamal(g, q)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    message = 2081  # must be from 0 to q - 2
    compare_message = message % (q - 1)
    y = random.randint(1, q - 1)
    ciphertext = elgamal_client.encrypt(message, public_key, y)
    decrypted_message = elgamal_client.decrypt(ciphertext, private_key)

    print(f'Message: {compare_message}')
    print(f'Ciphertext: {ciphertext}')
    print(f'Decrypted Ciphertext: {decrypted_message}')
    assert compare_message == decrypted_message


# regular_elgamal()


def exponential_elgamal():
    print('------------------------------------------------')
    print('Exponential Elgamal Encryption and Decryption Example:')
    elgamal_client = ElGamal(g, q, exponential=True)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    message = 6246  # must be from 0 to q - 2
    compare_message = message % (q - 1)
    y = random.randint(1, q - 1)
    ciphertext = elgamal_client.encrypt(message, public_key, y)
    decrypted_message = elgamal_client.decrypt(ciphertext, private_key)

    print(f'Message: {compare_message}')
    print(f'Ciphertext: {ciphertext}')
    print(f'Decrypted Ciphertext: {decrypted_message}')
    assert compare_message == decrypted_message


# exponential_elgamal()


# exponential ElGamal: adding ciphertexts
def exp_elgamal_addition():
    print('------------------------------------------------')
    print('Exponential Elgamal Addition Example:')
    elgamal_client = ElGamal(g, q, exponential=True)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    m1 = 100023532
    m2 = 322552
    m_sum = (m1 + m2) % (q - 1)
    y = random.randint(1, q - 1)

    exp_c1 = elgamal_client.encrypt(m1, public_key, y)
    exp_c2 = elgamal_client.encrypt(m2, public_key, y)

    added_ciphertexts = elgamal_client.add(exp_c1, exp_c2)
    decrypt_added_ciphertexts = elgamal_client.decrypt(added_ciphertexts, private_key)

    print(f'Message 1: {m1}')
    print(f'Message 2: {m2}')
    print(f'Ciphertext 1: {exp_c1}')
    print(f'Ciphertext 2: {exp_c2}')
    print(f'Added ciphertexts: {added_ciphertexts}')
    print(f'Decrypted ciphertext: {decrypt_added_ciphertexts}')
    print(f'Plaintext Sum: {m_sum}')
    assert decrypt_added_ciphertexts == m_sum


# exp_elgamal_addition()


# exponential ElGamal: multiplying ciphertext with a scalar
def exp_elgamal_scalar_mult():
    print('------------------------------------------------')
    print('Exponential Elgamal Scalar Multiplication Example:')
    elgamal_client = ElGamal(g, q, exponential=True)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    m1 = 994686
    y = random.randint(1, q - 1)

    exp_c1 = elgamal_client.encrypt(m1, public_key, y)

    scalar = 1412414124
    plaintext_mult = (scalar * m1) % (q - 1)

    multiplied_ciphertext = elgamal_client.multiply_by_scalar(scalar, exp_c1)
    decrypt_mult_ciphertext = elgamal_client.decrypt(multiplied_ciphertext, private_key)

    print(f'Message: {m1}')
    print(f'Scalar: {scalar}')
    print(f'Encrypted Message: {exp_c1}')
    print(f'Decrypted Message: {decrypt_mult_ciphertext}')
    print(f'Plaintext Multiplication: {plaintext_mult}')
    assert plaintext_mult == decrypt_mult_ciphertext


# exp_elgamal_scalar_mult()


def elgamal_linear_combo():
    print('------------------------------------------------')
    print('Exponential Elgamal Linear Combination Example:')

    elgamal_client = ElGamal(g, q, exponential=True)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    m1 = 1412432958520835235252
    scalar = 1351532234543252352
    m2 = 54742125342642698709468
    m_sum = (scalar * m1 + m2) % (q - 1)

    y1 = random.randint(1, q - 1)
    exp_c1 = elgamal_client.encrypt(m1, public_key, y1)
    y2 = random.randint(1, q - 1)
    exp_c2 = elgamal_client.encrypt(m2, public_key, y2)

    multiplied_ciphertext = elgamal_client.multiply_by_scalar(scalar, exp_c1)
    summed_ciphertexts = elgamal_client.add(multiplied_ciphertext, exp_c2)
    decrypt_l_c_ciphertext = elgamal_client.decrypt(summed_ciphertexts, private_key)

    print(f'Message 1 : {m1}, Scalar: {scalar}, Encrypted Message 1: {exp_c1}')
    print(f'Multiplied ciphertext: {multiplied_ciphertext}')
    print(f'Message 2: {m2}, Encrypted Message 2: {exp_c2}')
    print(f'Summed ciphertexts: {summed_ciphertexts}')
    print(f'Decrypted Message: {decrypt_l_c_ciphertext}, Plaintext Linear Combination: {m_sum}')
    assert m_sum == decrypt_l_c_ciphertext


# elgamal_linear_combo()

def mini_HE_SimplePIR():
    print('------------------------------------------------')
    print('Exponential Elgamal Linear Combination Example:')

    lwe_p = 26
    lwe_q = 2 ** 32
    lwe_n = 2
    lwe_client = LWESecretKey(lwe_p, lwe_q, lwe_n)
    lwe_private_key = lwe_client.get_secret_key()

    elgamal_client = ElGamal(g, q, exponential=True)
    elg_private_key = elgamal_client.generate_private_key()
    elg_public_key = elgamal_client.generate_public_key(elg_private_key)

    elg_wrapped_lwe_secret_key = [
        elgamal_client.encrypt(int(key), elg_public_key, random.randint(1, elgamal_client.q - 1)) for key in
        lwe_private_key]
    print(f'ElGamal wrapped LWE secret key: {elg_wrapped_lwe_secret_key}')

    m_lwe_key = [(i % (elgamal_client.q - 1)) for i in lwe_private_key]

    database_summed_rows = [5]  # [5, 10, 15, 20, 25]
    print(f'DB summed rows: {database_summed_rows}')
    response = [lwe_client.encrypt(row, lwe_private_key) for row in database_summed_rows]
    print(f'LWE encrypted summed rows: {response}')

    lwe_response = np.empty(len(response), dtype=tuple)
    slim_response = np.empty(len(response), dtype=tuple)
    m_lwe_response = np.empty(len(response), dtype=tuple)

    for i, (a, c) in enumerate(response):
        y = random.randint(1, elgamal_client.q - 1)
        elg_result = elgamal_client.encrypt(int(c), elg_public_key, y)
        lwe_result = c
        m_lwe_result = c % (elgamal_client.q - 1)

        for a_j, s_j, lwe_key_j, m_lwe_key_j in zip(a, elg_wrapped_lwe_secret_key, lwe_private_key, m_lwe_key):
            lwe_a_j_key_j_product = a_j * lwe_key_j
            lwe_result -= lwe_a_j_key_j_product

            m_lwe_a_j_key_j_product = a_j * m_lwe_key_j
            m_lwe_result -= m_lwe_a_j_key_j_product

            elg_a_j_s_j_product = elgamal_client.multiply_by_scalar((elgamal_client.q - 1 - int(a_j)), s_j)
            elg_result = elgamal_client.add(elg_result, elg_a_j_s_j_product)

        lwe_base = math.floor(lwe_client.q / lwe_client.p)  # round to the nearest multiple of floor(q/p)
        lwe_response[i] = round((lwe_result % lwe_client.q) / lwe_base) % lwe_client.p

        m_lwe_response[i] = m_lwe_result % (elgamal_client.q)

        elg_base = math.floor(elgamal_client.q / lwe_client.p)
        slim_response[i] = round(elgamal_client.decrypt(elg_result, elg_private_key)/elg_base) % lwe_client.p
    # elg_decrypt_slim_response = [(elgamal_client.decrypt(i, elg_private_key)) for i in slim_response]
    print(f'LWE response: {lwe_response}')
    m_prime = pow(g, int(m_lwe_response[0]), elgamal_client.q)
    for i in range(elgamal_client.q - 1):  # searching from 0 to q - 2
        if pow(g, i, elgamal_client.q) == m_prime:
            m_lwe_final_result = i
    print(f'Modified LWE response: {m_lwe_response}, '
          f'g^m_lwe_response mod elg_q = {m_prime}, '
          f'log_g m_prime = {m_lwe_final_result}, '
          f'mod plaintext p: {m_lwe_final_result % lwe_client.p}')
    print(f'Slim ElGamal response: {slim_response}')
    # print(f'Decrypted Slim ElGamal response: {elg_decrypt_slim_response}')

mini_HE_SimplePIR()
