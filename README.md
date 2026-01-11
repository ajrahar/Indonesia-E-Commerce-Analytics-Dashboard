# 🛒 Indonesia E-Commerce Sales & Shipping Analytics Dashboard

### 📊 Interactive Streamlit Dashboard for Analyzing 20K+ E-Commerce Transactions (2023-2025)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Data](https://img.shields.io/badge/Data-20K%2B%20Rows-orange.svg)

> **Dashboard analisis e-commerce Indonesia yang komprehensif dengan dual-mode data loading, 20+ visualisasi interaktif, dan analisis mendalam dari 5 dimensi bisnis.**

---

## 📋 Deskripsi

Aplikasi dashboard interaktif berbasis **Streamlit** untuk menganalisis data e-commerce Indonesia dengan lebih dari **20,000 transaksi** dari tahun 2023-2025. Dashboard ini menyediakan insights mendalam tentang pola penjualan, preferensi pengiriman, metode pembayaran, dan distribusi geografis pelanggan.

**🎯 Cocok untuk:**
- Data Analyst yang ingin menganalisis tren e-commerce
- Business Intelligence untuk decision making
- E-commerce owners untuk memahami customer behavior
- Students & Researchers untuk belajar data visualization



## ✨ Fitur Utama

### 🌐 Dual-Mode Data Loading
- **Load dari Kaggle**: Otomatis download dataset dari Kaggle (memerlukan koneksi internet)
  - Auto-detect file CSV terbesar
  - Support multiple encoding (UTF-8, Latin1, ISO-8859-1, CP1252)
  - Intelligent error handling dengan fallback
- **Upload CSV Manual**: Upload file CSV dari komputer lokal
  - Support berbagai format dan encoding
  - Auto-detect delimiter (comma, semicolon, tab)
  - Skip bad lines untuk data yang tidak konsisten
  - Validasi fleksibel dengan auto-generate missing columns

### 📊 Validasi & Data Processing
- **Validasi Fleksibel**: Hanya 3 kolom wajib (total_qty, Total Pembayaran, Waktu Pesanan Dibuat)
- **Auto-Generate Missing Data**:
  - `order_id` dibuat otomatis jika tidak ada
  - Kolom numerik yang hilang diisi dengan 0
  - Kolom kategorikal yang hilang diisi dengan "Tidak Diketahui"
- **Robust Error Handling**: Informative messages dengan tips untuk user


### 📊 Dashboard Overview
- Metrik utama (Total Pesanan, Revenue, AOV, dll)
- Tren penjualan bulanan
- Distribusi status pesanan
- Top 10 kategori produk

### 📈 Analisis Penjualan
- Analisis revenue berdasarkan waktu (harian, bulanan, tahunan)
- Analisis kategori produk dengan treemap dan scatter plot
- Analisis pengaruh diskon terhadap nilai pesanan
- Analisis produk yang dikembalikan

### 🚚 Analisis Pengiriman
- Distribusi opsi pengiriman
- Analisis biaya pengiriman
- Perbandingan estimasi vs aktual
- Analisis berat pengiriman dan kategori

### 💳 Analisis Pembayaran
- Distribusi metode pembayaran
- Tren penggunaan metode pembayaran
- Analisis nilai transaksi per metode
- Statistik detail per metode

### 🗺️ Analisis Geografis
- Top kota/kabupaten berdasarkan pesanan dan revenue
- Analisis per provinsi dengan treemap
- Perbandingan regional (Jawa, Sumatera, Kalimantan, dll)
- Visualisasi hierarki dengan sunburst chart

### 📋 Data Mentah
- View dan filter data mentah
- Pagination untuk performa optimal
- Download data dalam format CSV
- Statistik deskriptif

## 🚀 Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi

1. **Clone atau download repository ini**
```bash
cd /Users/miftahul/Projects/Python/StreamLit/IECSS
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Jalankan aplikasi**
```bash
streamlit run app.py
```

4. **Buka browser**
Aplikasi akan otomatis terbuka di browser pada `http://localhost:8501`

## 📦 Dependencies

- `streamlit>=1.30.0` - Framework web app
- `pandas>=2.0.0` - Manipulasi data
- `plotly>=5.18.0` - Visualisasi interaktif
- `streamlit-extras>=0.3.0` - Komponen tambahan
- `kagglehub>=0.2.0` - Load data dari Kaggle
- `openpyxl>=3.1.0` - Support Excel (opsional)

## 📊 Struktur Data

Dataset harus memiliki kolom-kolom berikut:

| Kolom | Deskripsi | Tipe |
|-------|-----------|------|
| `order_id` | ID unik pesanan | String |
| `total_qty` | Total kuantitas produk | Integer |
| `total_weight_gr` | Total berat dalam gram | Float |
| `total_returned_qty` | Jumlah produk dikembalikan | Integer |
| `Total Diskon` | Total diskon | Float |
| `product_categories` | Kategori produk | String |
| `num_product_categories` | Jumlah kategori | Integer |
| `Status Pesanan` | Status pesanan | String |
| `Opsi Pengiriman` | Metode pengiriman | String |
| `Metode Pembayaran` | Metode pembayaran | String |
| `Kota/Kabupaten` | Kota/kabupaten tujuan | String |
| `Provinsi` | Provinsi tujuan | String |
| `Total Pembayaran` | Total pembayaran | Float |
| `Waktu Pesanan Dibuat` | Timestamp pesanan | DateTime |

## 🎯 Cara Penggunaan

### Mode 1: Load dari Kaggle
1. Buka aplikasi
2. Di sidebar, pilih "🌐 Load dari Kaggle"
3. Klik tombol "🚀 Muat Data dari Kaggle"
4. Tunggu proses loading selesai
5. Jelajahi berbagai tab analisis

### Mode 2: Upload CSV
1. Buka aplikasi
2. Di sidebar, pilih "📁 Upload File CSV"
3. Klik "Browse files" dan pilih file CSV
4. Tunggu proses upload dan validasi
5. Jelajahi berbagai tab analisis

## 📁 Struktur Proyek

```
IECSS/
├── app.py                          # File utama aplikasi
├── requirements.txt                # Dependencies
├── README.md                       # Dokumentasi
├── utils/
│   ├── __init__.py
│   └── data_processor.py          # Fungsi pemrosesan data
└── components/
    ├── __init__.py
    ├── overview.py                # Komponen dashboard overview
    ├── sales_analysis.py          # Komponen analisis penjualan
    ├── shipping_analysis.py       # Komponen analisis pengiriman
    ├── payment_analysis.py        # Komponen analisis pembayaran
    └── geographic_analysis.py     # Komponen analisis geografis
```

## 🎨 Fitur Visualisasi

Aplikasi menggunakan Plotly untuk visualisasi interaktif:
- 📊 Bar Charts
- 📈 Line Charts
- 🥧 Pie Charts
- 🗺️ Treemaps
- 🌅 Sunburst Charts
- 📉 Scatter Plots
- 📦 Box Plots
- 📊 Histograms

Semua grafik mendukung:
- Zoom dan pan
- Hover tooltips
- Download sebagai PNG
- Interaktivitas penuh

## 💡 Tips Penggunaan

1. **Performa**: Untuk dataset besar (>100K rows), gunakan fitur sampling pada scatter plots
2. **Filter**: Gunakan multiselect pada tab "Data Mentah" untuk fokus pada kolom tertentu
3. **Export**: Download hasil analisis dalam format CSV untuk analisis lebih lanjut
4. **Responsif**: Dashboard responsive dan dapat diakses dari berbagai ukuran layar

## 🐛 Troubleshooting

### Error saat load dari Kaggle
- **"Unsupported file extension"**: Fixed - aplikasi sekarang auto-detect file CSV
- **"Error tokenizing data"**: Fixed - support multiple encoding dan skip bad lines
- Pastikan koneksi internet stabil
- Coba beberapa kali jika timeout
- Alternatif: gunakan mode upload CSV

### Error saat upload CSV
- **"Expected X fields, saw Y"**: Fixed - auto-skip bad lines
- **"Encoding error"**: Fixed - support multiple encoding (UTF-8, Latin1, ISO-8859-1, CP1252)
- **"Kolom yang hilang"**: Fixed - auto-generate missing columns dengan nilai default
- Pastikan file dalam format CSV
- Gunakan delimiter standar (koma, semicolon, atau tab)

### Aplikasi lambat
- Tutup tab yang tidak digunakan
- Gunakan pagination pada data mentah
- Restart aplikasi jika perlu
- Clear cache dengan menekan 'C' di aplikasi

### Data tidak muncul
- Pastikan data sudah berhasil dimuat (cek sidebar)
- Reload halaman dengan menekan 'R'
- Cek console untuk error messages
- Pastikan minimal 10 baris data tersedia

## 📝 Lisensi

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan.

## 👨‍💻 Kontributor

Dibuat dengan ❤️ menggunakan Streamlit

## 🔗 Links

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Dataset Source](https://www.kaggle.com/datasets/bakitacos/indonesia-e-commerce-sales-and-shipping-20232025)

## 📧 Kontak

Untuk pertanyaan atau saran, silakan buat issue di repository ini.

---

**Selamat menganalisis! 🚀**
