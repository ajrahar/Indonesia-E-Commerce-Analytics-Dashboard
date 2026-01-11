"""
Komponen untuk analisis geografis
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import format_currency, format_number


def render_geographic_analysis(df: pd.DataFrame):
    """
    Render halaman analisis geografis
    
    Args:
        df: DataFrame yang sudah dibersihkan
    """
    st.header("🗺️ Analisis Geografis")
    
    tab1, tab2, tab3 = st.tabs([
        "🏙️ Analisis Kota/Kabupaten",
        "🗺️ Analisis Provinsi",
        "📊 Perbandingan Regional"
    ])
    
    with tab1:
        render_city_analysis(df)
    
    with tab2:
        render_province_analysis(df)
    
    with tab3:
        render_regional_comparison(df)


def render_city_analysis(df: pd.DataFrame):
    """
    Analisis berdasarkan kota/kabupaten
    """
    st.subheader("🏙️ Analisis per Kota/Kabupaten")
    
    if 'Kota/Kabupaten' not in df.columns:
        st.warning("⚠️ Data kota/kabupaten tidak tersedia")
        return
    
    # Agregasi per kota
    city_stats = df.groupby('Kota/Kabupaten').agg({
        'order_id': 'count',
        'Total Pembayaran': 'sum',
        'total_qty': 'sum',
        'Ongkos Kirim Dibayar oleh Pembeli': 'mean' if 'Ongkos Kirim Dibayar oleh Pembeli' in df.columns else 'count'
    }).reset_index()
    
    city_stats.columns = ['Kota', 'Jumlah Pesanan', 'Total Pendapatan', 'Total Qty', 'Rata-rata Ongkir']
    city_stats = city_stats.sort_values('Total Pendapatan', ascending=False)
    
    # Metrik top cities
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_city = city_stats.iloc[0]
        st.metric(
            "🏆 Kota Teratas (Pendapatan)",
            top_city['Kota'],
            format_currency(top_city['Total Pendapatan'])
        )
    
    with col2:
        top_orders_city = city_stats.sort_values('Jumlah Pesanan', ascending=False).iloc[0]
        st.metric(
            "📦 Kota Teratas (Pesanan)",
            top_orders_city['Kota'],
            format_number(top_orders_city['Jumlah Pesanan'])
        )
    
    with col3:
        total_cities = len(city_stats)
        st.metric(
            "🏙️ Total Kota/Kabupaten",
            format_number(total_cities)
        )
    
    st.divider()
    
    # Top 20 kota
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### 🏆 Top 20 Kota - Pendapatan")
        
        top_cities_revenue = city_stats.head(20)
        
        fig = px.bar(
            top_cities_revenue,
            y='Kota',
            x='Total Pendapatan',
            orientation='h',
            color='Jumlah Pesanan',
            color_continuous_scale='Blues',
            labels={'Total Pendapatan': 'Total Pendapatan (Rp)'}
        )
        
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>Pendapatan: Rp %{x:,.0f}<br>Pesanan: %{marker.color}<extra></extra>'
        )
        
        fig.update_layout(
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.markdown("#### 📦 Top 20 Kota - Jumlah Pesanan")
        
        top_cities_orders = city_stats.sort_values('Jumlah Pesanan', ascending=False).head(20)
        
        fig = px.bar(
            top_cities_orders,
            y='Kota',
            x='Jumlah Pesanan',
            orientation='h',
            color='Total Pendapatan',
            color_continuous_scale='Greens',
            labels={'Jumlah Pesanan': 'Jumlah Pesanan'}
        )
        
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>Pesanan: %{x:,}<br>Pendapatan: Rp %{marker.color:,.0f}<extra></extra>'
        )
        
        fig.update_layout(
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plot
    st.markdown("#### 📊 Hubungan Pesanan vs Pendapatan per Kota")
    
    fig = px.scatter(
        city_stats.head(50),
        x='Jumlah Pesanan',
        y='Total Pendapatan',
        size='Total Qty',
        color='Rata-rata Ongkir',
        hover_name='Kota',
        color_continuous_scale='Viridis',
        labels={
            'Jumlah Pesanan': 'Jumlah Pesanan',
            'Total Pendapatan': 'Total Pendapatan (Rp)',
            'Rata-rata Ongkir': 'Rata-rata Ongkir (Rp)'
        }
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def render_province_analysis(df: pd.DataFrame):
    """
    Analisis berdasarkan provinsi
    """
    st.subheader("🗺️ Analisis per Provinsi")
    
    if 'Provinsi' not in df.columns:
        st.warning("⚠️ Data provinsi tidak tersedia")
        return
    
    # Agregasi per provinsi
    province_stats = df.groupby('Provinsi').agg({
        'order_id': 'count',
        'Total Pembayaran': ['sum', 'mean'],
        'total_qty': 'sum',
        'Kota/Kabupaten': 'nunique' if 'Kota/Kabupaten' in df.columns else 'count'
    }).reset_index()
    
    province_stats.columns = ['Provinsi', 'Jumlah Pesanan', 'Total Pendapatan', 'Rata-rata Nilai', 'Total Qty', 'Jumlah Kota']
    province_stats = province_stats.sort_values('Total Pendapatan', ascending=False)
    
    # Metrik
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        top_province = province_stats.iloc[0]
        st.metric(
            "🏆 Provinsi Teratas",
            top_province['Provinsi']
        )
    
    with col2:
        st.metric(
            "💰 Pendapatan Teratas",
            format_currency(top_province['Total Pendapatan'])
        )
    
    with col3:
        total_provinces = len(province_stats)
        st.metric(
            "🗺️ Total Provinsi",
            format_number(total_provinces)
        )
    
    with col4:
        avg_per_province = province_stats['Total Pendapatan'].mean()
        st.metric(
            "📊 Rata-rata per Provinsi",
            format_currency(avg_per_province)
        )
    
    st.divider()
    
    # Visualisasi
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Top 15 Provinsi - Pendapatan")
        
        top_provinces = province_stats.head(15)
        
        fig = px.bar(
            top_provinces,
            x='Provinsi',
            y='Total Pendapatan',
            color='Jumlah Pesanan',
            color_continuous_scale='Oranges',
            labels={'Total Pendapatan': 'Total Pendapatan (Rp)'}
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Pendapatan: Rp %{y:,.0f}<br>Pesanan: %{marker.color}<extra></extra>'
        )
        
        fig.update_layout(
            height=500,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🥧 Distribusi Pendapatan Top 10 Provinsi")
        
        top_10_provinces = province_stats.head(10)
        
        fig = px.pie(
            top_10_provinces,
            values='Total Pendapatan',
            names='Provinsi',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Treemap
    st.markdown("#### 🗺️ Peta Hierarki Pendapatan per Provinsi")
    
    fig = px.treemap(
        province_stats.head(20),
        path=['Provinsi'],
        values='Total Pendapatan',
        color='Jumlah Pesanan',
        color_continuous_scale='RdYlGn',
        hover_data=['Total Qty', 'Rata-rata Nilai']
    )
    
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Pendapatan: Rp %{value:,.0f}<br>Pesanan: %{color}<extra></extra>'
    )
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)


def render_regional_comparison(df: pd.DataFrame):
    """
    Perbandingan antar regional
    """
    st.subheader("📊 Perbandingan Regional")
    
    if 'Provinsi' not in df.columns:
        st.warning("⚠️ Data provinsi tidak tersedia")
        return
    
    # Kategorisasi regional (simplified - bisa disesuaikan)
    def categorize_region(province):
        # Mapping sederhana - bisa diperluas
        jawa = ['DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Banten', 'DI Yogyakarta']
        sumatera = ['Sumatera Utara', 'Sumatera Barat', 'Sumatera Selatan', 'Riau', 'Jambi', 'Bengkulu', 'Lampung', 'Aceh', 'Kepulauan Riau', 'Bangka Belitung']
        kalimantan = ['Kalimantan Barat', 'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara']
        sulawesi = ['Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat']
        
        if province in jawa:
            return 'Jawa'
        elif province in sumatera:
            return 'Sumatera'
        elif province in kalimantan:
            return 'Kalimantan'
        elif province in sulawesi:
            return 'Sulawesi'
        else:
            return 'Lainnya'
    
    df_regional = df.copy()
    df_regional['Regional'] = df_regional['Provinsi'].apply(categorize_region)
    
    # Agregasi per regional
    regional_stats = df_regional.groupby('Regional').agg({
        'order_id': 'count',
        'Total Pembayaran': ['sum', 'mean'],
        'total_qty': 'sum',
        'Provinsi': 'nunique'
    }).reset_index()
    
    regional_stats.columns = ['Regional', 'Jumlah Pesanan', 'Total Pendapatan', 'Rata-rata Nilai', 'Total Qty', 'Jumlah Provinsi']
    regional_stats = regional_stats.sort_values('Total Pendapatan', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🗺️ Distribusi Pesanan per Regional")
        
        fig = px.pie(
            regional_stats,
            values='Jumlah Pesanan',
            names='Regional',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Pesanan: %{value:,}<br>Persentase: %{percent}<extra></extra>'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 Pendapatan per Regional")
        
        fig = px.bar(
            regional_stats,
            x='Regional',
            y='Total Pendapatan',
            color='Rata-rata Nilai',
            color_continuous_scale='Teal',
            text='Total Pendapatan',
            labels={'Total Pendapatan': 'Total Pendapatan (Rp)'}
        )
        
        fig.update_traces(
            texttemplate='Rp %{text:,.0f}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Pendapatan: Rp %{y:,.0f}<br>Rata-rata: Rp %{marker.color:,.0f}<extra></extra>'
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabel perbandingan
    st.markdown("#### 📋 Tabel Perbandingan Regional")
    
    # Format tabel
    display_stats = regional_stats.copy()
    display_stats['Total Pendapatan'] = display_stats['Total Pendapatan'].apply(format_currency)
    display_stats['Rata-rata Nilai'] = display_stats['Rata-rata Nilai'].apply(format_currency)
    display_stats['Jumlah Pesanan'] = display_stats['Jumlah Pesanan'].apply(format_number)
    display_stats['Total Qty'] = display_stats['Total Qty'].apply(format_number)
    
    st.dataframe(
        display_stats,
        hide_index=True,
        use_container_width=True
    )
    
    # Sunburst chart
    if 'Provinsi' in df_regional.columns:
        st.markdown("#### 🌅 Visualisasi Hierarki Regional-Provinsi")
        
        # Ambil top provinces per regional
        regional_province = df_regional.groupby(['Regional', 'Provinsi']).agg({
            'Total Pembayaran': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        regional_province.columns = ['Regional', 'Provinsi', 'Pendapatan', 'Pesanan']
        
        # Ambil top 5 per regional
        top_per_regional = regional_province.groupby('Regional').apply(
            lambda x: x.nlargest(5, 'Pendapatan')
        ).reset_index(drop=True)
        
        fig = px.sunburst(
            top_per_regional,
            path=['Regional', 'Provinsi'],
            values='Pendapatan',
            color='Pesanan',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Pendapatan: Rp %{value:,.0f}<extra></extra>'
        )
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
