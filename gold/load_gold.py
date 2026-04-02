"""
Capa Gold: Carga a SQL Server
"""
import pandas as pd
import sys
import os
from sqlalchemy import create_engine, text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SQL_CONFIG

def load_to_sqlserver(df, table_name, if_exists='replace'):
    try:
        # Crear conexión con SQLAlchemy
        conn_str = (
            f"mssql+pyodbc://@{SQL_CONFIG['server']}/{SQL_CONFIG['database']}"
            f"?driver={SQL_CONFIG['driver']}&trusted_connection=yes"
        )
        engine = create_engine(conn_str)
        
        # Cargar datos
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        print(f"✅ Datos cargados: {table_name} - {len(df)} registros")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Cargar datos limpios
    df = pd.read_csv("data/silver/ventas_clean.csv")
    print(f"📊 Cargando {len(df)} registros a SQL Server...")
    
    # Cargar a tabla de hechos
    load_to_sqlserver(df, "HechoVentas")


    