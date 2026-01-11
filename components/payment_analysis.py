"""
Komponen untuk analisis pembayaran
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import format_currency, format_number


def render_payment_analysis(df: pd.DataFrame):
    """
    Render halaman analisis pembayaran
    
    Args:
        df: DataFrame yang sudah dibersihkan
    """
    st.header("💳 Analisis Pembayaran")
    
    if 'Metode Pembayaran' not in df.columns:
        st.warning("⚠️ Data metode pembayaran tidak tersedia")
        return
    
    # Metrik ringkasan
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_transactions = len(df)
        st.metric("💳 Total Transaksi", format_number(total_transactions))
    
    with col2:
        total_payment = df['Total Pembayaran'].sum()
        st.metric("💰 Total Pembayaran", format_currency(total_payment))
    
    with col3:
        avg_payment = df['Total Pembayaran'].mean()
        st.metric("📊 Rata-rata Pembayaran", format_currency(avg_payment))
    
    with col4:
        num_methods = df['Metode Pembayaran'].nunique()
        st.metric("🔢 Jumlah Metode", format_number(num_methods))
    
    st.divider()
    
    # Visualisasi
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📊 Distribusi Metode Pembayaran")
        render_payment_distribution(df)
    
    with col_right:
        st.subheader("💰 Pendapatan per Metode")
        render_payment_revenue(df)
    
    st.divider()
    
    # Analisis detail
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Tren Metode Pembayaran")
        render_payment_trend(df)
    
    with col2:
        st.subheader("🎯 Nilai Transaksi per Metode")
        render_payment_value_analysis(df)


def render_payment_distribution(df: pd.DataFrame):
    """
    Render distribusi metode pembayaran
    """
    payment_counts = df['Metode Pembayaran'].value_counts().reset_index()
    payment_counts.columns = ['Metode', 'Jumlah']
    
    fig = px.pie(
        payment_counts,
        values='Jumlah',
        names='Metode',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Jumlah: %{value:,}<br>Persentase: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_payment_revenue(df: pd.DataFrame):
    """
    Render pendapatan per metode pembayaran
    """
    payment_revenue = df.groupby('Metode Pembayaran').agg({
        'Total Pembayaran': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    payment_revenue.columns = ['Metode', 'Total Pendapatan', 'Jumlah Transaksi']
    payment_revenue = payment_revenue.sort_values('Total Pendapatan', ascending=True)
    
    fig = px.bar(
        payment_revenue,
        y='Metode',
        x='Total Pendapatan',
        orientation='h',
        color='Jumlah Transaksi',
        color_continuous_scale='Greens',
        text='Total Pendapatan',
        labels={'Total Pendapatan': 'Total Pendapatan (Rp)'}
    )
    
    fig.update_traces(
        texttemplate='Rp %{text:,.0f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Pendapatan: Rp %{x:,.0f}<br>Transaksi: %{marker.color}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_payment_trend(df: pd.DataFrame):
    """
    Render tren penggunaan metode pembayaran dari waktu ke waktu
    """
    if 'Bulan' not in df.columns:
        st.warning("⚠️ Data tanggal tidak tersedia")
        return
    
    # Agregasi per bulan dan metode
    payment_trend = df.groupby(['Bulan', 'Metode Pembayaran']).size().reset_index(name='Jumlah')
    
    # Ambil top 5 metode pembayaran
    top_methods = df['Metode Pembayaran'].value_counts().head(5).index.tolist()
    payment_trend_filtered = payment_trend[payment_trend['Metode Pembayaran'].isin(top_methods)]
    
    fig = px.line(
        payment_trend_filtered,
        x='Bulan',
        y='Jumlah',
        color='Metode Pembayaran',
        markers=True,
        labels={'Jumlah': 'Jumlah Transaksi'}
    )
    
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>%{x}<br>Transaksi: %{y}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_payment_value_analysis(df: pd.DataFrame):
    """
    Analisis nilai transaksi per metode pembayaran
    """
    payment_stats = df.groupby('Metode Pembayaran').agg({
        'Total Pembayaran': ['mean', 'median', 'min', 'max'],
        'order_id': 'count'
    }).reset_index()
    
    payment_stats.columns = ['Metode', 'Rata-rata', 'Median', 'Minimum', 'Maksimum', 'Jumlah']
    payment_stats = payment_stats.sort_values('Rata-rata', ascending=False)
    
    # Box plot
    fig = px.box(
        df,
        x='Metode Pembayaran',
        y='Total Pembayaran',
        color='Metode Pembayaran',
        labels={
            'Metode Pembayaran': 'Metode Pembayaran',
            'Total Pembayaran': 'Nilai Transaksi (Rp)'
        }
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Nilai: Rp %{y:,.0f}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabel statistik
    st.markdown("#### 📋 Statistik Detail per Metode Pembayaran")
    
    # Format currency columns
    for col in ['Rata-rata', 'Median', 'Minimum', 'Maksimum']:
        payment_stats[col] = payment_stats[col].apply(lambda x: format_currency(x))
    
    payment_stats['Jumlah'] = payment_stats['Jumlah'].apply(lambda x: format_number(x))
    
    st.dataframe(
        payment_stats,
        hide_index=True,
        use_container_width=True
    )
