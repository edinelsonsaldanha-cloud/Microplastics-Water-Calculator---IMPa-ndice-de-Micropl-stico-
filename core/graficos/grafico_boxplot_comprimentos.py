import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("QtAgg")

def grafico_boxplot_comprimentos(pasta_projeto):
    """
    Gera boxplot da distribuição dos comprimentos dos microplásticos (µm)
    por ponto amostral.
    """

    # ===============================
    # Caminho dos dados
    # ===============================
    caminho_mp = os.path.join(
        pasta_projeto, "dados", "microplasticos.json"
    )

    if not os.path.exists(caminho_mp):
        raise FileNotFoundError(
            "Arquivo microplasticos.json não encontrado."
        )

    with open(caminho_mp, "r", encoding="utf-8") as f:
        microplasticos = json.load(f)

    if not microplasticos:
        raise ValueError(
            "Nenhum microplástico cadastrado para gerar o boxplot."
        )

    # ===============================
    # Construir DataFrame
    # ===============================
    dados = []

    for mp in microplasticos:
        dados.append({
            "ponto": mp["ponto"],
            "comprimento_um": mp["comprimento_um"]
        })

    df = pd.DataFrame(dados)

    # ===============================
    # Garantia de ordenação dos pontos
    # ===============================
    pontos_ordem = sorted(df["ponto"].unique())
    dados_por_ponto = [
        df[df["ponto"] == p]["comprimento_um"].values
        for p in pontos_ordem
    ]

    # ===============================
    # Plot
    # ===============================
    plt.figure(figsize=(9, 5))

    plt.boxplot(
        dados_por_ponto,
        labels=pontos_ordem,
        patch_artist=True,
        medianprops=dict(color="orange", linewidth=2),
        boxprops=dict(facecolor="#1f77b4", alpha=0.6),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black")
    )

    plt.title("Distribuição dos Comprimentos dos Microplásticos por Ponto Amostral")
    plt.xlabel("Ponto Amostral")
    plt.ylabel("Comprimento dos microplásticos (µm)")
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()
