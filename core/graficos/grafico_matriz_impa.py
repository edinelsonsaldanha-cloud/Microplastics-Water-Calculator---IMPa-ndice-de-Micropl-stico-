import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use("QtAgg")


def grafico_matriz_impa(pasta_projeto):
    """
    Gera a matriz (heatmap) de IMPa (µm/L) por ponto amostral e tipo morfológico.
    """

    # ===============================
    # Caminho dos resultados
    # ===============================
    caminho_resultados = os.path.join(
        pasta_projeto, "dados", "impa_mp_resultados.json"
    )

    if not os.path.exists(caminho_resultados):
        raise FileNotFoundError(
            "Arquivo impa_mp_resultados.json não encontrado."
        )

    with open(caminho_resultados, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    impa_por_tipo = resultados["IMPa_por_tipo_por_ponto"]

    # ===============================
    # Construir DataFrame
    # ===============================
    df = pd.DataFrame(impa_por_tipo).T
    df = df.fillna(0)

    # Ordenação opcional
    df = df.sort_index()

    # ===============================
    # Plot
    # ===============================
    plt.figure(figsize=(9, 5))

    sns.heatmap(
        df,
        cmap="viridis",
        annot=True,
        fmt=".1f",
        linewidths=0.5,
        cbar_kws={"label": "IMPₐ (µm/L)"}
    )

    plt.title("Summary Matrix of the Length-Based Microplastic Index (IMPa-L) (µm/L) by Sampling Unit and Morphological Category")
    plt.xlabel("Morphological Category")
    plt.ylabel("Sampling Unit")

    plt.tight_layout()
    plt.show()
