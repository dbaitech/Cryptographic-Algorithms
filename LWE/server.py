import numpy as np
from lwe import LWESecretKey


class Server:
    def __init__(self, db, num_rows, num_cols, q):
        self.db = db
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.q = q

    def process_enc_query(self, enc_query):
        response = np.empty(self.num_rows, dtype=tuple)
        for i, db_row in enumerate(self.db):
            row_sum = (0, 0)
            for db_cell, query_col in zip(db_row, enc_query):
                row_sum = LWESecretKey.add(self.q, row_sum, LWESecretKey.multiply_scalar(self.q, db_cell, query_col))
            response[i] = row_sum
        return response
