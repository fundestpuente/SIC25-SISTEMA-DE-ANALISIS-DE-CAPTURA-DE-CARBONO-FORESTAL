import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("../../../capturaC.csv", encoding="utf-8", sep=";")

fig, ax = plt.subplots(2, 2)

# Riqueza de especies por bosque
bosques = set(df["Site"])
especies_por_bosque = {}
for bosque in bosques:
    especies_unicas = set(df[ df["Site"] == bosque ]["Specie"])
    especies_por_bosque[bosque] = len(especies_unicas)

ax[0,0].bar(especies_por_bosque.keys(), especies_por_bosque.values())
ax[0,0].set_title("Riqueza de especies vegetales por bosque")

# Especies vegetales por bosque
especies_vegetales = {}

especies_unicas = set(df["Specie"])
for bosque in bosques:
    for especie in especies_unicas:
        conteo = df[(df["Site"] == bosque) & (df["Specie"] == especie)]["Specie"].count()
        if especie not in especies_vegetales:
            especies_vegetales[especie] = [conteo]
        else:
            especies_vegetales[especie].append(conteo)

bottom = np.zeros(len(bosques))
for conteo in especies_vegetales.values():
    ax[0,1].bar(list(bosques), conteo, bottom=bottom)
    bottom += np.array(conteo)

ax[0,1].legend(especies_vegetales.keys(), bbox_to_anchor=(1.05, 0), loc='lower left')

# Relación de altura y carbono
for bosque in bosques:
    carbonos = list(df[ df["Site"] == bosque ][["Carbon_est_1", "Carbon_est_2"]].mean(axis=1))
    alturas = list(df[ df["Site"] == bosque ]["Tree_Height"])
    ax[1,0].scatter(alturas, carbonos, label=bosque)

    m, c = np.polyfit(alturas, carbonos, 1)
    line_y = m * np.array(alturas) + c
    ax[1,0].plot(alturas, line_y, linestyle='--')

ax[1,0].set_title("Relación de altura y carbono por bosque")
ax[1,0].set_xlabel("Altura (cm)")
ax[1,0].set_ylabel("Carbono estimado (kg)")
ax[1,0].legend()

plt.show()
