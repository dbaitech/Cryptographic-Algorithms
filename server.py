import numpy as np
import random
from ElGamal.elgamal import ElGamal
from LWE.lwe import LWESecretKey


class Server:
    def __init__(self, db, num_rows, num_cols, lwe_q, elgamal_g, elgamal_q):
        self.db = db
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.lwe_q = lwe_q
        self.elgamal = ElGamal(elgamal_g, elgamal_q, exponential=True)
        self.slim_response = None

    def process_enc_query(self, enc_query, elg_public_key, elg_wrapped_lwe_secret_key):
        response = np.empty(self.num_rows, dtype=tuple)
        for i, db_row in enumerate(self.db):
            row_sum = (0, 0)
            for db_cell, query_col in zip(db_row, enc_query):
                row_sum = LWESecretKey.add(self.lwe_q, row_sum,
                                           LWESecretKey.multiply_scalar(self.lwe_q, db_cell, query_col))
            response[i] = row_sum
        # return response
        return self.__slim_response(response, elg_public_key, elg_wrapped_lwe_secret_key)

    def __slim_response(self, response, elg_public_key, elg_wrapped_lwe_secret_key):
        slim_response = np.empty(response.shape, dtype=tuple)

        for i, (a, c) in enumerate(response):
            y_1 = random.randint(1, self.elgamal.q - 1)
            enc_c = self.elgamal.encrypt(int(c), elg_public_key, y_1)

            y_2 = random.randint(1, self.elgamal.q - 1)
            sum_a_j_s_j = self.elgamal.encrypt(0, elg_public_key, y_2) # set it to 0 in ElGamal

            for a_j, s_j in zip(a, elg_wrapped_lwe_secret_key):
                sum_a_j_s_j = self.elgamal.add(sum_a_j_s_j,
                                               self.elgamal.multiply_by_scalar(int(a_j), s_j))  # sum(q - a_i, s_i)

            slim_response[i] = self.elgamal.add(enc_c,
                                                self.elgamal.multiply_by_scalar(-1, sum_a_j_s_j))  # c + sum(q - a_i, s_i)
        self.slim_response = slim_response
        return slim_response
