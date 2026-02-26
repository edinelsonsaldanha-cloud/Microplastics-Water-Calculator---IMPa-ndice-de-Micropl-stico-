import json
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use("QtAgg")


def grafico_matriz_mp(pasta_projeto):
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

    matriz = np.zeros((len(tipos), len(pontos)))

    for j, ponto in enumerate(pontos):
        for i, tipo in enumerate(tipos):
            matriz[i, j] = dados[ponto].get(tipo, 0.0)

    plt.figure(figsize=(8, 5))
    plt.imshow(matriz, aspect="auto")
    plt.colorbar(label="Count-Based Microplastic Concentration (MP) (Items/L)")
    plt.xticks(range(len(pontos)), pontos)
    plt.yticks(range(len(tipos)), tipos)
    plt.xlabel("Sampling Unit")
    plt.ylabel("Morphological Category")
    plt.title("Count-Based Microplastic Concentration Matrix (MP) (Sampling Unit × Morphological Category)")
    plt.tight_layout()
    plt.show()
