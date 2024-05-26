import numpy as np
import lwe


class Client:
    def __init__(self, db_num_rows: int, db_num_cols: int, p=2, q=2 ** 32, n=840):
        self.db_num_rows = db_num_rows
        self.db_num_cols = db_num_cols
        self.lwe = lwe.LWESecretKey(p, q, n)
        self.secret_key = self.lwe.get_secret_key()
        self.col = None
        self.row = None
        self.query = None
        self.enc_query = None
        self.db_response = None
        self.decrypted_db_response = None
        self.queried_element = None

    def generate_encrypted_query(self, row: int, col: int):
        self.__set_query_coordinates(row, col)
        self.__generate_query()
        enc_query = np.empty(self.db_num_cols, dtype=tuple)
        for i, x in enumerate(self.query):
            enc_query[i] = self.lwe.encrypt(x, self.secret_key)
        self.enc_query = enc_query
        return self.enc_query

    def receive_db_response(self, response):
        self.db_response = response
        decrypted_response = np.zeros(self.db_num_rows)
        for i, row in enumerate(self.db_response):
            decrypted_response[i] = self.lwe.decrypt(row, self.secret_key)
        self.decrypted_db_response = decrypted_response
        return self.__get_queried_element()

    def __set_query_coordinates(self, row, col):
        self.row = row
        self.col = col

    def __generate_query(self):
        query_vector = np.zeros(self.db_num_cols)
        query_vector[self.col] = 1
        self.query = query_vector

    def __get_queried_element(self):
        self.queried_element = self.decrypted_db_response[self.row]
        return int(self.queried_element)


