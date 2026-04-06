"""
Capa Bronze: Extracción desde SQL Server y API CEPALSTAT
ODS 12 - Desperdicio de alimentos Bolivia
"""
import pandas as pd
import pyodbc
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SQL_CONFIG

# ─── SQL SERVER ───────────────────────────────────────────

def extract_sql_server(query):
    try:
        conn_str = (
            f"DRIVER={SQL_CONFIG['driver']};"
            f"SERVER={SQL_CONFIG['server']};"
            f"DATABASE={SQL_CONFIG['database']};"
            f"Trusted_Connection=yes;"
        )
        print("Conectando a:", SQL_CONFIG['server'])
        print("Base de datos:", SQL_CONFIG['database'])
        conn = pyodbc.connect(conn_str)
        df = pd.read_sql(query, conn)
        conn.close()
        print(f"✅ SQL Server: {len(df)} registros extraídos")
        return df
    except Exception as e:
        print(f"❌ Error SQL Server: {e}")
        return None

def save_bronze(df, filename):
    if df is not None:
        os.makedirs("data/bronze", exist_ok=True)
        df.to_csv(f"data/bronze/{filename}.csv", index=False)
        print(f"✅ Guardado: data/bronze/{filename}.csv")

# ─── CEPALSTAT ────────────────────────────────────────────

def extract_cepal(indicator_id=316, country="BOL"):
    """
    Extrae indicador de CEPALSTAT para Bolivia.
    Si la API falla, usa datos de respaldo simulados (fallback ODS 12).
    """
    url = "https://api.cepalstat.org/cepalstat/api/v1/indicator/data"
    params = {
        "indicator": indicator_id,
        "members": country,
        "format": "json",
        "lang": "es"
    }
    try:
        print(f"🌐 Conectando a CEPALSTAT (indicador {indicator_id})...")
        response = requests.get(url, params=params, timeout=10)

        assert response.status_code == 200, \
            f"❌ CEPALSTAT respondió con código {response.status_code}"
        data = response.json()
        assert "data" in data and len(data["data"]) > 0, \
            "❌ CEPALSTAT: sin registros"

        df = pd.DataFrame(data["data"])
        print(f"✅ CEPALSTAT: {len(df)} registros extraídos")
        return df

    except Exception as e:
        print(f"⚠️ CEPALSTAT no disponible: {e}")
        print("🔄 Usando datos de respaldo (fallback ODS 12)...")

        # Datos simulados de consumo de alimentos Bolivia (fuente: CEPAL estimado)
        fallback = pd.DataFrame({
            "country": ["BOL"] * 6,
            "indicator": ["Consumo de alimentos per capita"] * 6,
            "year": [2018, 2019, 2020, 2021, 2022, 2023],
            "value": [2450, 2480, 2310, 2390, 2460, 2500],
            "unit": ["kcal/persona/dia"] * 6
        })
        print(f"✅ Fallback cargado: {len(fallback)} registros")
        return fallback
    
    # ─── MAIN ─────────────────────────────────────────────────

if __name__ == "__main__":
    # Extracción SQL Server
    df_ventas = extract_sql_server("SELECT * FROM Ventas")
    save_bronze(df_ventas, "ventas")

    # Extracción CEPALSTAT
    df_cepal = extract_cepal(indicator_id=316, country="BOL")
    save_bronze(df_cepal, "cepal_consumo_bolivia")