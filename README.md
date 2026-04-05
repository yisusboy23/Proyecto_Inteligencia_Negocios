# Sistema de Inteligencia de Negocios - Supermercado Bolivia
Proyecto End-to-End de BI que integra datos internos con indicadores de CEPALSTAT, alineado al ODS 8/9.

## Arquitectura
- **Bronze:** Ingesta de datos desde SQL Server y API CEPALSTAT
- **Silver:** Limpieza y normalización con Pandas
- **Gold:** Modelo Estrella en SQL Server + KPIs
- **Dashboard:** Visualización interactiva en Streamlit

## Cómo ejecutar

### 1. Instalar dependencias
pip install -r requirements.txt

### 2. Configurar conexión
Editar `config.py` con los datos de tu servidor SQL Server.

### 3. Correr el pipeline
python bronze/ingesta.py
python silver/