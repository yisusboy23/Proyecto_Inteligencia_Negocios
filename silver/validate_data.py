"""
Capa Silver: Validación de datos con asserts
"""
import pandas as pd

def validate_dataframe(df, nombre_datos):
    print(f"\n🔍 Validando {nombre_datos}...")
    
    assert df is not None, f"❌ {nombre_datos}: DataFrame es None"
    assert not df.empty, f"❌ {nombre_datos}: DataFrame está vacío"
    print(f"✅ {nombre_datos}: {len(df)} registros")
    
    columnas_numericas = df.select_dtypes(include=['number']).columns
    for col in columnas_numericas:
        nulos = df[col].isnull().sum()
        if nulos > 0:
            print(f"⚠️ {col}: {nulos} nulos")
    
    print(f"✅ Validación completada\n")
    return True

if __name__ == "__main__":
    df = pd.read_csv("data/silver/datos_empresa_clean.csv")
    validate_dataframe(df, "Datos Empresa")