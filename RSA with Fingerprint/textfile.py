import random
import os
import docx

global prime_before, prime_after
static_folder = "static"

#----------------------------------------------------------------------------------------------#


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def generate_keypair1(prime_before, prime_after):
    n = prime_before * prime_after
    phi = (prime_before-1) * (prime_after-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = modinv(e, phi)
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

def encryptfile(file_path, prime_before, prime_after):
    # generate keypair
    public, private = generate_keypair1(prime_before, prime_after)

    # read input message from file
    with open(file_path, 'r', encoding='utf-8') as f:
        message = f.read().strip()

    # get input file name and extension
    input_file_name, input_file_ext = os.path.splitext(file_path)

    # check file extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.doc' or ext == '.docx':
        # read input message from doc or docx file
        doc = docx.Document(file_path)
        message = '\n'.join([para.text for para in doc.paragraphs])
    elif ext == '.txt':
        # read input message from txt file
        with open(file_path, 'r', encoding='utf-8') as f:
            message = f.read().strip()
    else:
        raise ValueError('Invalid file extension')

    # encrypt message
    encrypted_msg = encrypt(public, message)

    # write encrypted message to file
    encrypted_file_path = os.path.join(static_folder, 'encrypted' + input_file_ext)
    with open(encrypted_file_path, 'w', encoding='utf-8') as f:
        f.write(' '.join(map(str, encrypted_msg)))

    # decrypt message
    decrypted_msg = decrypt(private, encrypted_msg)

    # write decrypted message to file
    decrypted_file_path = os.path.join(static_folder, 'decrypted' + input_file_ext)
    with open(decrypted_file_path, 'w', encoding='utf-8') as f:
        f.write(decrypted_msg)

    # save input file to static folder
    input_file_name = os.path.basename(file_path)
    static_input_file_path = os.path.join(static_folder, input_file_name)
    os.rename(file_path, static_input_file_path)

