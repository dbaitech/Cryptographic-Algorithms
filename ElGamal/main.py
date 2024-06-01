import random
import elgamal


def main():
    g = 7  # generator
    q = 2083  # prime
    elgamal_client = elgamal.ElGamal(g, q)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    # regular ElGamal
    message = 108
    y = random.randint(1, q)
    ciphertext = elgamal.encrypt(message, public_key, y)
    decrypted_message = elgamal_client.decrypt(ciphertext, private_key)

    print(f'Message: {message}, Encrypted Message: {ciphertext}, Decrypted Message: {decrypted_message}')
    assert message == decrypted_message

    # exponential ElGamal
    exp_message = g**285 % q
    exp_ciphertext = elgamal.encrypt(exp_message, public_key, y)
    exp_decrypted_message = elgamal_client.decrypt(exp_ciphertext, private_key)

    print(f'Message: {exp_message}, Encrypted Message: {exp_ciphertext}, Decrypted Message: {exp_decrypted_message}')
    assert exp_message == exp_decrypted_message

if __name__ == '__main__':
    main()
