import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use("QtAgg")


def grafico_impa_percentual_por_tipo(pasta_projeto):
    """
    Gera gráfico de barras empilhadas (%) do IMPₐ por tipo
    para cada ponto amostral.
    """

    caminho_resultados = os.path.join(
        pasta_projeto, "dados", "impa_mp_resultados.json"
    )

    if not os.path.exists(caminho_resultados):
        raise FileNotFoundError(
            "Arquivo impa_mp_resultados.json não encontrado."
        )

    with open(caminho_resultados, "r", encoding="utf-8") as f:
        r = json.load(f)

    impa_tipo = r["IMPa_por_tipo_por_ponto"]

    # ===============================
    # Montar DataFrame
    # ===============================
    df = pd.DataFrame(impa_tipo).T.fillna(0)

    # Converter para percentual
    df_percentual = df.div(df.sum(axis=1), axis=0) * 100

    # ===============================
    # Plot
    # ===============================
    fig, ax = plt.subplots(figsize=(10, 6))

    df_percentual.plot(
        kind="bar",
        stacked=True,
        ax=ax,
        colormap="tab20"
    )

    ax.set_ylabel("IMPa-L (%)")
    ax.set_xlabel("Sampling Unit")
    ax.set_title("Percentage Contribution to the Length-Based Microplastic Index (IMPa-L) by Morphological Category")

    ax.legend(
        title="Tipo",
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )

    plt.tight_layout()

    # ===============================
    # Salvar figura
    # ===============================
    pasta_saida = os.path.join(pasta_projeto, "resultados")
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_fig = os.path.join(
        pasta_saida,
        "grafico_impa_percentual_por_tipo.png"
    )

    plt.savefig(caminho_fig, dpi=300)
    plt.show()
