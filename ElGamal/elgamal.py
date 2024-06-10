import random
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class ElGamal:
    def __init__(self, g, q, exponential=False):
        self.g = g  # generator
        self.q = q  # modulus
        self.exponential = exponential

    def generate_public_key(self, private_key):  # generator, order of cyclic group
        h = pow(self.g, private_key, self.q)
        return self.g, self.q, h

    def generate_private_key(self):
        return random.randint(0, self.q - 2)  # private key should be in the range [1, q-1]

    # message must be from 0 to q - 2
    def encrypt(self, message, public_key, y):
        g, q, h = public_key

        assert 1 <= y <= q - 1
        if message > q - 1:
            past_message = message
            message = message % (q - 1)  # ensure message is within the valid range of 0 to q - 2
            logging.info(f'Message was greater than range, taking message = {past_message} mod (q - 1) = {message}')
        shared_secret = pow(h, y, q)
        c1 = pow(g, y, q)
        print(f'c1 = pow({g}, {y}, {q}) = {c1}')
        if self.exponential:
            c2 = (pow(g, message, q) * shared_secret) % q
            print(f'c2 = pow({g}, {message}, {q}) * {shared_secret} % {q} = {c2}')
        else:
            c2 = (message * shared_secret) % q
        return c1, c2

    def decrypt(self, ciphertext, private_key):
        c1, c2 = ciphertext
        shared_secret = pow(c1, -1 * private_key, self.q) % self.q
        m_prime = (c2 * shared_secret) % self.q
        if self.exponential:
            for i in range(self.q - 1): # searching from 0 to q - 2
                if pow(self.g, i, self.q) == m_prime:
                    return i
            raise ValueError('Message too large to be represented in {0, ..., q-2}')
        return m_prime

    def add(self, ciphertext1, ciphertext2):
        if not self.exponential:
            raise ValueError('Only exponential ElGamal supports homomorphic addition.')
        c1, c2 = ciphertext1
        d1, d2 = ciphertext2
        return (c1 * d1) % self.q, (c2 * d2) % self.q

    def multiply_by_scalar(self, scalar, ciphertext):
        if not self.exponential:
            raise ValueError('Only exponential ElGamal supports multiplication with a scalar.')
        c1, c2 = ciphertext
        # scalar = scalar % (self.q - 1)  # scalar should be handled mod (q-1) for exponents
        return pow(c1, scalar, self.q), pow(c2, scalar, self.q)

    def multiply(self, ciphertext1, ciphertext2):
        if self.exponential:
            raise ValueError('Exponential ElGamal does not support homomorphic multiplication.')
        c1, c2 = ciphertext1
        d1, d2 = ciphertext2
        return (c1 * d1) % self.q, (c2 * d2) % self.q

# import random
#
#
# class ElGamal:
#     def __init__(self, g, q, exponential=False):
#         self.g = g  # generator
#         self.q = q  # modulus
#         self.exponential = exponential
#
#     def generate_public_key(self, private_key):  # generator, order of cyclic group
#         h = pow(self.g, private_key, self.q)
#         return self.g, self.q, h
#
#     def generate_private_key(self):
#         return random.randint(1, self.q)
#
#     def encrypt(self, message, public_key, y):
#         g, q, h = public_key
#
#         assert 1 <= y <= q - 1
#         # if message >= q - 1:
#         #     message = message % (q - 1)  # will eventually choose q such that b - sum(a_i, s_i)
#         message = message % q
#         shared_secret = pow(h, y, q)
#         c1 = pow(g, y, q)
#         if self.exponential:
#             c2 = (pow(g, message, q) * shared_secret) % q
#         else:
#             c2 = (message * shared_secret) % q
#         return c1, c2
#
#     def decrypt(self, ciphertext, private_key):
#         c1, c2 = ciphertext
#         m_prime = (c2 * pow(c1, -1 * private_key, self.q)) % self.q
#         if self.exponential:
#             for i in range(self.q):
#                 if pow(self.g, i, self.q) == m_prime:
#                     return i
#             raise ValueError('Message too large to be represented in {1, ..., q-1}')
#         return m_prime
#
#     def add(self, ciphertext1, ciphertext2):
#         if not self.exponential:
#             raise ValueError('Only exponential ElGamal supports homomorphic addition.')
#         c1, c2 = ciphertext1
#         d1, d2 = ciphertext2
#         return (c1 * d1) % self.q, (c2 * d2) % self.q
#
#     def multiply_by_scalar(self, scalar, ciphertext):
#         if not self.exponential:
#             raise ValueError('Only exponential ElGamal supports multiplication with a scalar.')
#         c1, c2 = ciphertext
#         scalar = scalar % self.q
#         return pow(c1, scalar, self.q), pow(c2, scalar, self.q)
#
#     def multiply(self, ciphertext1, ciphertext2):
#         if self.exponential:
#             raise ValueError('Exponential ElGamal does not support homomorphic multiplication.')
#         c1, c2 = ciphertext1
#         d1, d2 = ciphertext2
#         return (c1 * d1) % self.q, (c2 * d2) % self.q
