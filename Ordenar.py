import pandas as pd
import math

def ordenar_datos(df):
    arboles = []
    for especie in df['Specie'].unique(): #tal vez buscar a mano si son arboles y a partir de eso calcular la densidad
        if pd.notnull(especie): #o solo aceptar datos si tienen wood density, no se va a cambiar esto hasta que encuentre api
            # peor de los casos, el wood density lo calcula el usuario
            arboles.append(especie)
    print(arboles)
    df.dropna(thresh=3)
    print(df.head())
    #df['Wood_density_(g/cm3)'] = 
    df['Tree_Height'] = float((math.tan(math.radians(df['Base_Angle'])*8) + math.tan(math.radians(df['Crown_Angle'])*8))*100)
    df['DBH_(cm)']= float(df['Circumference_(cm)'] / math.pi)
    #df['AGB_(cm)'] = float(0.0776*((df['Wood_density_(g/cm3)']*(df['DBH_(cm)']^2)*df['Tree_Height'])^0.94))
    