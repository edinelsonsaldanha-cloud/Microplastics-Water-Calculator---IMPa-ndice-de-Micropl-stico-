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
    plt.ylabel("IMPa–Área (µm²/L)")
    plt.xlabel("Ponto amostral")
    plt.title("IMPa–Área por ponto")
    plt.tight_layout()
    plt.show()
