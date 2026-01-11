"""
Komponen untuk dashboard overview
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import calculate_metrics, format_currency, format_number


def render_overview(df: pd.DataFrame):
    """
    Render halaman overview dengan metrik utama dan visualisasi
    
    Args:
        df: DataFrame yang sudah dibersihkan
    """
    st.header("📊 Ringkasan Dashboard")
    
    # Hitung metrik
    metrics = calculate_metrics(df)
    
    # Tampilkan metrik utama dalam 4 kolom
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🛒 Total Pesanan",
            value=format_number(metrics['total_orders'])
        )
    
    with col2:
        st.metric(
            label="💰 Total Pendapatan",
            value=format_currency(metrics['total_revenue'])
        )
    
    with col3:
        st.metric(
            label="📦 Rata-rata Nilai Pesanan",
            value=format_currency(metrics['avg_order_value'])
        )
    
    with col4:
        st.metric(
            label="🎁 Total Produk Terjual",
            value=format_number(metrics['total_qty_sold'])
        )
    
    st.divider()
    
    # Baris kedua metrik
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="🏷️ Total Diskon",
            value=format_currency(metrics['total_discount'])
        )
    
    with col6:
        st.metric(
            label="↩️ Produk Dikembalikan",
            value=format_number(metrics['total_returned'])
        )
    
    with col7:
        st.metric(
            label="📊 Tingkat Pengembalian",
            value=f"{metrics['return_rate']:.2f}%"
        )
    
    with col8:
        st.metric(
            label="🚚 Rata-rata Ongkir",
            value=format_currency(metrics['avg_shipping_cost'])
        )
    
    st.divider()
    
    # Visualisasi
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Tren Penjualan Bulanan")
        render_monthly_trend(df)
    
    with col_right:
        st.subheader("📋 Distribusi Status Pesanan")
        render_order_status_distribution(df)
    
    st.divider()
    
    # Top kategori produk
    st.subheader("🏆 Top 10 Kategori Produk")
    render_top_categories(df)


def render_monthly_trend(df: pd.DataFrame):
    """
    Render grafik tren penjualan bulanan
    """
    if 'Bulan' not in df.columns:
        st.warning("⚠️ Data tanggal tidak tersedia")
        return
    
    # Agregasi per bulan
    monthly_sales = df.groupby('Bulan').agg({
        'Total Pembayaran': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    monthly_sales.columns = ['Bulan', 'Pendapatan', 'Jumlah Pesanan']
    
    # Buat grafik dengan dual axis
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=monthly_sales['Bulan'],
        y=monthly_sales['Pendapatan'],
        name='Pendapatan',
        marker_color='#1f77b4',
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>Pendapatan: Rp %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_sales['Bulan'],
        y=monthly_sales['Jumlah Pesanan'],
        name='Jumlah Pesanan',
        marker_color='#ff7f0e',
        yaxis='y2',
        mode='lines+markers',
        hovertemplate='<b>%{x}</b><br>Pesanan: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        yaxis=dict(title='Pendapatan (Rp)', side='left'),
        yaxis2=dict(title='Jumlah Pesanan', overlaying='y', side='right'),
        hovermode='x unified',
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_order_status_distribution(df: pd.DataFrame):
    """
    Render grafik distribusi status pesanan
    """
    if 'Status Pesanan' not in df.columns:
        st.warning("⚠️ Data status pesanan tidak tersedia")
        return
    
    status_counts = df['Status Pesanan'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Jumlah']
    
    fig = px.pie(
        status_counts,
        values='Jumlah',
        names='Status',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_top_categories(df: pd.DataFrame):
    """
    Render tabel dan grafik top kategori produk
    """
    if 'product_categories' not in df.columns:
        st.warning("⚠️ Data kategori produk tidak tersedia")
        return
    
    # Agregasi per kategori
    category_stats = df.groupby('product_categories').agg({
        'order_id': 'count',
        'Total Pembayaran': 'sum',
        'total_qty': 'sum'
    }).reset_index()
    
    category_stats.columns = ['Kategori', 'Jumlah Pesanan', 'Total Pendapatan', 'Total Qty']
    category_stats = category_stats.sort_values('Total Pendapatan', ascending=False).head(10)
    
    # Grafik bar horizontal
    fig = px.bar(
        category_stats,
        y='Kategori',
        x='Total Pendapatan',
        orientation='h',
        color='Jumlah Pesanan',
        color_continuous_scale='Blues',
        hover_data=['Total Qty'],
        labels={'Total Pendapatan': 'Pendapatan (Rp)', 'Jumlah Pesanan': 'Pesanan'}
    )
    
    fig.update_layout(
        height=500,
        xaxis_title='Total Pendapatan (Rp)',
        yaxis_title='Kategori Produk',
        yaxis={'categoryorder': 'total ascending'}
    )
    
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Pendapatan: Rp %{x:,.0f}<br>Pesanan: %{marker.color}<extra></extra>'
    )
    
    st.plotly_chart(fig, use_container_width=True)
