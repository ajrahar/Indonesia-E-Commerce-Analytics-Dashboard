"""
Komponen untuk analisis pengiriman
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import format_currency, format_number


def render_shipping_analysis(df: pd.DataFrame):
    """
    Render halaman analisis pengiriman
    
    Args:
        df: DataFrame yang sudah dibersihkan
    """
    st.header("🚚 Analisis Pengiriman")
    
    tab1, tab2, tab3 = st.tabs([
        "📦 Opsi Pengiriman",
        "💵 Biaya Pengiriman",
        "⚖️ Berat Pengiriman"
    ])
    
    with tab1:
        render_shipping_options(df)
    
    with tab2:
        render_shipping_costs(df)
    
    with tab3:
        render_shipping_weight(df)


def render_shipping_options(df: pd.DataFrame):
    """
    Analisis opsi pengiriman
    """
    st.subheader("📦 Distribusi Opsi Pengiriman")
    
    if 'Opsi Pengiriman' not in df.columns:
        st.warning("⚠️ Data opsi pengiriman tidak tersedia")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Jumlah Pesanan per Opsi Pengiriman")
        
        shipping_counts = df['Opsi Pengiriman'].value_counts().reset_index()
        shipping_counts.columns = ['Opsi', 'Jumlah']
        
        fig = px.bar(
            shipping_counts,
            x='Opsi',
            y='Jumlah',
            color='Jumlah',
            color_continuous_scale='Blues',
            text='Jumlah'
        )
        
        fig.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Jumlah: %{y:,}<extra></extra>'
        )
        
        fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🥧 Persentase Opsi Pengiriman")
        
        fig = px.pie(
            shipping_counts,
            values='Jumlah',
            names='Opsi',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analisis revenue per opsi pengiriman
    st.markdown("#### 💰 Pendapatan per Opsi Pengiriman")
    
    shipping_revenue = df.groupby('Opsi Pengiriman').agg({
        'Total Pembayaran': ['sum', 'mean'],
        'order_id': 'count'
    }).reset_index()
    
    shipping_revenue.columns = ['Opsi', 'Total Pendapatan', 'Rata-rata Nilai', 'Jumlah Pesanan']
    shipping_revenue = shipping_revenue.sort_values('Total Pendapatan', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=shipping_revenue['Opsi'],
        y=shipping_revenue['Total Pendapatan'],
        name='Total Pendapatan',
        marker_color='#2ecc71',
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>Total: Rp %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=shipping_revenue['Opsi'],
        y=shipping_revenue['Rata-rata Nilai'],
        name='Rata-rata Nilai',
        marker_color='#e74c3c',
        yaxis='y2',
        mode='lines+markers',
        hovertemplate='<b>%{x}</b><br>Rata-rata: Rp %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        yaxis=dict(title='Total Pendapatan (Rp)', side='left'),
        yaxis2=dict(title='Rata-rata Nilai Pesanan (Rp)', overlaying='y', side='right'),
        hovermode='x unified',
        height=400,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_shipping_costs(df: pd.DataFrame):
    """
    Analisis biaya pengiriman
    """
    st.subheader("💵 Analisis Biaya Pengiriman")
    
    # Metrik ringkasan
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Ongkos Kirim Dibayar oleh Pembeli' in df.columns:
            avg_cost = df['Ongkos Kirim Dibayar oleh Pembeli'].mean()
            st.metric("📊 Rata-rata Ongkir", format_currency(avg_cost))
    
    with col2:
        if 'Ongkos Kirim Dibayar oleh Pembeli' in df.columns:
            total_cost = df['Ongkos Kirim Dibayar oleh Pembeli'].sum()
            st.metric("💰 Total Ongkir", format_currency(total_cost))
    
    with col3:
        if 'Perkiraan Ongkos Kirim' in df.columns:
            avg_estimate = df['Perkiraan Ongkos Kirim'].mean()
            st.metric("📈 Rata-rata Estimasi", format_currency(avg_estimate))
    
    with col4:
        if 'Estimasi Potongan Biaya Pengiriman' in df.columns:
            avg_discount = df['Estimasi Potongan Biaya Pengiriman'].mean()
            st.metric("🏷️ Rata-rata Potongan", format_currency(avg_discount))
    
    st.divider()
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Distribusi biaya pengiriman
        if 'Ongkos Kirim Dibayar oleh Pembeli' in df.columns:
            st.markdown("#### 📊 Distribusi Biaya Pengiriman")
            
            fig = px.histogram(
                df,
                x='Ongkos Kirim Dibayar oleh Pembeli',
                nbins=50,
                color_discrete_sequence=['#3498db'],
                labels={'Ongkos Kirim Dibayar oleh Pembeli': 'Biaya Pengiriman (Rp)'}
            )
            
            fig.update_traces(
                hovertemplate='Biaya: Rp %{x:,.0f}<br>Jumlah: %{y}<extra></extra>'
            )
            
            fig.update_layout(
                height=400,
                xaxis_title='Biaya Pengiriman (Rp)',
                yaxis_title='Jumlah Pesanan'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        # Biaya pengiriman per opsi
        if 'Opsi Pengiriman' in df.columns and 'Ongkos Kirim Dibayar oleh Pembeli' in df.columns:
            st.markdown("#### 📦 Biaya Rata-rata per Opsi Pengiriman")
            
            shipping_avg_cost = df.groupby('Opsi Pengiriman')['Ongkos Kirim Dibayar oleh Pembeli'].mean().sort_values(ascending=True).reset_index()
            shipping_avg_cost.columns = ['Opsi', 'Rata-rata Biaya']
            
            fig = px.bar(
                shipping_avg_cost,
                y='Opsi',
                x='Rata-rata Biaya',
                orientation='h',
                color='Rata-rata Biaya',
                color_continuous_scale='Greens',
                text='Rata-rata Biaya'
            )
            
            fig.update_traces(
                texttemplate='Rp %{text:,.0f}',
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Rata-rata: Rp %{x:,.0f}<extra></extra>'
            )
            
            fig.update_layout(
                height=400,
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Perbandingan estimasi vs aktual
    if 'Perkiraan Ongkos Kirim' in df.columns and 'Ongkos Kirim Dibayar oleh Pembeli' in df.columns:
        st.markdown("#### 🔍 Perbandingan Estimasi vs Aktual")
        
        # Ambil sample untuk visualisasi (max 1000 points)
        df_sample = df.sample(min(1000, len(df)))
        
        fig = px.scatter(
            df_sample,
            x='Perkiraan Ongkos Kirim',
            y='Ongkos Kirim Dibayar oleh Pembeli',
            color='Opsi Pengiriman',
            labels={
                'Perkiraan Ongkos Kirim': 'Estimasi Ongkir (Rp)',
                'Ongkos Kirim Dibayar oleh Pembeli': 'Ongkir Aktual (Rp)'
            },
            opacity=0.6
        )
        
        # Tambahkan garis diagonal (perfect estimate)
        max_val = max(df_sample['Perkiraan Ongkos Kirim'].max(), df_sample['Ongkos Kirim Dibayar oleh Pembeli'].max())
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            name='Estimasi Sempurna',
            line=dict(color='red', dash='dash'),
            hovertemplate='Garis Estimasi Sempurna<extra></extra>'
        ))
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)


def render_shipping_weight(df: pd.DataFrame):
    """
    Analisis berat pengiriman
    """
    st.subheader("⚖️ Analisis Berat Pengiriman")
    
    if 'total_weight_gr' not in df.columns:
        st.warning("⚠️ Data berat pengiriman tidak tersedia")
        return
    
    # Konversi ke kg
    df_weight = df.copy()
    df_weight['total_weight_kg'] = df_weight['total_weight_gr'] / 1000
    
    # Metrik
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_weight = df_weight['total_weight_kg'].mean()
        st.metric("📊 Rata-rata Berat", f"{avg_weight:.2f} kg")
    
    with col2:
        total_weight = df_weight['total_weight_kg'].sum()
        st.metric("⚖️ Total Berat", f"{total_weight:,.0f} kg")
    
    with col3:
        max_weight = df_weight['total_weight_kg'].max()
        st.metric("📈 Berat Maksimal", f"{max_weight:,.2f} kg")
    
    st.divider()
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Distribusi berat
        st.markdown("#### 📊 Distribusi Berat Pengiriman")
        
        fig = px.histogram(
            df_weight,
            x='total_weight_kg',
            nbins=50,
            color_discrete_sequence=['#9b59b6'],
            labels={'total_weight_kg': 'Berat (kg)'}
        )
        
        fig.update_traces(
            hovertemplate='Berat: %{x:.2f} kg<br>Jumlah: %{y}<extra></extra>'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title='Berat (kg)',
            yaxis_title='Jumlah Pesanan'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        # Hubungan berat dengan biaya pengiriman
        if 'Ongkos Kirim Dibayar oleh Pembeli' in df_weight.columns:
            st.markdown("#### 💰 Hubungan Berat vs Biaya Pengiriman")
            
            # Sample untuk performa
            df_sample = df_weight.sample(min(1000, len(df_weight)))
            
            fig = px.scatter(
                df_sample,
                x='total_weight_kg',
                y='Ongkos Kirim Dibayar oleh Pembeli',
                color='Opsi Pengiriman' if 'Opsi Pengiriman' in df_sample.columns else None,
                labels={
                    'total_weight_kg': 'Berat (kg)',
                    'Ongkos Kirim Dibayar oleh Pembeli': 'Biaya Pengiriman (Rp)'
                },
                opacity=0.6
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Kategori berat
    st.markdown("#### 📦 Kategori Berat Pengiriman")
    
    df_weight['Kategori Berat'] = pd.cut(
        df_weight['total_weight_kg'],
        bins=[0, 1, 5, 10, 20, float('inf')],
        labels=['Sangat Ringan (< 1kg)', 'Ringan (1-5kg)', 'Sedang (5-10kg)', 'Berat (10-20kg)', 'Sangat Berat (> 20kg)']
    )
    
    weight_category = df_weight['Kategori Berat'].value_counts().reset_index()
    weight_category.columns = ['Kategori', 'Jumlah']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            weight_category,
            values='Jumlah',
            names='Kategori',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pendapatan per kategori berat
        weight_revenue = df_weight.groupby('Kategori Berat')['Total Pembayaran'].sum().reset_index()
        weight_revenue.columns = ['Kategori', 'Total Pendapatan']
        
        fig = px.bar(
            weight_revenue,
            x='Kategori',
            y='Total Pendapatan',
            color='Total Pendapatan',
            color_continuous_scale='Purples'
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Pendapatan: Rp %{y:,.0f}<extra></extra>'
        )
        
        fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
