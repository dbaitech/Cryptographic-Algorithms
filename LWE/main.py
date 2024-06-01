import lwe
import client
import server
import numpy as np


def main():
    p = 10  # plaintext modulus
    q = 2 ** 32  # ciphertext modulus
    n = 840  # dimension of secret key
    database = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    svr = server.Server(database, 3, 3, q)
    cl = client.Client(3, 3, p, q, n)

    # querying element
    query_row = 1
    query_col = 1
    enc_query = cl.generate_encrypted_query(query_row, query_col)
    svr_response = svr.process_enc_query(enc_query)
    queried_element = cl.receive_db_response(svr_response)

    assert queried_element == database[query_row][query_col]
    print(f'Element at ({query_row}, {query_col}) is {queried_element}')


def lwe_test():
    p = 10  # plaintext modulus
    q = 2 ** 32  # ciphertext modulus
    n = 840  # dimension of secret key

    system = lwe.LWESecretKey(p, q, n)

    # basic encrypt and decrypt
    s = system.get_secret_key()
    plaintext_1 = 5

    ciphertext_1 = system.encrypt(plaintext_1, s)
    decrypted_ciphertext = system.decrypt(ciphertext_1, s)

    print(f'Plaintext: {plaintext_1}')
    print(f'Decrypted ciphertext: {decrypted_ciphertext}')
    assert plaintext_1 == decrypted_ciphertext

    # homomorphic addition
    plaintext_2 = 4
    plaintext_sum = (plaintext_1 + plaintext_2) % p

    ciphertext_2 = system.encrypt(plaintext_2, s)
    ciphertext_sum = system.add(q, ciphertext_1, ciphertext_2)
    decrypted_sum = system.decrypt(ciphertext_sum, s)

    print(f'Plaintext sum: {plaintext_1} + {plaintext_2} mod {p} = {plaintext_sum}')
    print(f'Decrypted sum: {decrypted_sum}')
    assert plaintext_sum == decrypted_sum

    # homomorphic multiplication (scalar with the ciphertext)
    plaintext_scalar = 111
    plaintext_product = (plaintext_scalar * plaintext_1) % p

    product = system.multiply_scalar(q, plaintext_scalar, ciphertext_1)
    decrypted_product = system.decrypt(product, s)

    print(f'Plaintext product: {plaintext_scalar} x {plaintext_1} mod {p} = {plaintext_product}')
    print(f'Decrypted product: {decrypted_product}')
    assert plaintext_product == decrypted_product


if __name__ == '__main__':
    main()
