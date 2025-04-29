# Simulador de encriptación SUCI usando ECIES (criptografía de curva elíptica)
# Lado A: encripta un texto usando clave pública (simula el UE)
# Lado B: desencripta usando clave privada (simula el UDM)

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os, base64

# 1. Generamos la clave privada (lado B - UDM)
udm_private_key = ec.generate_private_key(ec.SECP256R1())
udm_public_key = udm_private_key.public_key()

# Serializar la clave pública para simular envío a lado A
public_bytes = udm_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# 2. Lado A - Simula el teléfono encriptando un mensaje con la clave pública del UDM
def encrypt_with_public_key(message: str, public_key_pem: bytes):
    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())

    # Generamos una clave efímera para ECIES
    ephemeral_key = ec.generate_private_key(ec.SECP256R1())
    shared_secret = ephemeral_key.exchange(ec.ECDH(), public_key)

    # Derivamos una clave AES del secreto compartido
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'suci encryption',
        backend=default_backend()
    ).derive(shared_secret)

    # Encriptamos usando AES-GCM
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

    return {
        'ephemeral_public_key': ephemeral_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ),
        'iv': base64.b64encode(iv).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'tag': base64.b64encode(encryptor.tag).decode()
    }

# 3. Lado B - Desencriptamos usando la clave privada del UDM
def decrypt_with_private_key(encrypted_data: dict, private_key):
    ephemeral_public_key = serialization.load_pem_public_key(
        encrypted_data['ephemeral_public_key'],
        backend=default_backend()
    )
    shared_secret = private_key.exchange(ec.ECDH(), ephemeral_public_key)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'suci encryption',
        backend=default_backend()
    ).derive(shared_secret)

    iv = base64.b64decode(encrypted_data['iv'])
    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    tag = base64.b64decode(encrypted_data['tag'])

    decryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

# Simulación:
texto = "IMSI123456789012345"
print("[LADO A] Texto original:", texto)

encrypted = encrypt_with_public_key(texto, public_bytes)
print("\n[LADO A] Texto encriptado:", encrypted['ciphertext'])

# Ahora lado B desencripta
resultado = decrypt_with_private_key(encrypted, udm_private_key)
print("\n[LADO B] Texto desencriptado:", resultado)
