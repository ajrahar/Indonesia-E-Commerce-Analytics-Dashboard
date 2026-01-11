"""
Aplikasi Streamlit: Analisis E-Commerce Indonesia 2023-2025
Dashboard interaktif untuk menganalisis data penjualan, pengiriman, dan pembayaran e-commerce
"""

import streamlit as st
import pandas as pd
from utils.data_processor import (
    load_from_kaggle,
    load_from_csv,
    validate_dataframe,
    clean_and_transform,
    get_date_range
)
from components.overview import render_overview
from components.sales_analysis import render_sales_analysis
from components.shipping_analysis import render_shipping_analysis
from components.payment_analysis import render_payment_analysis
from components.geographic_analysis import render_geographic_analysis

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis E-Commerce Indonesia",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        font-size: 1.1rem;
    }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🛒 Analisis E-Commerce Indonesia 2023-2025</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Dashboard Interaktif untuk Analisis Penjualan, Pengiriman & Pembayaran</div>', unsafe_allow_html=True)

# Sidebar untuk data loading
with st.sidebar:
    st.header("📂 Muat Data")
    
    # Pilihan mode loading
    data_source = st.radio(
        "Pilih Sumber Data:",
        ["🌐 Load dari Kaggle", "📁 Upload File CSV"],
        help="Pilih cara memuat data: otomatis dari Kaggle atau upload file CSV manual"
    )
    
    st.divider()
    
    # Initialize session state untuk data
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    # Mode 1: Load dari Kaggle
    if data_source == "🌐 Load dari Kaggle":
        st.info("💡 Data akan dimuat langsung dari Kaggle dataset")
        
        if st.button("🚀 Muat Data dari Kaggle", type="primary", use_container_width=True):
            with st.spinner("⏳ Memuat data dari Kaggle..."):
                df = load_from_kaggle()
                
                if df is not None:
                    # Validasi data
                    is_valid, message = validate_dataframe(df)
                    
                    if is_valid:
                        # Clean dan transform
                        df = clean_and_transform(df)
                        st.session_state.df = df
                        st.session_state.data_loaded = True
                        st.success(f"✅ Data berhasil dimuat! ({len(df):,} baris)")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Gagal memuat data dari Kaggle")
    
    # Mode 2: Upload CSV
    else:
        st.info("💡 Upload file CSV dari komputer Anda")
        
        uploaded_file = st.file_uploader(
            "Pilih file CSV",
            type=['csv'],
            help="Upload file CSV dengan data e-commerce"
        )
        
        if uploaded_file is not None:
            with st.spinner("⏳ Memproses file CSV..."):
                df = load_from_csv(uploaded_file)
                
                if df is not None:
                    # Validasi data
                    is_valid, message = validate_dataframe(df)
                    
                    if is_valid:
                        # Clean dan transform
                        df = clean_and_transform(df)
                        st.session_state.df = df
                        st.session_state.data_loaded = True
                        st.success(f"✅ Data berhasil dimuat! ({len(df):,} baris)")
                    else:
                        st.error(f"❌ {message}")
    
    # Informasi data jika sudah dimuat
    if st.session_state.data_loaded and st.session_state.df is not None:
        st.divider()
        st.subheader("ℹ️ Informasi Data")
        
        df = st.session_state.df
        
        st.metric("📊 Total Baris", f"{len(df):,}")
        st.metric("📋 Total Kolom", f"{len(df.columns):,}")
        
        # Rentang tanggal
        start_date, end_date = get_date_range(df)
        st.write(f"📅 **Periode Data:**")
        st.write(f"{start_date} - {end_date}")
        
        # Tombol untuk reset data
        if st.button("🔄 Reset Data", use_container_width=True):
            st.session_state.df = None
            st.session_state.data_loaded = False
            st.rerun()

# Main content
if st.session_state.data_loaded and st.session_state.df is not None:
    df = st.session_state.df
    
    # Tabs untuk navigasi
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "📈 Analisis Penjualan",
        "🚚 Analisis Pengiriman",
        "💳 Analisis Pembayaran",
        "🗺️ Analisis Geografis",
        "📋 Data Mentah"
    ])
    
    with tab1:
        render_overview(df)
    
    with tab2:
        render_sales_analysis(df)
    
    with tab3:
        render_shipping_analysis(df)
    
    with tab4:
        render_payment_analysis(df)
    
    with tab5:
        render_geographic_analysis(df)
    
    with tab6:
        st.header("📋 Data Mentah")
        
        st.info(f"📊 Menampilkan {len(df):,} baris data")
        
        # Filter kolom
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect(
            "Pilih kolom yang ingin ditampilkan:",
            all_columns,
            default=all_columns[:10] if len(all_columns) > 10 else all_columns
        )
        
        if selected_columns:
            # Pagination
            rows_per_page = st.selectbox("Baris per halaman:", [10, 25, 50, 100, 500], index=2)
            total_pages = (len(df) - 1) // rows_per_page + 1
            page = st.number_input("Halaman:", min_value=1, max_value=total_pages, value=1)
            
            start_idx = (page - 1) * rows_per_page
            end_idx = min(start_idx + rows_per_page, len(df))
            
            st.dataframe(
                df[selected_columns].iloc[start_idx:end_idx],
                use_container_width=True,
                height=600
            )
            
            st.caption(f"Menampilkan baris {start_idx + 1} - {end_idx} dari {len(df):,} total baris")
            
            # Download data
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df[selected_columns].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Data (CSV)",
                    data=csv,
                    file_name="ecommerce_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Statistik deskriptif
                if st.button("📊 Lihat Statistik Deskriptif", use_container_width=True):
                    st.subheader("📊 Statistik Deskriptif")
                    st.dataframe(df[selected_columns].describe(), use_container_width=True)
        else:
            st.warning("⚠️ Pilih minimal satu kolom untuk ditampilkan")

else:
    # Tampilan awal sebelum data dimuat
    st.info("👈 Silakan muat data terlebih dahulu menggunakan sidebar")
    
    # Instruksi
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌐 Load dari Kaggle
        
        **Kelebihan:**
        - ✅ Tidak perlu download manual
        - ✅ Selalu mendapat data terbaru
        - ✅ Otomatis dan cepat
        
        **Cara Penggunaan:**
        1. Pilih opsi "Load dari Kaggle"
        2. Klik tombol "Muat Data dari Kaggle"
        3. Tunggu proses loading selesai
        """)
    
    with col2:
        st.markdown("""
        ### 📁 Upload File CSV
        
        **Kelebihan:**
        - ✅ Bisa menggunakan data custom
        - ✅ Tidak perlu koneksi internet
        - ✅ Kontrol penuh atas data
        
        **Cara Penggunaan:**
        1. Pilih opsi "Upload File CSV"
        2. Klik tombol "Browse files"
        3. Pilih file CSV dari komputer
        """)
    
    st.divider()
    
    # Informasi dataset
    st.markdown("""
    ### 📊 Tentang Dataset
    
    Dataset ini berisi data e-commerce Indonesia dari tahun 2023-2025 dengan lebih dari 20,000 baris data yang mencakup:
    
    - 🛒 **Data Pesanan**: ID pesanan, jumlah, berat, status
    - 💰 **Data Pembayaran**: Total pembayaran, metode pembayaran, diskon
    - 🚚 **Data Pengiriman**: Opsi pengiriman, biaya, estimasi
    - 📦 **Data Produk**: Kategori produk, jumlah kategori
    - 🗺️ **Data Geografis**: Kota/kabupaten, provinsi
    
    **Sumber Dataset**: [Kaggle - Indonesia E-Commerce Sales & Shipping 2023-2025](https://www.kaggle.com/datasets/bakitacos/indonesia-e-commerce-sales-and-shipping-20232025)
    """)

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>📊 Dashboard Analisis E-Commerce Indonesia | Dibuat dengan ❤️ menggunakan Streamlit</p>
    </div>
""", unsafe_allow_html=True)
