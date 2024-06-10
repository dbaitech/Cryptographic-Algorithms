import client
import server
import numpy as np


def main():
    p = 26  # plaintext modulus
    lwe_q = 2 ** 32  # ciphertext modulus
    lwe_n = 2  # 840 # dimension of secret key
    elgamal_g = 7
    elgamal_q = 2083
    num_rows = 5
    num_cols = 5
    database = np.array([[1, 2, 3, 4, 5],
                         [6, 7, 8, 9, 10],
                         [11, 12, 13, 14, 15],
                         [16, 17, 18, 19, 20],
                         [21, 22, 23, 24, 25]])
    svr = server.Server(database, num_rows, num_cols, lwe_q, elgamal_g, elgamal_q)
    cl = client.Client(num_rows, num_cols, p, lwe_q, lwe_n, elgamal_g, elgamal_q)

    # querying element
    query_row = 4
    query_col = 4

    assert 0 <= query_row < num_rows
    assert 0 <= query_col < num_cols

    enc_query = cl.generate_encrypted_query(query_row, query_col)
    svr_response = svr.process_enc_query(enc_query, cl.elgamal_public_key, cl.get_elg_wrap_lwe_secret_key())
    queried_element = cl.receive_db_response(svr_response)

    print(f'Element at ({query_row}, {query_col}) is {queried_element}')
    assert queried_element == database[query_row][query_col]



if __name__ == '__main__':
    main()
