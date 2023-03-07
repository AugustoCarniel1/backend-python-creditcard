import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def encrypt_credit_card_number(key, number):

    cc_number_bytes = number.encode('UTF-8')

    encrypted = key.encrypt(
        cc_number_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(encrypted).decode('UTF-8')


def decrypt_credit_card_number(key, encrypted):

    encrypted_number_bytes = base64.b64decode(encrypted.encode('UTF-8'))

    decrypted = key.decrypt(
        encrypted_number_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted.decode('UTF-8')
