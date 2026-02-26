import os
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use("QtAgg")

def grafico_impa_area_percentual_por_tipo(pasta_projeto):
    caminho = os.path.join(
        pasta_projeto, "dados", "impa_area_resultados.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:
        r = json.load(f)

    dados = r["IMPa_area_por_tipo_por_ponto"]

    tipos = sorted({
        t for p in dados.values() for t in p.keys()
    })

    soma_tipo = {t: 0 for t in tipos}

    for p in dados.values():
        for t, v in p.items():
            soma_tipo[t] += v

    total = sum(soma_tipo.values())
    percentuais = [100 * soma_tipo[t] / total for t in tipos]

    plt.figure(figsize=(7, 5))
    plt.bar(tipos, percentuais)
    plt.ylabel("Contribution (%)")
    plt.title("Percentage Contribution to the Area-Based Microplastic Index (IMPa-A) by Morphological Category")
    plt.tight_layout()
    plt.show()
