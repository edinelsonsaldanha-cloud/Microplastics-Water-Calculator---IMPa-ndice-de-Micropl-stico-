import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def grafico_distribuicao_comprimentos(pasta_projeto):
    """
    Gera gráfico de distribuição dos comprimentos dos microplásticos.
    """

    caminho_mp = os.path.join(
        pasta_projeto, "dados", "microplasticos.json"
    )

    if not os.path.exists(caminho_mp):
        raise FileNotFoundError(
            "Arquivo microplasticos.json não encontrado."
        )

    with open(caminho_mp, "r", encoding="utf-8") as f:
        microplasticos = json.load(f)

    if len(microplasticos) == 0:
        raise ValueError("Nenhum microplástico registrado.")

    # -------------------------------
    # DataFrame
    # -------------------------------
    df = pd.DataFrame(microplasticos)

    comprimentos = df["comprimento_um"]

    # -------------------------------
    # Gráfico
    # -------------------------------
    plt.figure(figsize=(9, 5))

    sns.histplot(
        comprimentos,
        bins=20,
        kde=True
    )

    plt.xlabel("Comprimento dos microplásticos (µm)")
    plt.ylabel("Frequência")
    plt.title("Distribuição dos Comprimentos dos Microplásticos")

    plt.tight_layout()
    plt.show()
