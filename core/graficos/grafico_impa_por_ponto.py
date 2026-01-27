import json
import os
import matplotlib.pyplot as plt


def grafico_impa_por_ponto(pasta_projeto):
    caminho = os.path.join(
        pasta_projeto, "dados", "impa_mp_resultados.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:
        r = json.load(f)

    pontos = list(r["IMPa_por_ponto"].keys())
    valores = list(r["IMPa_por_ponto"].values())

    plt.figure(figsize=(8, 5))
    plt.bar(pontos, valores)
    plt.ylabel("IMPₐ (µm/L)")
    plt.xlabel("Ponto amostral")
    plt.title("IMPₐ por ponto amostral")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
