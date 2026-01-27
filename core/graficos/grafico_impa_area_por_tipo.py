import os
import json
import matplotlib.pyplot as plt
import numpy as np


def grafico_impa_area_por_tipo(pasta_projeto):
    caminho = os.path.join(
        pasta_projeto, "dados", "impa_area_resultados.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:
        r = json.load(f)

    dados = r["IMPa_area_por_tipo_por_ponto"]

    pontos = list(dados.keys())
    tipos = sorted({
        t for p in dados.values() for t in p.keys()
    })

    valores = {
        tipo: [dados[p].get(tipo, 0) for p in pontos]
        for tipo in tipos
    }

    bottom = np.zeros(len(pontos))

    plt.figure(figsize=(9, 5))
    for tipo in tipos:
        plt.bar(pontos, valores[tipo], bottom=bottom, label=tipo)
        bottom += np.array(valores[tipo])

    plt.ylabel("IMPa–Área (µm²/L)")
    plt.xlabel("Ponto amostral")
    plt.title("Contribuição morfológica do IMPa–Área")
    plt.legend()
    plt.tight_layout()
    plt.show()
