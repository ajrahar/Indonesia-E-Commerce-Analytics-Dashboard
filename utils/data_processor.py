"""
Modul untuk memproses dan memuat data e-commerce
"""
import streamlit as st
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
from typing import Optional, Tuple
import os


@st.cache_data(show_spinner=False)
def load_from_kaggle() -> Optional[pd.DataFrame]:
    """
    Memuat dataset dari Kaggle menggunakan kagglehub
    
    Returns:
        DataFrame jika berhasil, None jika gagal
    """
    try:
        # Download dataset dari Kaggle
        # Ini akan download semua file ke local cache
        dataset_path = kagglehub.dataset_download(
            "bakitacos/indonesia-e-commerce-sales-and-shipping-20232025"
        )
        
        # Cari file CSV di dalam dataset
        import glob
        csv_files = glob.glob(os.path.join(dataset_path, "*.csv"))
        
        if not csv_files:
            st.error("❌ Tidak ditemukan file CSV di dataset")
            return None
        
        # Ambil file CSV pertama (atau yang paling besar jika ada multiple)
        csv_file = csv_files[0]
        if len(csv_files) > 1:
            # Pilih file terbesar
            csv_file = max(csv_files, key=os.path.getsize)
        
        st.info(f"📂 Memuat file: {os.path.basename(csv_file)}")
        
        # Coba berbagai encoding dan parameter (sama seperti load_from_csv)
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(
                    csv_file,
                    encoding=encoding,
                    on_bad_lines='skip',
                    engine='python',
                    sep=None,
                    skipinitialspace=True
                )
                
                if df is not None and len(df) > 0:
                    st.success(f"✅ Data berhasil dimuat dari Kaggle! ({len(df):,} baris, encoding: {encoding})")
                    return df
                    
            except Exception as e:
                continue
        
        # Jika semua encoding gagal, coba dengan parameter paling permisif
        df = pd.read_csv(
            csv_file,
            on_bad_lines='skip',
            engine='python',
            encoding_errors='ignore'
        )
        
        if df is not None and len(df) > 0:
            st.warning(f"⚠️ Data dimuat dengan beberapa baris dilewati ({len(df):,} baris)")
            return df
        
        return None
        
    except Exception as e:
        st.error(f"❌ Gagal memuat data dari Kaggle: {str(e)}")
        st.info("💡 Tip: Coba gunakan mode 'Upload File CSV' sebagai alternatif")
        return None


@st.cache_data(show_spinner=False)
def load_from_csv(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Memuat data dari file CSV yang diupload
    
    Args:
        uploaded_file: File yang diupload melalui Streamlit
        
    Returns:
        DataFrame jika berhasil, None jika gagal
    """
    try:
        # Coba berbagai encoding dan parameter
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                # Reset file pointer
                uploaded_file.seek(0)
                
                # Coba baca dengan encoding tertentu
                df = pd.read_csv(
                    uploaded_file,
                    encoding=encoding,
                    on_bad_lines='skip',  # Skip baris yang bermasalah
                    engine='python',  # Gunakan engine python untuk lebih fleksibel
                    sep=None,  # Auto-detect separator
                    skipinitialspace=True  # Skip spasi di awal
                )
                
                # Jika berhasil dan ada data, return
                if df is not None and len(df) > 0:
                    st.success(f"✅ File berhasil dibaca dengan encoding: {encoding}")
                    return df
                    
            except Exception as e:
                # Lanjut ke encoding berikutnya
                continue
        
        # Jika semua encoding gagal, coba dengan parameter default tapi lebih permisif
        uploaded_file.seek(0)
        df = pd.read_csv(
            uploaded_file,
            on_bad_lines='skip',
            engine='python',
            encoding_errors='ignore'  # Ignore encoding errors
        )
        
        if df is not None and len(df) > 0:
            st.warning("⚠️ File dibaca dengan beberapa baris dilewati karena format tidak konsisten")
            return df
        
        return None
        
    except Exception as e:
        st.error(f"❌ Gagal membaca file CSV: {str(e)}")
        st.info("💡 Tips: Pastikan file CSV Anda memiliki format yang konsisten dan gunakan delimiter standar (koma atau semicolon)")
        return None



def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validasi struktur DataFrame
    
    Args:
        df: DataFrame yang akan divalidasi
        
    Returns:
        Tuple (is_valid, message)
    """
    # Kolom yang diperlukan (core columns)
    required_columns = [
        'total_qty', 'Total Pembayaran', 'Waktu Pesanan Dibuat'
    ]
    
    # Kolom opsional tapi penting
    optional_columns = [
        'order_id', 'total_weight_gr', 'total_returned_qty',
        'Total Diskon', 'product_categories', 'num_product_categories',
        'Status Pesanan', 'Opsi Pengiriman', 'Metode Pembayaran',
        'Kota/Kabupaten', 'Provinsi', 'Ongkos Kirim Dibayar oleh Pembeli',
        'Perkiraan Ongkos Kirim', 'Estimasi Potongan Biaya Pengiriman'
    ]
    
    # Cek kolom yang tersedia
    available_columns = df.columns.tolist()
    
    # Cek kolom wajib
    missing_required = [col for col in required_columns if col not in available_columns]
    
    if missing_required:
        st.warning(f"⚠️ Kolom wajib yang hilang: {', '.join(missing_required)}")
        st.info(f"📋 Kolom yang tersedia: {', '.join(available_columns[:10])}...")
        return False, f"Kolom wajib yang hilang: {', '.join(missing_required)}"
    
    # Cek kolom opsional
    missing_optional = [col for col in optional_columns if col not in available_columns]
    
    if missing_optional:
        st.info(f"ℹ️ Beberapa kolom opsional tidak tersedia: {', '.join(missing_optional[:5])}...")
        st.info("Aplikasi akan tetap berjalan dengan fitur terbatas")
    
    # Validasi minimal jumlah baris
    if len(df) < 10:
        return False, f"⚠️ Data terlalu sedikit ({len(df)} baris). Minimal 10 baris diperlukan."
    
    return True, "✅ Data valid!"


def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan dan mentransformasi data
    
    Args:
        df: DataFrame mentah
        
    Returns:
        DataFrame yang sudah dibersihkan
    """
    df = df.copy()
    
    # Generate order_id jika tidak ada
    if 'order_id' not in df.columns:
        df['order_id'] = [f'ORD_{i:07d}' for i in range(1, len(df) + 1)]
        st.info("ℹ️ Kolom 'order_id' dibuat otomatis")
    
    # Konversi kolom tanggal
    if 'Waktu Pesanan Dibuat' in df.columns:
        df['Waktu Pesanan Dibuat'] = pd.to_datetime(df['Waktu Pesanan Dibuat'], errors='coerce')
        df['Tanggal'] = df['Waktu Pesanan Dibuat'].dt.date
        df['Bulan'] = df['Waktu Pesanan Dibuat'].dt.to_period('M').astype(str)
        df['Tahun'] = df['Waktu Pesanan Dibuat'].dt.year
        df['Hari'] = df['Waktu Pesanan Dibuat'].dt.day_name()
    
    # Konversi kolom numerik
    numeric_columns = [
        'total_qty', 'total_weight_gr', 'total_returned_qty',
        'Total Diskon', 'Total Pembayaran', 'Ongkos Kirim Dibayar oleh Pembeli',
        'Perkiraan Ongkos Kirim', 'Estimasi Potongan Biaya Pengiriman'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            # Buat kolom dengan nilai default 0 jika tidak ada
            df[col] = 0
    
    # Bersihkan nilai null di kolom kategorikal
    categorical_columns = [
        'Status Pesanan', 'Opsi Pengiriman', 'Metode Pembayaran',
        'Kota/Kabupaten', 'Provinsi', 'product_categories'
    ]
    
    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].fillna('Tidak Diketahui')
        else:
            # Buat kolom dengan nilai default jika tidak ada
            df[col] = 'Tidak Diketahui'
    
    # Handle kolom num_product_categories
    if 'num_product_categories' not in df.columns:
        df['num_product_categories'] = 1
    
    return df


def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Menghitung metrik-metrik penting
    
    Args:
        df: DataFrame yang sudah dibersihkan
        
    Returns:
        Dictionary berisi metrik-metrik
    """
    metrics = {
        'total_orders': len(df),
        'total_revenue': df['Total Pembayaran'].sum(),
        'avg_order_value': df['Total Pembayaran'].mean(),
        'total_qty_sold': df['total_qty'].sum(),
        'total_discount': df['Total Diskon'].sum(),
        'total_returned': df['total_returned_qty'].sum(),
        'return_rate': (df['total_returned_qty'].sum() / df['total_qty'].sum() * 100) if df['total_qty'].sum() > 0 else 0,
        'avg_shipping_cost': df['Ongkos Kirim Dibayar oleh Pembeli'].mean() if 'Ongkos Kirim Dibayar oleh Pembeli' in df.columns else 0,
    }
    
    return metrics


def get_date_range(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Mendapatkan rentang tanggal dari data
    
    Args:
        df: DataFrame
        
    Returns:
        Tuple (tanggal_awal, tanggal_akhir)
    """
    if 'Waktu Pesanan Dibuat' in df.columns:
        min_date = df['Waktu Pesanan Dibuat'].min()
        max_date = df['Waktu Pesanan Dibuat'].max()
        return min_date.strftime('%d %B %Y'), max_date.strftime('%d %B %Y')
    return "N/A", "N/A"


def format_currency(value: float) -> str:
    """
    Format angka menjadi format mata uang Rupiah
    
    Args:
        value: Nilai numerik
        
    Returns:
        String terformat
    """
    return f"Rp {value:,.0f}".replace(',', '.')


def format_number(value: float) -> str:
    """
    Format angka dengan pemisah ribuan
    
    Args:
        value: Nilai numerik
        
    Returns:
        String terformat
    """
    return f"{value:,.0f}".replace(',', '.')
