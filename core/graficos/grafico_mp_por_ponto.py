import json
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("QtAgg")


def grafico_mp_por_ponto(pasta_projeto):
    caminho = os.path.join(
        pasta_projeto, "dados", "impa_mp_resultados.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:
        r = json.load(f)

    pontos = list(r["MP_por_ponto"].keys())
    valores = list(r["MP_por_ponto"].values())

    plt.figure(figsize=(7, 4))
    plt.bar(pontos, valores)
    plt.ylabel("Count-Based Microplastic Concentration (MP) (Items/L)")
    plt.xlabel("Sampling Unit")
    plt.title("Count-Based Microplastic Concentration (MP) per Sampling Unit")
    plt.tight_layout()
    plt.show()
