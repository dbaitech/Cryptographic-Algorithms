This repository contains the files to implement Private Information Retrieval using the **Secret-key Regev encryption** and **Kushilevitz and Ostrovsky method** described in the paper *Replication is not needed: single database, computationally-private information retrieval* (https://dl.acm.org/doi/10.5555/795663.796363)

# Structure
## client.py
Contains the client functionalities to generate an encrypted query and decrypt the server's response. 
1. A secret key is generated using the Secret-key Regev encryption scheme
2. An encrypted query is then generated based on the secret key and the given row and column to be queried from the database (assumes a 2D database of size $\sqrt n$ x $\sqrt n$).
   - The client first generates a vector $v$ of size $\sqrt n$ where each element corresponds to a column in the database.
   - $v$ is filled with zeros except at the index corresponding column being queried which contains a 1.
   - $v$ is then encrypted according to the Secret-key Regev encryption scheme in lwe.py
4. The server's response of $\sqrt n$ values (1 per row) is then filtered to get the value of the desired row which contains the true value of the column in the database.

## server.py
Coming Soon

## lwe.py
Coming Soon
