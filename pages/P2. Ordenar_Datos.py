import streamlit as st
import pandas as pd
import os
import numpy as np

st.title("🔢 Ordenar Datos")

if "df" in st.session_state:
    df = st.session_state["df"]
    st.success("Usando datos del archivo cargado recientemente.")
else:
    files = [f for f in os.listdir("data") if f.endswith((".csv", ".xlsx"))]
    if not files:
        st.warning("⚠️ No hay archivos cargados aún. Ve a 'Subir Datos'.")
        st.stop()
    selected_file = st.selectbox("Selecciona un archivo:", files)
    path = os.path.join("data", selected_file)
    df = pd.read_csv(path) if selected_file.endswith(".csv") else pd.read_excel(path)

def ordenar_datos(df):
    # para filtrar valores nulos principales
    df = df[(df['Base_angle'] != 0) & (df['Crown_angle'] != 0)
            & (df['Base_angle'] != '-') & (df['Crown_angle'] != '-')]

    df = df.dropna(subset=['Base_angle', 'Crown_angle'])
    df['Base_angle'] = pd.to_numeric(df['Base_angle'], errors='coerce')
    df['Crown_angle'] = pd.to_numeric(df['Crown_angle'], errors='coerce')
    df['Tree_Height'] = (((np.tan(np.radians(df['Base_angle']))) * 8) + (
                (np.tan(np.radians(df['Crown_angle']))) * 8)) * 100
    df['DBH_(cm)'] = df['Circumference_(cm)'] / np.pi
    df['AGB_(cm)'] = 0.0776 * ((df['Wood_density_(g_cm^-3)']
                                * (df['DBH_(cm)'] ** 2) *
                                df['Tree_Height']) ** 0.94)

    df['Carbon_Conv_Factor1'] = df['Circumference_(cm)'].apply(lambda x: 0.5 if x > 6 else 0)
    df['Carbon_Conv_Factor2'] = df['Circumference_(cm)'].apply(lambda x: 0.474 if x > 6 else 0)
    df['Carbon_est_1_kg'] = (df['AGB_(cm)'] * df['Carbon_Conv_Factor1']) / 1000
    df['Carbon_est_2_kg'] = (df['AGB_(cm)'] * df['Carbon_Conv_Factor2']) / 1000
    df["Carbon_prom"] = df[["Carbon_est_1_kg", "Carbon_est_2_kg"]].mean(axis=1)

    return df


non_null_counts = df.notnull().sum(axis=1)
possible_header_index = non_null_counts.idxmax()
df = ordenar_datos(df)
"""Así se ve el dataframe tras el ordenamiento de los datos"""
st.dataframe(df)

if "df" in st.session_state:
    del st.session_state["df"]

st.session_state["df"] = df

