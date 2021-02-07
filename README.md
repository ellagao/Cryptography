# Cryptography
In this repository, there are 4 projects:

1. Vigenere Encryption:
  This project can encrypt and decrypt txt files by Vigenere Encryption.
  It also solve this problem:
    Enter two short plaintexts of equal length and look for two secret keys.
    so that the ciphertext obtained by encrypting the first plaintext with the first secret key is the same as the ciphertext obtained by encrypting the second plaintext with the second secret key. 
    Output two secret keys and ciphertext. If such a secret key cannot be found, output "not found".
    (Plaintext length≥2*key length, the lengths of the keys can be different)
    
2. AES-128 Encryption:
  This project can encrypt and decrypt bmp files by Vigenere Encryption and AES-128 Encryption.
  More details:
    1. The key length of the Vigenere cipher is 4-32 bytes, and the operation is performed in bytes. (Mod 256)
    2. AES-128 Encryption uses ECB mode.
    3. High-level description of the Encryption algorithm
        KeyExpansion – round keys are derived from the cipher key using the AES key schedule. AES requires a separate 128-bit round key block for each round plus one more.
        Initial round key addition:
        AddRoundKey – each byte of the state is combined with a byte of the round key using bitwise xor.
        9, 11 or 13 rounds:
        SubBytes – a non-linear substitution step where each byte is replaced with another according to a lookup table.
        ShiftRows – a transposition step where the last three rows of the state are shifted cyclically a certain number of steps.
        MixColumns – a linear mixing operation which operates on the columns of the state, combining the four bytes in each column.
        AddRoundKey
        Final round (making 10, 12 or 14 rounds in total):
        SubBytes
        ShiftRows
        AddRoundKey
    4. Optimization of the cipher
        On systems with 32-bit or larger words, it is possible to speed up execution of this cipher by combining the SubBytes and ShiftRows steps with the MixColumns step by transforming them into a sequence of table lookups. 

3. Berlekamp–Massey(BM) algorithm:
  This project achieves the task of finding the shortest linear feedback shift register (LFSR) for a given binary output sequence. It also finds the minimal polynomial of a linearly recurrent sequence in an arbitrary field.
  
4. RC4 algorithm:
  This project can encrypt bitstreams by using RC4 algorithm.
