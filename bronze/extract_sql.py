"""
Capa Bronze: Extracción desde SQL Server
"""
import pandas as pd
import pyodbc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SQL_CONFIG

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
        print(f"✅ Datos extraídos: {len(df)} registros")
        return df
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def save_bronze(df, filename):
    if df is not None:
        os.makedirs("data/bronze", exist_ok=True)
        df.to_csv(f"data/bronze/{filename}.csv", index=False)
        print(f"✅ Guardado: data/bronze/{filename}.csv")

if __name__ == "__main__":
    query = "SELECT * FROM Ventas"
    df = extract_sql_server(query)
    save_bronze(df, "ventas")