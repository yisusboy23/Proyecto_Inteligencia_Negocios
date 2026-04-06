"""
Dashboard BI - Supermercados Bolivia
ODS 12: Optimización del Desperdicio de Alimentos
"""
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="BI Supermercados Bolivia")

st.title("📊 Dashboard BI - Supermercados Bolivia")
st.markdown("### 🎯 ODS 12: Optimización del Desperdicio de Alimentos")
st.markdown("---")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/silver/ventas_clean.csv")
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['total_venta'] = df['cantidad'] * df['precio_unitario']
        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:

    # ── FILTROS EN SIDEBAR ──────────────────────────────────
    st.sidebar.header("🔎 Filtros")

    # Filtro por rango de fechas
    fecha_min = df['fecha'].min().date()
    fecha_max = df['fecha'].max().date()
    rango_fechas = st.sidebar.date_input(
        "Rango de fechas",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )

    # Filtro por producto
    productos = sorted(df['id_producto'].unique().tolist())
    productos_sel = st.sidebar.multiselect(
        "Productos",
        options=productos,
        default=productos
    )

    # Filtro por geografía
    geografias = sorted(df['id_geografia'].unique().tolist())
    geo_sel = st.sidebar.multiselect(
        "Zona geográfica",
        options=geografias,
        default=geografias
    )

    # ── APLICAR FILTROS ─────────────────────────────────────
    if len(rango_fechas) == 2:
        fecha_inicio, fecha_fin = rango_fechas
        df_filtrado = df[
            (df['fecha'].dt.date >= fecha_inicio) &
            (df['fecha'].dt.date <= fecha_fin) &
            (df['id_producto'].isin(productos_sel)) &
            (df['id_geografia'].isin(geo_sel))
        ]
    else:
        df_filtrado = df

    # ── KPIs ────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    total_ventas = df_filtrado['total_venta'].sum()
    total_registros = len(df_filtrado)
    ticket_promedio = df_filtrado['total_venta'].mean() if total_registros > 0 else 0
    productos_unicos = df_filtrado['id_producto'].nunique()

    col1.metric("💰 Total Ventas", f"Bs. {total_ventas:,.0f}")
    col2.metric("📦 Transacciones", f"{total_registros:,}")
    col3.metric("🎫 Ticket Promedio", f"Bs. {ticket_promedio:,.1f}")
    col4.metric("🛒 Productos Activos", productos_unicos)

    st.markdown("---")

    # ── GRÁFICOS ────────────────────────────────────────────
    col_izq, col_der = st.columns(2)

    with col_izq:
        ventas_fecha = df_filtrado.groupby('fecha')['total_venta'].sum().reset_index()
        fig1 = px.line(
            ventas_fecha, x='fecha', y='total_venta',
            title="📈 Tendencia de Ventas",
            labels={'total_venta': 'Ventas (Bs.)', 'fecha': 'Fecha'}
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_der:
        ventas_producto = df_filtrado.groupby('id_producto')['total_venta'].sum().reset_index()
        fig2 = px.bar(
            ventas_producto, x='id_producto', y='total_venta',
            title="🛒 Ventas por Producto",
            labels={'total_venta': 'Ventas (Bs.)', 'id_producto': 'Producto'}
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Ventas por zona
    ventas_geo = df_filtrado.groupby('id_geografia')['total_venta'].sum().reset_index()
    fig3 = px.pie(
        ventas_geo, values='total_venta', names='id_geografia',
        title="🗺️ Distribución por Zona Geográfica"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # ── TABLA DETALLE ───────────────────────────────────────
    st.subheader("📋 Detalle de Ventas")
    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.warning("⚠️ No se encontraron datos. Ejecuta primero: py bronze/extract_sql.py")