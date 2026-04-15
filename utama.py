# ============================================================
# APLIKASI CITRA - UTAMA
# Program interaktif untuk perbaikan kualitas citra digital
# ============================================================
# Author : Deny Fajar Nugraha
# Institusi: Universitas Tidar - Teknik Elektro
# ============================================================

import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

# Import komponen UI (dari folder bahan)
from bahan.judul import render_judul
from bahan.penutup import render_penutup
from bahan.samping import render_samping

# Import fungsi pengolahan citra (dari folder pengolahan_citra)
from pengolahan_citra.penajaman import terapkan_penajaman
from pengolahan_citra.reduksi_derau import terapkan_median_filter
from pengolahan_citra.clahe import terapkan_clahe

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="APLIKASI CITRA - Untidar",
    page_icon="🖼️",
    layout="wide"
)

# ============================================================
# FUNGSI UTILITAS (Histogram, Statistik, Unduh)
# ============================================================
def hitung_varians(citra_abu):
    return np.var(citra_abu)

def plot_histogram(citra, judul="Histogram"):
    if len(citra.shape) == 3:
        abu = cv2.cvtColor(citra, cv2.COLOR_BGR2GRAY)
    else:
        abu = citra
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(abu.ravel(), bins=256, range=[0, 256], color='#0d6efd', alpha=0.7)
    ax.set_xlim([0, 256])
    ax.set_xlabel('Nilai Intensitas Piksel')
    ax.set_ylabel('Frekuensi')
    ax.set_title(judul)
    return fig

def dapatkan_tautan_unduh(citra, nama_file="citra_hasil.png"):
    citra_rgb = cv2.cvtColor(citra, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(citra_rgb)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    byte_img = buf.getvalue()
    return byte_img

# ============================================================
# RENDER UI
# ============================================================
render_judul()
file_unggah, mode, ukuran_kernel, batas_klip, ukuran_tile = render_samping()

# ============================================================
# AREA UTAMA
# ============================================================
if file_unggah is not None:
    byte_file = np.asarray(bytearray(file_unggah.read()), dtype=np.uint8)
    citra_asli = cv2.imdecode(byte_file, cv2.IMREAD_COLOR)

    st.subheader("📷 Citra Asli")
    kol1, kol2 = st.columns(2)
    with kol1:
        st.image(cv2.cvtColor(citra_asli, cv2.COLOR_BGR2RGB),
                 caption="Citra Asli", use_container_width=True)
    with kol2:
        fig_asli = plot_histogram(citra_asli, "Histogram Citra Asli")
        st.pyplot(fig_asli)

    abu_asli = cv2.cvtColor(citra_asli, cv2.COLOR_BGR2GRAY)
    var_asli = hitung_varians(abu_asli)
    min_asli, max_asli = np.min(abu_asli), np.max(abu_asli)
    st.info(f"**Statistik Citra Asli:** Varians = {var_asli:.2f} | Rentang Intensitas = [{min_asli}, {max_asli}]")

    st.markdown("---")

    if st.button("🚀 Proses Citra", type="primary"):
        with st.spinner("Sedang memproses citra..."):
            if mode == "🔪 Penajaman (Sharpening)":
                citra_hasil = terapkan_penajaman(citra_asli)
                nama_mode = "Penajaman (Laplacian Kernel)"
            elif mode == "🧹 Reduksi Derau (Median Filter)":
                citra_hasil = terapkan_median_filter(citra_asli, ukuran_kernel)
                nama_mode = f"Median Filter ({ukuran_kernel}x{ukuran_kernel})"
            else:  # CLAHE
                citra_hasil = terapkan_clahe(citra_asli, batas_klip, ukuran_tile)
                nama_mode = f"CLAHE (klip={batas_klip}, tile={ukuran_tile})"

            abu_hasil = cv2.cvtColor(citra_hasil, cv2.COLOR_BGR2GRAY)
            var_hasil = hitung_varians(abu_hasil)
            min_hasil, max_hasil = np.min(abu_hasil), np.max(abu_hasil)

            st.subheader(f"✨ Citra Hasil ({nama_mode})")
            kol1, kol2 = st.columns(2)
            with kol1:
                st.image(cv2.cvtColor(citra_hasil, cv2.COLOR_BGR2RGB),
                         caption=f"Hasil: {nama_mode}", use_container_width=True)
            with kol2:
                fig_hasil = plot_histogram(citra_hasil, f"Histogram Hasil ({nama_mode})")
                st.pyplot(fig_hasil)

            st.success(f"""
            **Perbandingan Statistik:**
            - Varians Asli: {var_asli:.2f} → Varians Hasil: {var_hasil:.2f} (Δ = {var_hasil - var_asli:.2f})
            - Rentang Asli: [{min_asli}, {max_asli}] → Rentang Hasil: [{min_hasil}, {max_hasil}]
            """)

            data_unduh = dapatkan_tautan_unduh(citra_hasil, f"hasil_{nama_mode}.png")
            st.download_button(
                label="💾 Unduh Citra Hasil",
                data=data_unduh,
                file_name=f"hasil_{nama_mode}.png",
                mime="image/png"
            )
else:
    st.info("👈 Silakan unggah citra terlebih dahulu melalui sidebar di sebelah kiri.")
    st.markdown("### 🧪 Contoh Mode yang Tersedia:")
    kol1, kol2, kol3 = st.columns(3)
    with kol1:
        st.markdown("#### 🔪 Penajaman")
        st.markdown("Memperjelas tepi objek pada citra buram menggunakan kernel Laplacian.")
    with kol2:
        st.markdown("#### 🧹 Reduksi Derau")
        st.markdown("Membersihkan derau gangguan pada citra dengan Median Filter.")
    with kol3:
        st.markdown("#### 🌈 CLAHE")
        st.markdown("Meningkatkan kontras lokal secara adaptif tanpa berlebihan atau meningkatkan derau")

render_penutup()