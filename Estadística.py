import numpy as np
import pandas as pd

# ==================== Estadística descriptiva ====================

def estadisticas_descriptivas(df, columna):
    """Calcula estadísticas descriptivas básicas para la columna deseada"""
    datos = df[columna.lower()].dropna()
    
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
# ==================== ÍNDICES DE DIVERSIDAD ====================
"pi es la proporción del numero de una especie en el total de individuos (n/N) "
def indice_shannon(df):
    """Calcula el índice de Shannon: H' = -Σ(pi * ln(pi))"""
    conteo = df['species'].value_counts()
    total = conteo.sum()
    proporciones = conteo / total 
    shannon = np.sum(proporciones * np.log(proporciones)) * (-1)
    
    return {
        'shannon': shannon,
        'num_especies': len(conteo),
        'num_individuos': int(total),
        'equitatividad': shannon / np.log(len(conteo)) if len(conteo) > 1 else 1.0
    }

def indice_simpson(df):
    """Calcula el índice de Simpson: D = Σ(pi²)"""
    conteo = df['species'].value_counts()
    total = conteo.sum()
    proporciones = conteo / total 
    simpson_D = np.sum(proporciones ** 2)
    
    return {
        'simpson_D': simpson_D, #contradictorio par gente sin conocimiento técnico
        'simpson_inverso': 1 / simpson_D, #Es más entendible (mayor valor "es mejor")
        'simpson_diversidad': 1 - simpson_D 
        }
# ==================== Análisis de densidad de Carbono ====================
def densidad_carbono(df, area_ha=1.0):
    """Calcula densidades de carbono y biomasa por hectárea"""
    
    carbono_total = df['captura_carbono'].sum()
    agb_total = df['agb'].sum()
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

# ==================== Análisis por Sitio ====================
def estadistica_sitio(df, funcion):
    """Aplica la función solicitada a cada sitio registrado"""
    resultados = {}
    
    for sitio in df['site'].unique():
        df_sitio = df[df['site'] == sitio]
        resultados[sitio] = funcion(df_sitio)
    
    return resultados
    
