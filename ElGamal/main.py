import random
from elgamal import ElGamal


def main():
    g = 7  # generator
    q = 2083  # prime
    elgamal = ElGamal(g, q)
    private_key = elgamal.generate_private_key()
    public_key = elgamal.generate_public_key(private_key)
    h = public_key[2]

    message = 97
    y = random.randint(1, q)
    ciphertext = elgamal.encrypt(97, public_key, y)
    decrypted_message = elgamal.decrypt(ciphertext, private_key)

    print(f'Message: {message}, Encrypted Message: {ciphertext}, Decrypted Message: {decrypted_message}')
    assert message == decrypted_message


if __name__ == '__main__':
    main()
