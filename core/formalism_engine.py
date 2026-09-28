"""
Modul Kalkulasi Inti Pertambangan — Zuhri Formalism
Menjalankan algoritma perhitungan teknis secara deterministik dan terukur.
"""
from core.validator import MiningDataValidator

class MiningFormalismEngine:
    @staticmethod
    def calculate_ore_reserve(volume: float, bulk_density: float, dilution_factor: float) -> dict:
        """
        Menghitung estimasi cadangan bijih (Ore Reserve) berdasarkan parameter formal.
        """
        # Validasi ketat parameter masukan
        v = MiningDataValidator.validate_numeric_parameter("Volume", volume, 0.0, 1e9)
        bd = MiningDataValidator.validate_numeric_parameter("Bulk Density", bulk_density, 0.1, 20.0)
        df = MiningDataValidator.validate_numeric_parameter("Dilution Factor", dilution_factor, 0.0, 1.0)

        # Kalkulasi deterministik
        in_situ_tonnage = v * bd
        adjusted_tonnage = in_situ_tonnage * (1.0 + df)

        return {
            "in_situ_tonnage_tonnes": round(in_situ_tonnage, 2),
            "adjusted_reserve_tonnes": round(adjusted_tonnage, 2),
            "status": "VALID_DETERMINISTIC_EXECUTION"
        }
