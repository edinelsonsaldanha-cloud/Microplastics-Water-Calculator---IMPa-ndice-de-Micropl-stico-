import json
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib
matplotlib.use("QtAgg")


def grafico_impa_por_tipo(pasta_projeto):
    caminho = os.path.join(
        pasta_projeto, "dados", "impa_mp_resultados.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:
        r = json.load(f)

    dados = r["IMPa_por_tipo_por_ponto"]

    pontos = list(dados.keys())
    tipos = set()

    for p in dados.values():
        tipos.update(p.keys())

    tipos = sorted(tipos)

    valores = defaultdict(list)
    for tipo in tipos:
        for ponto in pontos:
            valores[tipo].append(dados[ponto].get(tipo, 0))

    plt.figure(figsize=(8, 5))

    base = [0] * len(pontos)
    for tipo in tipos:
        plt.bar(
            pontos,
            valores[tipo],
            bottom=base,
            label=tipo
        )
        base = [
            base[i] + valores[tipo][i]
            for i in range(len(base))
        ]

    plt.ylabel("IMPa-L (µm/L)")
    plt.xlabel("Sampling Unit")
    plt.title("Morphological Contribution to the Length-Based Microplastic Index (IMPa-L)")
    plt.legend(title="Morphological Category")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
