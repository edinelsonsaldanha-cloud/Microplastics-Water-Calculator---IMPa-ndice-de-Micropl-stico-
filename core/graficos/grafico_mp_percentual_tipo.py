import json
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib
matplotlib.use("QtAgg")


def grafico_mp_percentual_por_tipo(pasta_projeto):
    caminho = os.path.join(
        pasta_projeto, "dados", "impa_mp_resultados.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:
        r = json.load(f)

    dados = r["MP_por_tipo_por_ponto"]

    soma_tipo = defaultdict(float)

    for ponto in dados.values():
        for tipo, valor in ponto.items():
            soma_tipo[tipo] += valor

    total = sum(soma_tipo.values())
    tipos = list(soma_tipo.keys())
    percentuais = [(v / total) * 100 for v in soma_tipo.values()]

    plt.figure(figsize=(6, 6))
    plt.pie(
        percentuais,
        labels=tipos,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Distribuição percentual – MP tradicional")
    plt.tight_layout()
    plt.show()
