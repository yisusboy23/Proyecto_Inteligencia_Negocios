"""
Capa Silver: Validación de datos con asserts
"""
import pandas as pd

def validate_dataframe(df, nombre_datos):
    print(f"\n🔍 Validando {nombre_datos}...")

    # Validación 1: que no sea None ni esté vacío
    assert df is not None, f"❌ {nombre_datos}: DataFrame es None"
    assert not df.empty, f"❌ {nombre_datos}: DataFrame está vacío"
    print(f"✅ Registros encontrados: {len(df)}")

    # Validación 2: nulos por columna
    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]
    if not nulos.empty:
        print(f"⚠️ Columnas con nulos:\n{nulos}")
    else:
        print("✅ Sin valores nulos")

    # Validación 3: valores negativos en columnas numéricas
    for col in df.select_dtypes(include=['number']).columns:
        if (df[col] < 0).any():
            print(f"⚠️ '{col}' tiene valores negativos")
        else:
            print(f"✅ '{col}' sin negativos")

    # Validación 4: duplicados
    dupes = df.duplicated().sum()
    assert dupes == 0, f"❌ {nombre_datos}: {dupes} filas duplicadas encontradas"
    print("✅ Sin duplicados")

    # Validación 5: columnas mínimas esperadas
    columnas_esperadas = ['cantidad', 'precio_unitario']
    for col in columnas_esperadas:
        assert col in df.columns, f"❌ Columna requerida ausente: '{col}'"
    print("✅ Columnas requeridas presentes")

    print(f"✅ Validación de {nombre_datos} completada\n")
    return True

def validate_cepal(df, nombre_datos="CEPALSTAT"):
    print(f"\n🔍 Validando datos de {nombre_datos}...")

    # Validación: que la API no haya devuelto vacío
    assert df is not None, "❌ CEPALSTAT: respuesta None — la API puede haber fallado"
    assert not df.empty, "❌ CEPALSTAT: sin datos — verificar conexión o parámetros"
    print(f"✅ CEPALSTAT: {len(df)} registros recibidos")

    # Validación: columna de valor numérico presente
    assert 'value' in df.columns or 'valor' in df.columns, \
        "❌ CEPALSTAT: no se encontró columna 'value' o 'valor'"
    print("✅ Columna de valor presente")

    # Validación: no todos los valores son nulos
    col_valor = 'value' if 'value' in df.columns else 'valor'
    assert df[col_valor].notna().sum() > 0, \
        "❌ CEPALSTAT: todos los valores son nulos — datos inconsistentes"
    print("✅ Valores CEPALSTAT no están todos vacíos")

    print(f"✅ Validación CEPALSTAT completada\n")
    return True

if __name__ == "__main__":
    df = pd.read_csv("data/silver/ventas_clean.csv")
    validate_dataframe(df, "Ventas")