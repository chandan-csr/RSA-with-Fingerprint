#RSA algorithm
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

def generate_keypair(prime_before, prime_after):
    n = prime_before * prime_after
    phi = (prime_before-1) * (prime_after-1)

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return ''.join([chr(c + 65) for c in cipher])

def decrypt(pk, ciphertext):
    key, n = pk
    cipher = [ord(char) - 65 for char in ciphertext]
    plain = [chr(pow(char, key, n)) for char in cipher]
    return ''.join(plain)


#p = int(prime_before)
#q = int(prime_after)

#print("Public Key: ", public)
#print("Private Key: ", private)

#message = input("Enter a message to encrypt with RSA: ")
def ed(public_key,private_key,plaintext):
    ciphertext = encrypt(public_key, plaintext)
    #print("Encrypted Message: ", ''.join(map(str, encrypted_message)))

    decryptedtext = decrypt(private_key, ciphertext)
    
    return ciphertext, decryptedtext
    #print("Decrypted Message: ", decrypted_message)