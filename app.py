import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Gestor de Datos Forestales",
    page_icon="🌲",
    layout="wide"
)

st.title("🌳 Plataforma de Análisis de Datos Forestales")
st.write("""
Bienvenido al sistema de análisis de datos forestales.
Usa el menú lateral para acceder a las siguientes funciones:
- 📂 Subir datos  
- 🔢 Ordenar datos  
- 📊 Ver estadísticas  
- 📈 Visualizar gráficos

Por favor, revisar las opciones en ese orden para evitar que el código se caiga.
""")
