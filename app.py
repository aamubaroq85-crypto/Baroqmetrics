"""
Antarmuka Utama Streamlit — Baroqmetrics Geophysics & Mining Engine
Dibangun berdasarkan standar desain minimalis fungsional (DESIGN.md).
"""
import streamlit as st
import os
from dotenv import load_dotenv
from core.formalism_engine import MiningFormalismEngine
from core.validator import MiningDataValidator, SecureDataManager

# Memuat variabel lingkungan aman
load_dotenv()

# Konfigurasi Halaman
st.set_page_config(
    page_title="Baroqmetrics Mining Engine | Zuhri Formalism",
    page_icon="⛏️",
    layout="wide"
)

# Styling kustom sesuai skema warna DESIGN.md (Slate Dark & Sky Blue)
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    h1, h2, h3 { color: #0F172A; font-family: 'Inter', sans-serif; }
    .stButton>button {
        background-color: #0284C7;
        color: white;
        border-radius: 0.375rem;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #0369A1;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("⛏️ Baroqmetrics Geophysics & Mining Engine")
    st.markdown("### *Professional Calculation & Data Sanitization Suite (Zuhri Formalism)*")
    st.write("Sistem pemrosesan data pertambangan berstandar deterministik, aman, dan terenkripsi.")

    # Sidebar Navigasi / Kontrol
    st.sidebar.header("🎛️ Panel Kontrol & Konfigurasi")
    module_choice = st.sidebar.selectbox(
        "Pilih Modul Fungsional",
        ["Estimasi Cadangan Bijih (Ore Reserve)", "Sanitasi & Enkripsi Data Lokal"]
    )

    if module_choice == "Estimasi Cadangan Bijih (Ore Reserve)":
        st.subheader("📊 Modul Kalkulasi Cadangan Bijih")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            volume_input = st.number_input("Volume Blok (m³)", min_value=0.0, value=10000.0, step=100.0)
        with col2:
            density_input = st.number_input("Bulk Density (t/m³)", min_value=0.1, value=2.7, step=0.1)
        with col3:
            dilution_input = st.number_input("Dilution Factor (rasio)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)

        if st.button("Jalankan Kalkulasi Deterministik"):
            try:
                # Eksekusi melalui Engine Formalisme dengan validasi ketat
                result = MiningFormalismEngine.calculate_ore_reserve(
                    volume=volume_input,
                    bulk_density=density_input,
                    dilution_factor=dilution_input
                )
                
                st.success("Kalkulasi berhasil dieksekusi tanpa pelanggaran batas logika.")
                st.metric("Estimasi Tonnage In-Situ", f"{result['in_situ_tonnage_tonnes']:,} Tonnes")
                st.metric("Total Cadangan Terkoreksi (Adjusted)", f"{result['adjusted_reserve_tonnes']:,} Tonnes")
                
            except Exception as e:
                st.error(f"Gagal mengeksekusi kalkulasi sistem: {str(e)}")

    elif module_choice == "Sanitasi & Enkripsi Data Lokal":
        st.subheader("🔒 Keamanan & Enkripsi Data Sensitif (SECURITY.md)")
        
        raw_text = st.text_area("Masukkan Catatan / Parameter Log Tambang Mentah:")
        
        if st.button("Enkripsi Data Aman"):
            if raw_text:
                try:
                    manager = SecureDataManager()
                    encrypted = manager.encrypt_data(raw_text)
                    st.success("Data berhasil dienkripsi menggunakan standar keamanan tinggi.")
                    st.code(encrypted)
                except Exception as e:
                    st.error(f"Error Enkripsi: {str(e)}")
            else:
                st.warning("Harap masukkan teks terlebih dahulu.")

if __name__ == "__main__":
    main()
