This repository contains the files to implement Private Information Retrieval using the **Secret-key Regev encryption (LWE)** and **Kushilevitz and Ostrovsky method** described in the paper *Replication is not needed: single database, computationally-private information retrieval* (https://dl.acm.org/doi/10.5555/795663.796363)

# Structure
## client.py
Contains the client functionalities to generate an encrypted query and decrypt the server's response. 
1. A secret key is generated using the Secret-key Regev encryption scheme
2. An encrypted query is then generated based on the secret key and the desired row and column to be queried from the database (assumes a 2D database of size $\sqrt n$ x $\sqrt n$).
   - The client first generates a vector $v$ of size $\sqrt n$ where each element corresponds to a column in the database.
   - $v$ is filled with zeros except at the index corresponding column being queried which contains a 1.
   - $v$ is then encrypted according to the Secret-key Regev encryption scheme in lwe.py
4. The server's response of $\sqrt n$ values (1 per row) is then filtered to get the value of the desired row which contains the encrypted value of the column in the database.
5. The user then decrypts this value to get the true value situated at the desired row and column.

## server.py
Contains the server's functionalities to receive and process the client's encrypted query. It Uses homomorphic addition and multiplication to get the inner product of the client's encrypted query vector with each row of the database. The server returns $\sqrt n$ values corresponding to each row.

## lwe.py
Abstracts the encryption and decryption methods used by the client as well as the homomorphic addition and multiplication methods used by the server. (Reference: *One Server for the Price of Two:
Simple and Fast Single-Server Private Information Retrieval*, https://eprint.iacr.org/2022/949.pdf)
### enryption
As described in the **Secret-key Regev encryption** scheme, a secret key $s$ is generated as a vector $\in \mathbb{Z}^n_q$ where each component is chosen randomly from the uniform distribution. $s$ is then used to encrypt the plaintext $m \in \mathbb{Z}_p$ as follows:
$$encrypt(m, s) = (a, a^Ts + e + \lfloor\frac{q}{p}\rfloor \cdot m) = (a, c)$$ where $a$ is a randomly chosen vector $\in \mathbb{Z}^n_q$, $e$ is a small number chosen from $\chi$ (a Normal distribution with special constraints), $p$ is the plaintext modulus, $q$ is the ciphertext modulus and $n$ is the dimension of the secret key.
