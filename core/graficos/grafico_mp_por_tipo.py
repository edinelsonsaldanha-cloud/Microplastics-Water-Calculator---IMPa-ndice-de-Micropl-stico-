import json
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib
matplotlib.use("QtAgg")


def grafico_mp_por_tipo(pasta_projeto):
    caminho = os.path.join(
        pasta_projeto, "dados", "impa_mp_resultados.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:
        r = json.load(f)

    dados = r["MP_por_tipo_por_ponto"]

    pontos = list(dados.keys())
    tipos = sorted(
        {t for p in dados.values() for t in p.keys()}
    )

    acumulado = {t: [] for t in tipos}

    for ponto in pontos:
        for tipo in tipos:
            acumulado[tipo].append(dados[ponto].get(tipo, 0.0))

    base = [0] * len(pontos)

    plt.figure(figsize=(8, 5))

    for tipo in tipos:
        plt.bar(pontos, acumulado[tipo], bottom=base, label=tipo)
        base = [
            base[i] + acumulado[tipo][i]
            for i in range(len(base))
        ]

    plt.ylabel("MP tradicional (itens/L)")
    plt.xlabel("Ponto amostral")
    plt.title("MP tradicional por tipo (empilhado)")
    plt.legend()
    plt.tight_layout()
    plt.show()
