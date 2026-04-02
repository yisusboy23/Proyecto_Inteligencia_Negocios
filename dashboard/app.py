import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Dashboard BI - Supermercados Bolivia")
st.markdown("### Optimización de Desperdicio de Alimentos")

# Cargar datos
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/silver/ventas_clean.csv")
        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Mostrar columnas disponibles
    st.write("Columnas disponibles:", df.columns.tolist())
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    
    # Calcular total de ventas
    if 'precio_unitario' in df.columns and 'cantidad' in df.columns:
        df['total_venta'] = df['cantidad'] * df['precio_unitario']
        total_ventas = df['total_venta'].sum()
        col1.metric("💰 Total Ventas", f"${total_ventas:,.0f}")
    
    col2.metric("📈 Registros", len(df))
    col3.metric("🎯 ODS 12", "Consumo Responsable")
    
    # Gráfico de ventas por fecha
    if 'fecha' in df.columns and 'total_venta' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'])
        ventas_por_fecha = df.groupby('fecha')['total_venta'].sum().reset_index()
        fig = px.line(ventas_por_fecha, x='fecha', y='total_venta', title="Tendencia de Ventas")
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos
    st.subheader("📋 Datos de Ventas")
    st.dataframe(df)
else:
    st.warning("No se encontraron datos. Ejecuta primero bronze/extract_sql.py")