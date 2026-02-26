import os
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("QtAgg")


def grafico_impa_area_por_ponto(pasta_projeto):
    caminho = os.path.join(
        pasta_projeto, "dados", "impa_area_resultados.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:
        r = json.load(f)

    pontos = list(r["IMPa_area_por_ponto"].keys())
    valores = list(r["IMPa_area_por_ponto"].values())

    plt.figure(figsize=(8, 5))
    plt.bar(pontos, valores)
    plt.ylabel("IMPa-A (µm²/L)")
    plt.xlabel("Sampling Unit")
    plt.title("Area-Based Microplastic Index (IMPa-A) per Sampling Unit")
    plt.tight_layout()
    plt.show()
