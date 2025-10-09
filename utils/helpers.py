import pandas as pd
import os

def load_data(filename):
    """Carga un archivo CSV o Excel desde la carpeta data"""
    path = os.path.join("data", filename)
    if not os.path.exists(path):
        return None

    if filename.endswith(".csv"):
        return pd.read_csv(path)
    elif filename.endswith(".xlsx"):
        return pd.read_excel(path, engine="openpyxl")
    else:
        raise ValueError("Formato no soportado.")
