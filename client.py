import math

import numpy as np
import random
from LWE.lwe import LWESecretKey
from ElGamal.elgamal import ElGamal


class Client:
    def __init__(self, db_num_rows: int, db_num_cols: int, p, lwe_q=2 ** 32, n=840, g=7, elgamal_q=2083):
        self.db_num_rows = db_num_rows
        self.db_num_cols = db_num_cols
        self.lwe = LWESecretKey(p, lwe_q, n)
        self.lwe_secret_key = self.lwe.get_secret_key()
        self.elgamal = ElGamal(g, elgamal_q, exponential=True)
        self.elgamal_private_key = self.elgamal.generate_private_key()
        self.elgamal_public_key = self.elgamal.generate_public_key(self.elgamal_private_key)
        self.col = None
        self.row = None
        self.query = None
        self.lwe_query = None
        self.elg_wrapped_lwe_key = None
        self.db_response = None
        self.decrypted_element = None

    def generate_encrypted_query(self, row: int, col: int):
        self.__set_query_coordinates(row, col)
        self.__generate_query()
        self.__generate_lwe_query()
        return self.lwe_query

    def get_elg_wrap_lwe_secret_key(self):
        elg_wrapped_lwe_key = np.empty(self.lwe_secret_key.shape, dtype=tuple)
        for i, s_i in enumerate(self.lwe_secret_key):
            y = random.randint(1, self.elgamal.q - 1)
            elg_wrapped_lwe_key[i] = self.elgamal.encrypt(int(s_i), self.elgamal_public_key, y)
            assert (s_i % (self.elgamal.q - 1)) == self.elgamal.decrypt(elg_wrapped_lwe_key[i], self.elgamal_private_key)
        self.elg_wrapped_lwe_key = elg_wrapped_lwe_key
        return self.elg_wrapped_lwe_key

    def receive_db_response(self, response):
        self.db_response = response
        row_response = self.db_response[self.row]  # get only desired row
        # decrypted_response = self.lwe.decrypt(row_response, self.lwe_secret_key)
        decrypted_response = self.elgamal.decrypt(row_response, self.elgamal_private_key)
        base = math.floor(self.elgamal.q / self.lwe.p)  # round to the nearest multiple of floor(q/p)
        self.decrypted_element = (round(decrypted_response / base)) % self.lwe.p
        return self.decrypted_element

    def __set_query_coordinates(self, row, col):
        self.row = row
        self.col = col

    def __generate_query(self):
        query_vector = np.zeros(self.db_num_cols)
        query_vector[self.col] = 1
        self.query = query_vector

    def __generate_lwe_query(self):
        lwe_query = np.empty(self.db_num_cols, dtype=tuple)
        for i, x in enumerate(self.query):
            lwe_query[i] = self.lwe.encrypt(x, self.lwe_secret_key)
        self.lwe_query = lwe_query
