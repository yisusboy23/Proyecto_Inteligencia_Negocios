"""
Capa Bronze: Extracción desde SQL Server
"""
import pandas as pd
import pyodbc
from config import SQL_CONFIG

def extract_sql_server(query):
    try:
        conn_str = (
            f"DRIVER={SQL_CONFIG['driver']};"
            f"SERVER={SQL_CONFIG['server']};"
            f"DATABASE={SQL_CONFIG['database']};"
            f"UID={SQL_CONFIG['username']};"
            f"PWD={SQL_CONFIG['password']}"
        )
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
        df.to_csv(f"data/bronze/{filename}.csv", index=False)
        print(f"✅ Guardado: data/bronze/{filename}.csv")

if __name__ == "__main__":
    query = "SELECT TOP 100 * FROM tu_tabla"
    df = extract_sql_server(query)
    save_bronze(df, "datos_empresa")