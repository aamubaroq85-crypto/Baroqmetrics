"""
Modul Validasi & Sanitasi Data — Zuhri Formalism
Bertanggung jawab untuk mencegah input ilegal dan mengamankan data lokal.
"""
import os
import re
from cryptography.fernet import Fernet

class MiningDataValidator:
    @staticmethod
    def sanitize_input(value: str) -> str:
        """Membersihkan input teks dari karakter berbahaya untuk mencegah injeksi."""
        if not isinstance(value, str):
            raise TypeError("Parameter input wajib berupa string.")
        # Hanya izinkan karakter alfanumerik, titik, spasi, minus, dan underscore
        sanitized = re.sub(r'[^a-zA-Z0-9.\s\-_]', '', value)
        return sanitized.strip()

    @staticmethod
    def validate_numeric_parameter(param_name: str, value: float, min_val: float, max_val: float) -> float:
        """Memastikan parameter numerik pertambangan berada dalam rentang valid yang deterministik."""
        try:
            val = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Parameter '{param_name}' harus bernilai numerik yang valid.")
        
        if not (min_val <= val <= max_val):
            raise ValueError(f"Parameter '{param_name}' ({val}) diluar batas aman ({min_val} - {max_val}).")
        return val

class SecureDataManager:
    def __init__(self, key: str = None):
        """Inisialisasi enkripsi tingkat lanjut menggunakan Fernet."""
        self.key = key or os.getenv("ENCRYPTION_KEY")
        if not self.key:
            # Fallback otomatis untuk pengembangan jika key belum ada di env (di-generate aman)
            self.key = Fernet.generate_key()
        elif isinstance(self.key, str):
            self.key = self.key.encode()
        self.cipher = Fernet(self.key)

    def encrypt_data(self, raw_data: str) -> bytes:
        """Mengenkripsi data sensitif pertambangan sebelum disimpan secara lokal."""
        try:
            return self.cipher.encrypt(raw_data.encode('utf-8'))
        except Exception as e:
            raise RuntimeError(f"Gagal melakukan enkripsi data: {str(e)}")

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Mendekripsi data lokal yang tersimpan secara aman."""
        try:
            return self.cipher.decrypt(encrypted_data).decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"Gagal melakukan dekripsi data: {str(e)}")
