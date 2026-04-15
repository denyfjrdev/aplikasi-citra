import streamlit as st
import os

def render_judul():
    """
    Menampilkan bagian judul (header) aplikasi.
    """
    kol1, kol2 = st.columns([1, 8])
    
    with kol1:
        logo_path = "logo_untidar.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)
        else:
            st.markdown("🖼️")
    
    with kol2:
        st.markdown('<p class="judul-aplikasi">Aplikasi Citra</p>', unsafe_allow_html=True)
        st.markdown("**Universitas Tidar - Teknik Elektro**")
        st.markdown("Pengolahan Citra Digital - UTS")
    
    st.markdown("""
    Aplikasi interaktif untuk perbaikan kualitas citra digital. 
    Unggah citra Anda, pilih mode perbaikan, dan lihat hasilnya beserta analisis histogram.
    """)
    st.markdown("---")