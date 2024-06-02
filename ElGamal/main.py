import random
from elgamal import ElGamal


def main():
    g = 7  # generator
    q = 2083  # prime
    elgamal_client = ElGamal(g, q)
    private_key = elgamal_client.generate_private_key()
    public_key = elgamal_client.generate_public_key(private_key)

    # regular ElGamal
    message = 108
    y = random.randint(1, q)
    ciphertext = ElGamal.encrypt(message, public_key, y)
    decrypted_message = elgamal_client.decrypt(ciphertext, private_key)

    print(f'Message: {message}, Encrypted Message: {ciphertext}, Decrypted Message: {decrypted_message}')
    assert message == decrypted_message

    # exponential ElGamal
    m_1 = 285
    m_2 = 215
    m_sum = m_1 + m_2
    exp_m_sum = g**m_sum % q

    exp_message_1 = g**285 % q
    exp_message_2 = g**215 % q

    # exp_ciphertext_1 = ElGamal.encrypt(exp_message_1, public_key, y)
    # exp_ciphertext_2 = ElGamal.encrypt(exp_message_2, public_key, y)

    exp_ciphertext_1 = ElGamal.encrypt(m_1, public_key, y, exponential=True)
    exp_ciphertext_2 = ElGamal.encrypt(m_2, public_key, y, exponential=True)

    added_ciphertexts = ElGamal.add(q, exp_ciphertext_1, exp_ciphertext_2)
    decrypt_added_ciphertexts = elgamal_client.decrypt(added_ciphertexts, private_key, exponential=True)

    print(f'Message 1: {exp_message_1}, Message 2: {exp_message_2}, '
          f'Encrypted Message 1: {exp_ciphertext_1}, Encrypted Message 2: {exp_ciphertext_2}, '
          f'Added encrypted Messages: {added_ciphertexts}, '
          f'Decrypted Added Messages: {decrypt_added_ciphertexts}')
    assert decrypt_added_ciphertexts == exp_m_sum


    # exp_decrypted_message_1 = elgamal_client.decrypt(exp_ciphertext_1, private_key)
    # exp_decrypted_message_2 = elgamal_client.decrypt(exp_ciphertext_2, private_key)
    #
    # print(f'Message: {exp_message}, Encrypted Message: {exp_ciphertext}, Decrypted Message: {exp_decrypted_message}')
    # assert exp_message == exp_decrypted_message

if __name__ == '__main__':
    main()
