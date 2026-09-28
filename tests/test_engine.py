"""
Modul Pengujian Unit Otomatis (Automated Unit Testing) — Zuhri Formalism
Memastikan seluruh komponen validasi, engine kalkulasi, dan modul logika 
berjalan secara deterministik tanpa celah kesalahan.
"""

import unittest
from core.validator import MiningDataValidator
from core.formalism_engine import MiningFormalismEngine
from modules.logic_processor import MiningLogicProcessor

class TestZuhriFormalismEngine(unittest.TestCase):
    
    def test_validator_numeric(self):
        """Uji coba validasi rentang angka yang valid dan invalid."""
        valid_val = MiningDataValidator.validate_numeric_parameter("Test Param", 5.0, 0.0, 10.0)
        self.assertEqual(valid_val, 5.0)
        
        # Memastikan error dilempar jika di luar batas aman
        with self.assertRaises(ValueError):
            MiningDataValidator.validate_numeric_parameter("Test Param", 15.0, 0.0, 10.0)

    def test_ore_reserve_calculation(self):
        """Uji coba perhitungan cadangan bijih (Ore Reserve)."""
        res = MiningFormalismEngine.calculate_ore_reserve(
            volume=1000.0, 
            bulk_density=2.5, 
            dilution_factor=0.1
        )
        self.assertEqual(res["in_situ_tonnage_tonnes"], 2500.0)
        self.assertEqual(res["adjusted_reserve_tonnes"], 2750.0)

    def test_logic_processor(self):
        """Uji coba kalkulasi siklus produksi alat berat."""
        res = MiningLogicProcessor.calculate_production_cycle(
            payload_capacity=50.0, 
            cycle_time_minutes=15.0, 
            efficiency_factor=0.8
        )
        self.assertEqual(res["cycles_per_hour"], 4.0)
        self.assertEqual(res["hourly_production_tonnes"], 160.0)

if __name__ == "__main__":
    unittest.main()
