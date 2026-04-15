import streamlit as st

def render_samping():
    """
    Menampilkan sidebar: unggah citra, pilih mode, pengaturan lanjutan.
    Mengembalikan tuple (file_unggah, mode, ukuran_kernel, batas_klip, ukuran_tile)
    """
    st.sidebar.header("📤 Unggah Citra")
    file_unggah = st.sidebar.file_uploader(
        "Pilih file citra (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Pilih Mode Perbaikan")
    mode = st.sidebar.radio(
        "Mode:",
        ["🔪 Penajaman (Sharpening)",
         "🧹 Reduksi Derau (Median Filter)",
         "🌈 Peningkatan Kontras (CLAHE)"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("🔧 Pengaturan Lanjutan")
    
    # Parameter untuk Median Filter
    if mode == "🧹 Reduksi Derau (Median Filter)":
        ukuran_kernel = st.sidebar.slider("Ukuran Kernel", min_value=3, max_value=11, step=2, value=5)
    else:
        ukuran_kernel = 5
    
    # Parameter untuk CLAHE
    if mode == "🌈 Peningkatan Kontras (CLAHE)":
        batas_klip = st.sidebar.slider("Batas Klip (Clip Limit)", min_value=1.0, max_value=5.0, step=0.5, value=2.0)
        ukuran_tile = st.sidebar.selectbox("Ukuran Tile Grid", options=[4, 8, 16], index=1)
    else:
        batas_klip = 2.0
        ukuran_tile = 8
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 📘 Tentang Mode
    - **Penajaman**: Memperjelas tepi objek.
    - **Reduksi Derau**: Membersihkan noise citra.
    - **CLAHE**: Kontras adaptif lokal.
    """)
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Deny Fajar Nugraha - 2026**")
    
    return file_unggah, mode, ukuran_kernel, batas_klip, ukuran_tile