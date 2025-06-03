import os
import json
import base64
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Configure logging
logging.basicConfig(
    filename="nudamu_memory.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class MemoriaSagrada:
    """
    Secure encrypted memory storage using AES-GCM.
    Stores interactions securely and allows retrieval.
    """
    def __init__(self, clave):
        # Permite clave como str o bytes
        if isinstance(clave, str):
            clave = clave.encode()
        if clave is None or len(clave) not in [16, 24, 32]:
            raise ValueError("❌ Invalid/Missing NUDAMU_CRYPTO_KEY (needs 16/24/32 bytes)")
        self.clave = clave
        self.storage_file = "secure_memoria.json"

    def cifrar(self, mensaje: str) -> str:
        """Encrypts a message using AES-GCM."""
        iv = os.urandom(12)  # Secure random nonce (IV)
        cipher = Cipher(algorithms.AES(self.clave), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(mensaje.encode()) + encryptor.finalize()
        encrypted_data = {
            "iv": base64.b64encode(iv).decode(),
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "tag": base64.b64encode(encryptor.tag).decode()
        }

        return json.dumps(encrypted_data)

    def descifrar(self, encrypted_json: str) -> str:
        """Decrypts an AES-GCM encrypted message."""
        try:
            data = json.loads(encrypted_json)
            iv = base64.b64decode(data["iv"])
            ciphertext = base64.b64decode(data["ciphertext"])
            tag = base64.b64decode(data["tag"])

            cipher = Cipher(algorithms.AES(self.clave), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()

            return (decryptor.update(ciphertext) + decryptor.finalize()).decode()
        except Exception as e:
            logging.error(f"⚠️ Decryption failed: {e}")
            return "❌ Decryption error!"

    def guardar(self, usuario_id: str, mensaje: str, etiqueta: str):
        """Encrypts and stores user interaction securely."""
        encrypted_message = self.cifrar(mensaje)
        memoria_entry = {
            "usuario_id": usuario_id,
            "etiqueta": etiqueta,
            "mensaje_cifrado": encrypted_message
        }

        # Save to file
        self._guardar_json(memoria_entry)

        logging.info(f"✅ Interaction stored securely for user {usuario_id}.")

    def recuperar(self, usuario_id: str) -> list:
        """Retrieves all stored interactions for a specific user."""
        memoria_data = self._cargar_json()
        usuario_memoria = [entry for entry in memoria_data if entry["usuario_id"] == usuario_id]

        return [
            {"etiqueta": entry["etiqueta"], "mensaje": self.descifrar(entry["mensaje_cifrado"])}
            for entry in usuario_memoria
        ]

    def listar_recuerdos(self, usuario_id: str) -> list:
        """Alias para recuperar, para compatibilidad con otras interfaces."""
        return self.recuperar(usuario_id)

    def _guardar_json(self, memoria_entry):
        """
        Saves encrypted memory data to a JSON file securely.
        Ensures stored interactions remain encrypted and accessible.
        """
        memoria_data = self._cargar_json()
        memoria_data.append(memoria_entry)

        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(memoria_data, f, ensure_ascii=False, indent=4)

    def _cargar_json(self) -> list:
        """Loads stored encrypted memory data from JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

