import streamlit as st
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

st.title("📈 Visualización de Datos")

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
def grafico_riqueza(ax):
    bosques = set(df["Site"])
    especies_por_bosque = {}
    for bosque in bosques:
        especies_unicas = set(df[df["Site"] == bosque]["Specie"])
        especies_por_bosque[bosque] = len(especies_unicas)

    colores = cm.viridis(np.linspace(0, 1, len(especies_por_bosque.keys())))
    ax.bar(especies_por_bosque.keys(), especies_por_bosque.values(), color=colores)
    ax.set_title("Riqueza de especies vegetales por bosque")
    plt.show()

def grafico_top9(ax):
    total_carbon_especies = df.groupby("Specie").agg(Total=("Carbon_prom", "sum"))
    total_carbon_especies.sort_values("Total", ascending=False, inplace=True)

    colores = cm.viridis(np.linspace(0, 1, 9))
    ax.bar(total_carbon_especies.index[0:9], total_carbon_especies["Total"].head(9), color=colores)
    ax.set_xticklabels(total_carbon_especies.index[0:9], rotation=45, ha='right', fontsize=9)
    ax.set_title("Top 9 especies que más capturan carbono en total")
    plt.show()

def grafico_altura_carbono(ax):
    bosques = set(df["Site"])
    for bosque in bosques:
        carbonos = list(df[df["Site"] == bosque]["Carbon_prom"])
        alturas = list(df[df["Site"] == bosque]["Tree_Height"])
        ax.scatter(alturas, carbonos, label=bosque)

        m, c = np.polyfit(alturas, carbonos, 1)
        line_y = m * np.array(alturas) + c
        ax.plot(alturas, line_y, linestyle='--')

    ax.set_title("Relación de altura y carbono capturado por bosque")
    ax.set_xlabel("Altura (cm)")
    ax.set_ylabel("Carbono estimado (kg)")
    ax.legend()
    plt.show()

def grafico_pie_carbono(ax):
    fig = ax.figure
    fig.clf()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    # Carbono por parcela
    parcelas = set(df["Parcel"])
    total_por_parcela = {}

    def mostrar_parcela(val):
        a = np.round(val / 100.0 * sum(total_por_parcela.values()), 0)
        return f"{a}\n{val:.2f}%"

    for parcela in parcelas:
        total = df[df["Parcel"] == parcela]["Carbon_prom"].sum()
        total_por_parcela[parcela] = total

    ax1.pie(total_por_parcela.values(),
            labels=[f"Parcela {p}" for p in total_por_parcela.keys()],
            autopct=mostrar_parcela)
    ax1.set_title("Carbono total por parcela")
    ax1.axis("equal")
    ax1.axis("off")

    # Carbono por bosque
    bosques = set(df["Site"])
    total_por_bosque = {}

    def mostrar_bosque(val):
        a = np.round(val / 100.0 * sum(total_por_bosque.values()), 0)
        return f"{a}\n{val:.2f}%"

    for bosque in bosques:
        total = df[df["Site"] == bosque]["Carbon_prom"].sum()
        total_por_bosque[bosque] = total

    ax2.pie(total_por_bosque.values(),
            labels=total_por_bosque.keys(),
            autopct=mostrar_bosque)
    ax2.set_title("Carbono total por bosque")
    ax2.axis("equal")
    ax2.axis("off")

    fig.subplots_adjust(wspace=1)
    plt.show()

def grafico_por_especie(ax):
    carbono = df.groupby(["Site", "Specie"])["Carbon_prom"].sum().unstack(fill_value=0)

    carbono = carbono.loc[:, carbono.sum() != 0]

    carbono.plot(kind="bar", stacked=True, ax=ax)

    ax.set_title("Carbono total capturado por especie en cada bosque", loc="center")
    ax.set_ylabel("Carbono total")
    ax.set_xlabel("Bosque")
    ax.set_xticklabels(labels=carbono.index, rotation=45, ha='right', fontsize=9)

    ax.legend(title="Especies", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.figure.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()

def grafico_carbono_abundancia(ax):
    carbono_por_especie = df.groupby("Specie")["Carbon_prom"].sum()

    abundancia_por_especie = df.groupby("Specie")["Specie"].count()

    carbono_pct = 100 * carbono_por_especie / carbono_por_especie.sum()
    abundancia_pct = 100 * abundancia_por_especie / abundancia_por_especie.sum()

    data = (
        pd.DataFrame({
            "Carbono": carbono_pct,
            "Abundancia": abundancia_pct
        })
        .reset_index()
    )

    data = data[data["Carbono"] > 0]

    especies = data["Specie"]
    carbono = data["Carbono"]
    abundancia = data["Abundancia"]

    x = np.arange(len(especies))
    width = 0.35

    ax.bar(x - width / 2, carbono, width, label="Carbono Capturado (%)", color="salmon")
    ax.bar(x + width / 2, abundancia, width, label="Abundancia (%)", color="turquoise")

    ax.set_xlabel("Especie")
    ax.set_ylabel("Porcentaje (%)")
    ax.set_title("Comparación de Carbono Capturado y Abundancia por Especie")
    ax.set_xticks(x)
    ax.set_xticklabels(especies, rotation=45, ha="right")
    ax.legend()

st.subheader("Carbono total capturado por especie en cada bosque")
fig, ax = plt.subplots(figsize=(8,5))
grafico_por_especie(ax)
st.pyplot(fig)

st.subheader("Riqueza de especies vegetales por bosque")
fig, ax = plt.subplots(figsize=(6,4))
grafico_riqueza(ax)
st.pyplot(fig)

st.subheader("Top 9 especies que más capturan carbono en total")
fig, ax = plt.subplots(figsize=(7,5))
grafico_top9(ax)
st.pyplot(fig)

st.subheader("Relación de altura y carbono capturado por bosque")
fig, ax = plt.subplots(figsize=(7,5))
grafico_altura_carbono(ax)
st.pyplot(fig)

st.subheader("Distribución de carbono por parcela y por bosque")
fig, ax = plt.subplots(figsize=(10,5))
grafico_pie_carbono(ax)
st.pyplot(fig)

st.subheader("Comparación de Carbono Capturado y Abundancia por Especie")
fig, ax = plt.subplots(figsize=(10,5))
grafico_carbono_abundancia(ax)
st.pyplot(fig)
