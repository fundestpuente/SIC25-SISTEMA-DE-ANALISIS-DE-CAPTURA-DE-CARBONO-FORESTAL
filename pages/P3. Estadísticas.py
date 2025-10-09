import streamlit as st
import pandas as pd
import numpy as np
import os

st.title("📊 Estadísticas Descriptivas y de Diversidad")

# ==================== Carga de datos ====================
if "df" in st.session_state:
    df = st.session_state["df"]
    st.success("Usando datos del archivo cargado recientemente.")
else:
    files = [f for f in os.listdir("data") if f.endswith((".csv", ".xlsx"))]
    if not files:
        st.warning("⚠️ No hay archivos cargados aún.")
        st.stop()
    selected_file = st.selectbox("Selecciona un archivo:", files)
    path = os.path.join("data", selected_file)
    df = pd.read_csv(path) if selected_file.endswith(".csv") else pd.read_excel(path)
    st.session_state["df"] = df

# ==================== Estadística descriptiva ====================
st.header("Estadísticas descriptivas")
columnas_numericas = df.select_dtypes(include=np.number).columns.tolist()
columna = st.selectbox("Selecciona la columna para estadística descriptiva:", columnas_numericas)

def estadisticas_descriptivas(df, columna):
    datos = df[columna].dropna()
    return {
        'n': len(datos),
        'media': datos.mean(),
        'mediana': datos.median(),
        'desv_std': datos.std(),
        'minimo': datos.min(),
        'maximo': datos.max(),
        'q1': datos.quantile(0.25),
        'q3': datos.quantile(0.75),
    }

desc = estadisticas_descriptivas(df, columna)
st.table(pd.DataFrame([desc]))

# ==================== Índices de diversidad ====================
st.header("Índices de diversidad")

# Shannon
def indice_shannon(df):
    conteo = df['Specie'].value_counts()
    total = conteo.sum()
    proporciones = conteo / total
    shannon = -np.sum(proporciones * np.log(proporciones))
    return {
        'shannon': shannon,
        'num_especies': len(conteo),
        'num_individuos': int(total),
        'equitatividad': shannon / np.log(len(conteo)) if len(conteo) > 1 else 1.0
    }

# Simpson
def indice_simpson(df):
    conteo = df['Specie'].value_counts()
    total = conteo.sum()
    proporciones = conteo / total
    simpson_D = np.sum(proporciones ** 2)
    return {
        'simpson_D': simpson_D,
        'simpson_inverso': 1 / simpson_D,
        'simpson_diversidad': 1 - simpson_D
    }

st.subheader("Índice de Shannon")
shannon_result = indice_shannon(df)
st.table(pd.DataFrame([shannon_result]))

st.subheader("Índice de Simpson")
simpson_result = indice_simpson(df)
st.table(pd.DataFrame([simpson_result]))

# ==================== Densidad de carbono ====================
st.header("Densidad de carbono y biomasa")

def densidad_carbono(df, area_ha=1.0):
    carbono_total = df['Carbon_prom'].sum()
    agb_total = df['AGB_(cm)'].sum()
    num_arboles = len(df)
    return {
        'carbono_total_ton': carbono_total,
        'carbono_por_ha_ton': carbono_total / area_ha,
        'agb_total_ton': agb_total,
        'agb_por_ha_ton': agb_total / area_ha,
        'arboles_totales': num_arboles,
        'arboles_por_ha': num_arboles / area_ha,
        'carbono_promedio_por_arbol_kg': (carbono_total * 1000 / num_arboles) if num_arboles > 0 else 0
    }

carbono_result = densidad_carbono(df)
st.table(pd.DataFrame([carbono_result]))

# ==================== Análisis por sitio ====================
st.header("Estadísticas por sitio")

def estadistica_sitio(df, funcion):
    resultados = {}
    for sitio in df['Site'].unique():
        df_sitio = df[df['Site'] == sitio]
        resultados[sitio] = funcion(df_sitio)
    return resultados

st.subheader("Índice de Shannon por sitio")
shannon_por_sitio = estadistica_sitio(df, indice_shannon)
st.write(pd.DataFrame(shannon_por_sitio).T)

st.subheader("Índice de Simpson por sitio")
simpson_por_sitio = estadistica_sitio(df, indice_simpson)
st.write(pd.DataFrame(simpson_por_sitio).T)

st.subheader("Densidad de carbono por sitio")
carbono_por_sitio = estadistica_sitio(df, densidad_carbono)
st.write(pd.DataFrame(carbono_por_sitio).T)
