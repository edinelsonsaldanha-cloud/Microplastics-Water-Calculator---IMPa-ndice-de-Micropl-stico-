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
    plt.ylabel("MP tradicional (itens/L)")
    plt.xlabel("Ponto amostral")
    plt.title("MP tradicional por ponto")
    plt.tight_layout()
    plt.show()
