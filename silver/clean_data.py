"""
Capa Silver: Limpieza y normalización
"""
import pandas as pd

def clean_dataframe(df):
    if df is None or df.empty:
        return None
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()
    df_clean = df_clean.dropna(axis=1, how="all")
    df_clean.columns = df_clean.columns.str.lower().str.replace(" ", "_")
    for col in df_clean.select_dtypes(include=["object"]).columns:
        df_clean[col] = df_clean[col].str.strip().str.upper()
    for col in df_clean.columns:
        if 'fecha' in col or 'date' in col:
            try:
                df_clean[col] = pd.to_datetime(df_clean[col])
            except:
                pass
    print(f"✅ Limpieza: {len(df_clean)} registros")
    return df_clean

def save_silver(df, filename):
    if df is not None:
        df.to_csv(f"data/silver/{filename}.csv", index=False)
        print(f"✅ Guardado: data/silver/{filename}.csv")

if __name__ == "__main__":
    df = pd.read_csv("data/bronze/datos_empresa.csv")
    df_clean = clean_dataframe(df)
    save_silver(df_clean, "datos_empresa_clean")