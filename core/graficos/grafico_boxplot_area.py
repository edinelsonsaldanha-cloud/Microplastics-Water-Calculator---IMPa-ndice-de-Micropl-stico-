import os
import json
import numpy as np
import matplotlib.pyplot as plt


def grafico_boxplot_area_microplasticos(pasta_projeto):
    """
    Boxplot das áreas dos microplásticos (µm²),
    agrupado por ponto amostral.
    """

    caminho_micro = os.path.join(
        pasta_projeto, "dados", "microplasticos.json"
    )

    if not os.path.exists(caminho_micro):
        raise FileNotFoundError(
            "Arquivo microplasticos.json não encontrado."
        )

    with open(caminho_micro, "r", encoding="utf-8") as f:
        microplasticos = json.load(f)

    if len(microplasticos) == 0:
        raise ValueError("Nenhum microplástico registrado.")

    # ===============================
    # Organizar áreas por ponto
    # ===============================
    dados_por_ponto = {}

    for mp in microplasticos:
        area = mp.get("area_um2")
        ponto = mp.get("ponto")

        if area is None:
            continue

        dados_por_ponto.setdefault(ponto, []).append(area)

    if not dados_por_ponto:
        raise ValueError(
            "Nenhum microplástico com área calculada."
        )

    pontos = sorted(dados_por_ponto.keys())
    valores = [dados_por_ponto[p] for p in pontos]

    # ===============================
    # Gráfico
    # ===============================
    plt.figure(figsize=(10, 6))
    plt.boxplot(valores, labels=pontos, showfliers=True)

    plt.ylabel("Área dos microplásticos (µm²)")
    plt.xlabel("Pontos Amostrais")
    plt.title("Boxplot das Áreas dos Microplásticos por Ponto")

    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
