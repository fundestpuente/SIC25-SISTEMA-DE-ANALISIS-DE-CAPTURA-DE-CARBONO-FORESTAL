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

plt.show()
