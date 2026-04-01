import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Dashboard BI")

# Cargar datos
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/silver/datos_empresa_clean.csv")
    except:
        return pd.DataFrame({'fecha': [], 'ventas': []})

df = load_data()

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("💰 Ventas", f"${df['ventas'].sum():,.0f}" if not df.empty else "$0")
col2.metric("📈 Registros", len(df))
col3.metric("🎯 ODS 8", "Trabajo Decente")

# Gráfico
if not df.empty and 'fecha' in df.columns:
    fig = px.line(df, x='fecha', y='ventas', title="Tendencia")
    st.plotly_chart(fig, use_container_width=True)

st.dataframe(df)