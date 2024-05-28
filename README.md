This repository contains the files to implement Private Information Retrieval using the **Secret-key Regev encryption (LWE)** and **Kushilevitz and Ostrovsky method** described in the paper *Replication is not needed: single database, computationally-private information retrieval* (https://dl.acm.org/doi/10.5555/795663.796363)

# Structure
## client.py
Contains the client functionalities to generate an encrypted query and decrypt the server's response. 
1. A secret key is generated using the Secret-key Regev encryption scheme
2. An encrypted query is then generated based on the secret key and the desired row and column to be queried from the database (assumes a 2D database of size $\sqrt n$ x $\sqrt n$).
   - The client first generates a vector $v$ of size $\sqrt n$ where each element corresponds to a column in the database.
   - $v$ is filled with zeros except at the index corresponding column being queried which contains a 1: $(0, \ldots, 1,\ldots, 0)$
   - $v$ is then encrypted according to the Secret-key Regev encryption scheme in lwe.py: $(0, \ldots, 1,\ldots, 0) \rightarrow \Big ((a_1, c_1), \ldots, (a_i, c_i),\ldots, (a_{\sqrt{n}}, c_{\sqrt{n}}) \Big )$
4. The server responds with $\sqrt n$ values (1 per row). Because the client knows what row it wants to query, it selects the value of the desired row which contains the encrypted value of the column in the database.
6. The client then decrypts this value to get the true value situated at the desired row and column.

## server.py
Contains the server's functionalities to receive and process the client's encrypted query. It uses homomorphic addition and multiplication to get the inner product of the client's encrypted query vector with each row of the database i.e. it computes the following for each row:
$$(f_i, g_i) = \sum_{i=1}^{\sqrt{n}} b_i \cdot (a_i, c_i)$$ where $b_i$ is the value of the cell at the current row and column $i$ in the database. The server returns $\sqrt n$ values corresponding to each row:
$$\Big ((f_1, g_1), \ldots, (f_{\sqrt{n}}, g_{\sqrt{n}}) \Big)$$

## lwe.py
Abstracts the encryption and decryption methods used by the client as well as the homomorphic addition and multiplication methods used by the server. (Reference: *One Server for the Price of Two:
Simple and Fast Single-Server Private Information Retrieval*, https://eprint.iacr.org/2022/949.pdf)
### enryption
As described in the **Secret-key Regev encryption** scheme, a secret key $s$ is generated as a vector $\in \mathbb{Z}^n_q$ where each component is chosen randomly from the uniform distribution. $s$ is then used to encrypt the plaintext $m \in \mathbb{Z}_p$ as follows:
$$encrypt(m, s) = (a, a^Ts + e + \lfloor\frac{q}{p}\rfloor \cdot m) = (a, c)$$ where $a$ is a randomly chosen vector $\in \mathbb{Z}^n_q$, $e$ is a small number chosen from $\chi$ (a Normal distribution with special constraints), $p$ is the plaintext modulus, $q$ is the ciphertext modulus and $n$ is the dimension of the secret key.

The client then uses this encrypt function to generate its encrypted query which will have the structure $\Big ((a_1, c_1), \ldots, (a_d, c_d) \Big)$ where $d$ is the number of columns in the database ($\sqrt n$).

### decryption
Given $(a, c)$ as the ciphertext, the decryption to get the plaintext $m$ is quite simple: $c - a^Ts \mod q$ which is rounded to the nearest multiple of $\lfloor\frac{q}{p}\rfloor$. So, it is essentially: $$m = round(\frac{c - a^Ts \mod q}{\lfloor\frac{q}{p}\rfloor})$$

The client receives the server's response as the modified ciphertexts after homomorphic operations have been performed: $((f_1, g_1), \ldots, (f_d, g_d))$. The client then selects the value corresponding to the row it wanted to query: $(f_i, g_i)$ and uses the decrypt function to get back the plaintext value.
