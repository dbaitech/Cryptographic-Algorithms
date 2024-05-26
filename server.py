import numpy as np
import lwe


class Server:
    def __init__(self, db, num_rows, num_cols, p, q, n):
        self.db = db
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.p = p
        self.q = q
        self.n = n
        self.lwe = lwe.LWESecretKey(p, q, n)

    def process_enc_query(self, enc_query):
        response = np.empty(self.num_rows, dtype=tuple)
        for i, db_row in enumerate(self.db):
            row_sum = (0, 0)
            for db_cell, query_col in zip(db_row, enc_query):
                row_sum = self.lwe.add(row_sum, self.lwe.multiply_scalar(db_cell, query_col))
            response[i] = row_sum
        return response
