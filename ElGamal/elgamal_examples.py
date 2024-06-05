import random
from elgamal import ElGamal

g = 7  # generator
q = 2083  # prime


def regular_elgamal():
    elgamal_client = ElGamal(g, q)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    message = 2081  # must be from 0 to q - 2
    compare_message = message % q
    y = random.randint(1, q - 1)
    ciphertext = elgamal_client.encrypt(message, public_key, y)
    decrypted_message = elgamal_client.decrypt(ciphertext, private_key)

    print(f'Message: {compare_message}, Ciphertext: {ciphertext}, Decrypted Ciphertext: {decrypted_message}')
    assert compare_message == decrypted_message


# regular_elgamal()


def exponential_elgamal():
    elgamal_client = ElGamal(g, q, exponential=True)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    message = 2082  # must be from 0 to q - 2
    compare_message = message % (q - 1)
    y = random.randint(1, q - 1)
    ciphertext = elgamal_client.encrypt(message, public_key, y)
    decrypted_message = elgamal_client.decrypt(ciphertext, private_key)

    print(f'Message: {compare_message}, Ciphertext: {ciphertext}, Decrypted Ciphertext: {decrypted_message}')
    assert compare_message == decrypted_message


# exponential_elgamal()


# exponential ElGamal: adding ciphertexts
def exp_elgamal_addition():
    elgamal_client = ElGamal(g, q, exponential=True)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    m1 = 7
    m2 = 3
    m_sum = m1 + m2 % q
    y = random.randint(1, q - 1)

    exp_c1 = elgamal_client.encrypt(m1, public_key, y)
    exp_c2 = elgamal_client.encrypt(m2, public_key, y)

    added_ciphertexts = elgamal_client.add(exp_c1, exp_c2)
    decrypt_added_ciphertexts = elgamal_client.decrypt(added_ciphertexts, private_key)

    print(f'Message 1: {m1}, Message 2: {m2}, '
          f'Ciphertext 1: {exp_c1}, Ciphertext 2: {exp_c2}, '
          f'Added ciphertexts: {added_ciphertexts}, '
          f'Decrypted ciphertext: {decrypt_added_ciphertexts}, '
          f'Plaintext Sum: {m_sum}')
    assert decrypt_added_ciphertexts == m_sum


# exp_elgamal_addition()


# exponential ElGamal: multiplying ciphertext with a scalar
def exp_elgamal_scalar_mult():
    elgamal_client = ElGamal(g, q, exponential=True)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    m1 = 2
    y = random.randint(1, q - 1)

    exp_c1 = elgamal_client.encrypt(m1, public_key, y)

    scalar = 1039
    plaintext_mult = (scalar * m1) % q

    multiplied_ciphertext = elgamal_client.multiply_by_scalar(scalar, exp_c1)
    decrypt_mult_ciphertext = elgamal_client.decrypt(multiplied_ciphertext, private_key)

    print(f'Message: {m1}, Scalar: {scalar}, Encrypted Message: {exp_c1}, '
          f'Decrypted Message: {decrypt_mult_ciphertext}, Plaintext Multiplication: {plaintext_mult}')
    assert plaintext_mult == decrypt_mult_ciphertext


# exp_elgamal_scalar_mult()

def elgamal_linear_combo():
    elgamal_client = ElGamal(g, q, exponential=True)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    m1 = 7
    scalar = 500
    m2 = 10
    m_sum = scalar * m1 + m2 % q

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
    print(f'Decrypted Message: {decrypt_l_c_ciphertext}, Plaintext Linear Combination: {m_sum % q}')
    assert m_sum % q == decrypt_l_c_ciphertext


elgamal_linear_combo()
