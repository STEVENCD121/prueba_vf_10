
import pandas as pd
import streamlit as st

def cargar_datos(ruta_csv):
    try:
        df = pd.read_csv(ruta_csv, dtype=str)

        df["Lote"] = df["Lote"].astype(str).str.strip()
        df["Tipo de Hidrocarburo"] = df["Tipo de Hidrocarburo"].astype(str).str.strip()
        df["Año"] = df["Año"].astype(str).str.extract(r'(\d{4})')[0].astype(int)

        columnas_numericas = ['Reservas Probadas (P1)', 'Reservas Probables (P2)', 
                              'Reservas Posibles (P3)', 'Recursos Contingentes (2C)', 
                              'Recursos Prospectivos (2U)', 'Producción', 'Inversion', 'Regalia', 'Canon']
        for col in columnas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df

    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo {ruta_csv}.")
        return None
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None

def mostrar_inversion(df, lote, años=[2021, 2022, 2023, 2024, 2025]):
    fila_lote = []
    fila_pais = []
    fila_participacion = []

    for año in años:
        df_filtrado = df[(df["Año"] == año)]
        inversion_lote = df_filtrado[df_filtrado["Lote"] == lote]["Inversion"].sum()
        inversion_pais = df_filtrado["Inversion"].sum()
        fila_lote.append(round(inversion_lote, 2))
        fila_pais.append(round(inversion_pais, 2))
        participacion = (inversion_lote / inversion_pais * 100) if inversion_pais > 0 else 0
        fila_participacion.append(round(participacion, 2))

    if all(v == 0 for v in fila_lote):
        st.warning(f"No hay inversión registrada para el lote '{lote}' en los años consultados.")
        return None

    df_resultado = pd.DataFrame({
        "Clasificación": ["Lote", "País", "%Participación"],
    })
    for i, año in enumerate(años):
        df_resultado[str(año)] = [fila_lote[i], fila_pais[i], fila_participacion[i]]

    return df_resultado

def mostrar_regalias(df, lote, años=[2021, 2022, 2023, 2024, 2025]):
    fila_lote = []
    fila_pais = []
    fila_participacion = []

    for año in años:
        df_filtrado = df[(df["Año"] == año)]
        regalia_lote = df_filtrado[df_filtrado["Lote"] == lote]["Regalia"].sum()
        regalia_pais = df_filtrado["Regalia"].sum()
        fila_lote.append(round(regalia_lote, 2))
        fila_pais.append(round(regalia_pais, 2))
        participacion = (regalia_lote / regalia_pais * 100) if regalia_pais > 0 else 0
        fila_participacion.append(round(participacion, 2))

    if all(v == 0 for v in fila_lote):
        st.warning(f"No hay regalías registradas para el lote '{lote}' en los años consultados.")
        return None

    df_resultado = pd.DataFrame({
        "Clasificación": ["Lote", "País", "%Participación"],
    })
    for i, año in enumerate(años):
        df_resultado[str(año)] = [fila_lote[i], fila_pais[i], fila_participacion[i]]

    return df_resultado

def mostrar_canon(df, lote, años=[2021, 2022, 2023, 2024, 2025]):
    fila_lote = []
    fila_pais = []
    fila_participacion = []

    for año in años:
        df_filtrado = df[(df["Año"] == año)]
        canon_lote = df_filtrado[df_filtrado["Lote"] == lote]["Canon"].sum()
        canon_pais = df_filtrado["Canon"].sum()
        fila_lote.append(round(canon_lote, 2))
        fila_pais.append(round(canon_pais, 2))
        participacion = (canon_lote / canon_pais * 100) if canon_pais > 0 else 0
        fila_participacion.append(round(participacion, 2))

    if all(v == 0 for v in fila_lote):
        st.warning(f"No hay cánones registrados para el lote '{lote}' en los años consultados.")
        return None

    df_resultado = pd.DataFrame({
        "Clasificación": ["Lote", "País", "%Participación"],
    })
    for i, año in enumerate(años):
        df_resultado[str(año)] = [fila_lote[i], fila_pais[i], fila_participacion[i]]

    return df_resultado

def mostrar_reservas_recursos(df, lote, hidrocarburo, año=2023):
    columnas_volumen = {
        'Reservas Probadas (P1)': 'P1',
        'Reservas Probables (P2)': 'P2',
        'Reservas Posibles (P3)': 'P3',
        'Recursos Contingentes (2C)': '2C',
        'Recursos Prospectivos (2U)': '2U'
    }

    df_filtrado = df[(df["Año"] == año) & 
                     (df["Tipo de Hidrocarburo"] == hidrocarburo) & 
                     (df["Lote"] == lote)]
    
    filas, volumen_lote, volumen_pais = [], [], []

    for col, etiqueta in columnas_volumen.items():
        valor_lote = df_filtrado[col].sum()
        valor_pais = df[(df["Año"] == año) & (df["Tipo de Hidrocarburo"] == hidrocarburo)][col].sum()
        filas.append(etiqueta)
        volumen_lote.append(valor_lote)
        volumen_pais.append(valor_pais)

    if all(v == 0 for v in volumen_lote):
        st.warning(f"No se tienen reservas ni recursos para el lote '{lote}' - hidrocarburo '{hidrocarburo}' en el año {año}.")
        return None

    df_resultado = pd.DataFrame({
        "Clasificación": filas,
        "Volumen (Miles)": [round(v / 1000, 2) for v in volumen_lote],
        "País (Miles)": [round(v / 1000, 2) for v in volumen_pais]
    })

    df_resultado["%Participación"] = (df_resultado["Volumen (Miles)"] / df_resultado["País (Miles)"] * 100).round(2)
    st.write(f"### RESERVAS Y RECURSOS DE {hidrocarburo.upper()} - Lote: {lote} - Año: {año}")
    st.table(df_resultado)
    return df_resultado

def mostrar_produccion(df, lote, hidrocarburo, años=[2021, 2022, 2023, 2024, 2025]):
    fila_lote = []
    fila_pais = []
    fila_participacion = []

    for año in años:
        df_filtrado = df[(df["Año"] == año) & (df["Tipo de Hidrocarburo"] == hidrocarburo)]
        prod_lote = df_filtrado[df_filtrado["Lote"] == lote]["Producción"].sum()
        prod_pais = df_filtrado["Producción"].sum()
        fila_lote.append(round(prod_lote, 2))
        fila_pais.append(round(prod_pais, 2))
        participacion = (prod_lote / prod_pais * 100) if prod_pais > 0 else 0
        fila_participacion.append(round(participacion, 2))

    if all(v == 0 for v in fila_lote):
        st.warning(f"No hay producción registrada para el lote '{lote}' - hidrocarburo '{hidrocarburo}' en los años consultados.")
        return None

    df_resultado = pd.DataFrame({
        "Clasificación": ["Lote", "País", "%Participación"],
    })
    for i, año in enumerate(años):
        df_resultado[str(año)] = [fila_lote[i], fila_pais[i], fila_participacion[i]]

    st.write(f"### Producción Fiscalizada de {hidrocarburo.upper()} - Lote: {lote}")
    st.table(df_resultado)
    return df_resultado

# --- MAIN CON ORDEN MODIFICADO ---
def main():
    st.title("Análisis de Reservas, Recursos, Producción, Inversiones, Regalías y Cánones por Lote")

    ruta_csv = "Integrado.csv"
    df = cargar_datos(ruta_csv)
    if df is None:
        return

    lote = st.text_input("¿De qué Lote necesitas información?").strip()
    if lote == "":
        st.info("Por favor, ingresa un lote para continuar.")
        return

    hidrocarburos = ["Petróleo", "Gas", "LGN"]
    año = st.number_input("Selecciona el año para mostrar la información:", min_value=2021, max_value=2025, value=2023, step=1)

    # --- 1. RESERVAS Y RECURSOS ---
    st.subheader("Reservas y Recursos")
    for h in hidrocarburos:
        mostrar_reservas_recursos(df, lote, h, año)

    # --- 2. PRODUCCIÓN FISCALIZADA ---
    st.subheader("Producción Fiscalizada")
    for h in hidrocarburos:
        mostrar_produccion(df, lote, h, años=[2021, 2022, 2023, 2024, 2025])

    # --- 3. INVERSIÓN, REGALÍAS Y CANONES ---
    df_inversion = mostrar_inversion(df, lote)
    if df_inversion is not None:
        st.write("### Inversión por Lote y País")
        st.table(df_inversion)

    df_regalias = mostrar_regalias(df, lote)
    if df_regalias is not None:
        st.write("### Regalías por Lote y País")
        st.table(df_regalias)

    df_canon = mostrar_canon(df, lote)
    if df_canon is not None:
        st.write("### Cánones por Lote y País")
        st.table(df_canon)

if __name__ == "__main__":
    main()
