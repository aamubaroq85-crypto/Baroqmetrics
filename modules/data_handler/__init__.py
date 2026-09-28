"""
Modul Pengolahan & Sanitasi Data Pertambangan — Zuhri Formalism
Bertanggung jawab untuk mem-parsing, memvalidasi struktur, dan mensanitasi 
data masukan (CSV/DataFrame) sebelum diproses oleh engine utama.
"""

import pandas as pd
import io
from core.validator import MiningDataValidator, SecureDataManager

class MiningDataHandler:
    @staticmethod
    def parse_and_sanitize_csv(uploaded_file) -> pd.DataFrame:
        """
        Membaca file CSV masukan, memvalidasi kolom wajib, dan membersihkan data 
        dari karakter ilegal untuk mencegah injeksi atau kesalahan runtime.
        """
        if uploaded_file is None:
            raise ValueError("Berkas data masukan tidak boleh kosong.")

        try:
            # Membaca file menggunakan pandas dengan penanganan error I/O
            if isinstance(uploaded_file, bytes):
                df = pd.read_csv(io.BytesIO(uploaded_file))
            else:
                df = pd.read_csv(uploaded_file)
        except Exception as e:
            raise RuntimeError(f"Gagal membaca format file CSV: {str(e)}")

        # Validasi kolom wajib untuk data geofisika/pertambangan
        required_columns = ["block_id", "volume", "bulk_density", "dilution_factor"]
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"Kolom wajib '{col}' tidak ditemukan dalam struktur data masukan.")

        # Sanitasi baris data string dan validasi rentang numerik
        sanitized_rows = []
        for index, row in df.iterrows():
            try:
                # Sanitasi string pada ID Blok
                clean_block_id = MiningDataValidator.sanitize_input(str(row["block_id"]))
                
                # Validasi ketat parameter numerik
                clean_volume = MiningDataValidator.validate_numeric_parameter(
                    f"Volume (Baris {index})", row["volume"], 0.0, 1e9
                )
                clean_density = MiningDataValidator.validate_numeric_parameter(
                    f"Bulk Density (Baris {index})", row["bulk_density"], 0.1, 20.0
                )
                clean_dilution = MiningDataValidator.validate_numeric_parameter(
                    f"Dilution Factor (Baris {index})", row["dilution_factor"], 0.0, 1.0
                )

                sanitized_rows.append({
                    "block_id": clean_block_id,
                    "volume": clean_volume,
                    "bulk_density": clean_density,
                    "dilution_factor": clean_dilution
                })
            except Exception as row_error:
                raise ValueError(f"Kesalahan validasi pada baris ke-{index}: {str(row_error)}")

        # Mengembalikan DataFrame yang telah bersih dan tervalidasi deterministik
        return pd.DataFrame(sanitized_rows)

    @staticmethod
    def export_encrypted_secure_log(data_dict: dict, file_path: str) -> bool:
        """
        Mengenkripsi kamus data log operasional dan menyimpannya secara lokal
        sesuai protokol keamanan SECURITY.md.
        """
        try:
            manager = SecureDataManager()
            raw_string = str(data_dict)
            encrypted_bytes = manager.encrypt_data(raw_string)
            
            with open(file_path, "wb") as f:
                f.write(encrypted_bytes)
            return True
        except Exception as e:
            raise RuntimeError(f"Gagal menyimpan log terenkripsi secara lokal: {str(e)}")
