"""
Komponen untuk analisis penjualan
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import format_currency, format_number


def render_sales_analysis(df: pd.DataFrame):
    """
    Render halaman analisis penjualan
    
    Args:
        df: DataFrame yang sudah dibersihkan
    """
    st.header("📈 Analisis Penjualan")
    
    # Tab untuk berbagai analisis
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Analisis Revenue",
        "📦 Analisis Kategori",
        "🏷️ Analisis Diskon",
        "↩️ Analisis Pengembalian"
    ])
    
    with tab1:
        render_revenue_analysis(df)
    
    with tab2:
        render_category_analysis(df)
    
    with tab3:
        render_discount_analysis(df)
    
    with tab4:
        render_return_analysis(df)


def render_revenue_analysis(df: pd.DataFrame):
    """
    Analisis revenue berdasarkan waktu
    """
    st.subheader("💰 Analisis Pendapatan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue per hari dalam seminggu
        if 'Hari' in df.columns:
            st.markdown("#### 📅 Pendapatan per Hari dalam Seminggu")
            
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_revenue = df.groupby('Hari')['Total Pembayaran'].sum().reindex(day_order).reset_index()
            day_revenue.columns = ['Hari', 'Pendapatan']
            
            # Translate hari ke Bahasa Indonesia
            day_translation = {
                'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
                'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
            }
            day_revenue['Hari'] = day_revenue['Hari'].map(day_translation)
            
            fig = px.bar(
                day_revenue,
                x='Hari',
                y='Pendapatan',
                color='Pendapatan',
                color_continuous_scale='Greens'
            )
            
            fig.update_traces(
                hovertemplate='<b>%{x}</b><br>Pendapatan: Rp %{y:,.0f}<extra></extra>'
            )
            
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue per tahun
        if 'Tahun' in df.columns:
            st.markdown("#### 📊 Pendapatan per Tahun")
            
            yearly_revenue = df.groupby('Tahun')['Total Pembayaran'].sum().reset_index()
            yearly_revenue.columns = ['Tahun', 'Pendapatan']
            
            fig = px.bar(
                yearly_revenue,
                x='Tahun',
                y='Pendapatan',
                color='Pendapatan',
                color_continuous_scale='Blues',
                text='Pendapatan'
            )
            
            fig.update_traces(
                texttemplate='Rp %{text:,.0f}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Pendapatan: Rp %{y:,.0f}<extra></extra>'
            )
            
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tren harian
    if 'Tanggal' in df.columns:
        st.markdown("#### 📈 Tren Pendapatan Harian")
        
        daily_revenue = df.groupby('Tanggal').agg({
            'Total Pembayaran': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        daily_revenue.columns = ['Tanggal', 'Pendapatan', 'Jumlah Pesanan']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_revenue['Tanggal'],
            y=daily_revenue['Pendapatan'],
            mode='lines',
            name='Pendapatan',
            fill='tozeroy',
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>%{x}</b><br>Pendapatan: Rp %{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            height=400,
            xaxis_title='Tanggal',
            yaxis_title='Pendapatan (Rp)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)


def render_category_analysis(df: pd.DataFrame):
    """
    Analisis berdasarkan kategori produk
    """
    st.subheader("📦 Analisis Kategori Produk")
    
    if 'product_categories' not in df.columns:
        st.warning("⚠️ Data kategori tidak tersedia")
        return
    
    # Statistik per kategori
    category_stats = df.groupby('product_categories').agg({
        'order_id': 'count',
        'Total Pembayaran': ['sum', 'mean'],
        'total_qty': 'sum',
        'Total Diskon': 'sum'
    }).reset_index()
    
    category_stats.columns = ['Kategori', 'Jumlah Pesanan', 'Total Pendapatan', 'Rata-rata Nilai', 'Total Qty', 'Total Diskon']
    category_stats = category_stats.sort_values('Total Pendapatan', ascending=False)
    
    # Tampilkan top 15
    top_categories = category_stats.head(15)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Top 15 Kategori - Pendapatan")
        
        fig = px.treemap(
            top_categories,
            path=['Kategori'],
            values='Total Pendapatan',
            color='Jumlah Pesanan',
            color_continuous_scale='RdYlGn',
            hover_data=['Total Qty', 'Rata-rata Nilai']
        )
        
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Pendapatan: Rp %{value:,.0f}<br>Pesanan: %{color}<extra></extra>'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Perbandingan Kategori")
        
        fig = px.scatter(
            top_categories,
            x='Jumlah Pesanan',
            y='Rata-rata Nilai',
            size='Total Pendapatan',
            color='Kategori',
            hover_data=['Total Qty'],
            labels={
                'Jumlah Pesanan': 'Jumlah Pesanan',
                'Rata-rata Nilai': 'Rata-rata Nilai Pesanan (Rp)'
            }
        )
        
        fig.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>Pesanan: %{x}<br>Rata-rata: Rp %{y:,.0f}<extra></extra>'
        )
        
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


def render_discount_analysis(df: pd.DataFrame):
    """
    Analisis pengaruh diskon
    """
    st.subheader("🏷️ Analisis Diskon")
    
    # Buat kategori diskon
    df_discount = df.copy()
    df_discount['Kategori Diskon'] = pd.cut(
        df_discount['Total Diskon'],
        bins=[-1, 0, 10000, 50000, 100000, float('inf')],
        labels=['Tanpa Diskon', 'Diskon Kecil (< 10rb)', 'Diskon Sedang (10-50rb)', 'Diskon Besar (50-100rb)', 'Diskon Sangat Besar (> 100rb)']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💵 Distribusi Kategori Diskon")
        
        discount_dist = df_discount['Kategori Diskon'].value_counts().reset_index()
        discount_dist.columns = ['Kategori', 'Jumlah']
        
        fig = px.pie(
            discount_dist,
            values='Jumlah',
            names='Kategori',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Pengaruh Diskon terhadap Nilai Pesanan")
        
        discount_impact = df_discount.groupby('Kategori Diskon').agg({
            'Total Pembayaran': 'mean',
            'total_qty': 'mean',
            'order_id': 'count'
        }).reset_index()
        
        discount_impact.columns = ['Kategori', 'Rata-rata Pembayaran', 'Rata-rata Qty', 'Jumlah Pesanan']
        
        fig = px.bar(
            discount_impact,
            x='Kategori',
            y='Rata-rata Pembayaran',
            color='Jumlah Pesanan',
            color_continuous_scale='Oranges',
            labels={'Rata-rata Pembayaran': 'Rata-rata Nilai Pesanan (Rp)'}
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Rata-rata: Rp %{y:,.0f}<br>Pesanan: %{marker.color}<extra></extra>'
        )
        
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


def render_return_analysis(df: pd.DataFrame):
    """
    Analisis produk yang dikembalikan
    """
    st.subheader("↩️ Analisis Pengembalian Produk")
    
    # Filter hanya yang ada pengembalian
    df_returns = df[df['total_returned_qty'] > 0].copy()
    
    if len(df_returns) == 0:
        st.info("ℹ️ Tidak ada data pengembalian produk")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "📦 Total Pesanan dengan Pengembalian",
            format_number(len(df_returns))
        )
    
    with col2:
        st.metric(
            "↩️ Total Produk Dikembalikan",
            format_number(df_returns['total_returned_qty'].sum())
        )
    
    with col3:
        return_rate = (len(df_returns) / len(df)) * 100
        st.metric(
            "📊 Persentase Pesanan dengan Pengembalian",
            f"{return_rate:.2f}%"
        )
    
    st.divider()
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Kategori dengan pengembalian tertinggi
        if 'product_categories' in df_returns.columns:
            st.markdown("#### 🏷️ Top 10 Kategori dengan Pengembalian Tertinggi")
            
            category_returns = df_returns.groupby('product_categories')['total_returned_qty'].sum().sort_values(ascending=False).head(10).reset_index()
            category_returns.columns = ['Kategori', 'Total Dikembalikan']
            
            fig = px.bar(
                category_returns,
                y='Kategori',
                x='Total Dikembalikan',
                orientation='h',
                color='Total Dikembalikan',
                color_continuous_scale='Reds'
            )
            
            fig.update_layout(
                height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        # Hubungan antara qty dan return
        st.markdown("#### 📊 Hubungan Qty Pesanan vs Qty Dikembalikan")
        
        fig = px.scatter(
            df_returns,
            x='total_qty',
            y='total_returned_qty',
            color='Total Pembayaran',
            color_continuous_scale='Viridis',
            labels={
                'total_qty': 'Total Qty Pesanan',
                'total_returned_qty': 'Qty Dikembalikan',
                'Total Pembayaran': 'Nilai Pesanan (Rp)'
            }
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
