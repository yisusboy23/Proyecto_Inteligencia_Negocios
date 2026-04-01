"""
Capa Gold: Carga a SQL Server
"""
import pandas as pd
import pyodbc
from config import SQL_CONFIG

def load_to_sqlserver(df, table_name, if_exists='replace'):
    try:
        conn_str = (
            f"DRIVER={SQL_CONFIG['driver']};"
            f"SERVER={SQL_CONFIG['server']};"
            f"DATABASE={SQL_CONFIG['database']};"
            f"UID={SQL_CONFIG['username']};"
            f"PWD={SQL_CONFIG['password']}"
        )
        conn = pyodbc.connect(conn_str)
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        conn.close()
        print(f"✅ Datos cargados: {table_name}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    df = pd.read_csv("data/silver/datos_empresa_clean.csv")
    load_to_sqlserver(df, "Hecho_Ventas")