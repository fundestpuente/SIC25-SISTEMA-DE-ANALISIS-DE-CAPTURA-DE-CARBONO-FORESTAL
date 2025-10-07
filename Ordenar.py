import pandas as pd
import math
import numpy as np

def ordenar_datos(df):
    arboles = []
    for especie in df['Specie'].unique(): #tal vez buscar a mano si son arboles y a partir de eso calcular la densidad
        if pd.notnull(especie): #o solo aceptar datos si tienen wood density, no se va a cambiar esto hasta que encuentre api
            # peor de los casos, el wood density lo calcula el usuario
            arboles.append(especie)
    print(arboles)
    df = df[(df['Base_angle'] != 0 ) & (df['Crown_angle'] != 0  )
             & (df['Base_angle'] != '-') & (df['Crown_angle'] != '-')]

    print(df)
    print(df.head())
    df = df.dropna(subset=['Base_angle', 'Crown_angle'])
    df['Base_angle'] = pd.to_numeric(df['Base_angle'], errors='coerce')
    df['Crown_angle'] = pd.to_numeric(df['Crown_angle'], errors='coerce')

   
    df['Wood_density_(g/cm3)'] = 0.59 #valor de ejemplo
    df['Tree_Height'] = (((np.tan(np.radians(df['Base_angle'])))*8) + ((np.tan(np.radians(df['Crown_angle'])))*8))*100
    df['DBH_(cm)']= df['Circumference_(cm)'] / np.pi
    df['AGB_(cm)'] = 0.0776*((df['Wood_density_(g/cm3)']
                              *(df['DBH_(cm)']**2)*
                              df['Tree_Height'])**0.94)
    
    df['Carbon_Conv_Factor1'] = df['Circumference_(cm)'].apply(lambda x: 0.5 if x > 6 else 0)
    df['Carbon_Conv_Factor2'] = df['Circumference_(cm)'].apply(lambda x: 0.474 if x > 6 else 0)
    df['Carbon_est_1_kg']= (df['AGB_(cm)']*df['Carbon_Conv_Factor1'])/1000
    df['Carbon_est_2_kg']= (df['AGB_(cm)']*df['Carbon_Conv_Factor2'])/1000
    
    return df
    


df_raw = pd.read_excel(r"datos\Captura_Info.xlsx")
non_null_counts = df_raw.notnull().sum(axis=1)
possible_header_index = non_null_counts.idxmax()
df = pd.read_excel(r"datos\Captura_Info.xlsx", header=1)
df = ordenar_datos(df)
print(df['Tree_Height'])
print(df.tail(6))
    