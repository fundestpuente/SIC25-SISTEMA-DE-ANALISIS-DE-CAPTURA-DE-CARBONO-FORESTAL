import streamlit as st
import pandas as pd
import os

if not os.path.exists("data"):
    os.makedirs("data")

st.title("📂 Subir o Reemplazar Datos (CSV o Excel)")

st.info("Sube un archivo **CSV** o **Excel (.xlsx)** con las siguientes columnas:")
st.code("""
Site, Parcel, Specie, Tree_Height_(cm), Circumference_(cm), DBH_(cm),
Wood_density_(g_cm^-3), AGB_(g), Carbon_conv_Factor_1, Carbon_conv_Factor_2,
Carbon_est_1_(kg), Carbon_est_2_(kg)
""")

existing_files = [f for f in os.listdir("data") if f.endswith((".csv", ".xlsx"))]
if existing_files:
    st.subheader("📁 Archivos actuales en el sistema:")
    selected_file = st.selectbox("Selecciona un archivo existente:", existing_files)
    
    if st.button("🗑️ Eliminar archivo seleccionado"):
        os.remove(os.path.join("data", selected_file))
        st.success(f"Archivo '{selected_file}' eliminado correctamente.")
        st.experimental_rerun()  

st.divider()

uploaded_file = st.file_uploader("Selecciona un nuevo archivo", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            print(df)

        st.success(f"✅ Archivo '{uploaded_file.name}' cargado correctamente")
        st.subheader("Vista previa:")
        st.dataframe(df.head())

        save_path = os.path.join("data", uploaded_file.name)
        df.to_csv(save_path.replace(".xlsx", ".csv"), index=False)
        st.success(f"Archivo guardado en: `{save_path.replace('.xlsx', '.csv')}`")

        if "df" in st.session_state:
            del st.session_state["df"]

        st.session_state["df"] = df

    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
