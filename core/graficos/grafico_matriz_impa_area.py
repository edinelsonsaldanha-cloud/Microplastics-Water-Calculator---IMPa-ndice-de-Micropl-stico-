import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("QtAgg")


def grafico_matriz_impa_area(pasta_projeto):
    caminho = os.path.join(
        pasta_projeto, "dados", "impa_area_resultados.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:
        r = json.load(f)

    df = pd.DataFrame(r["IMPa_area_por_tipo_por_ponto"]).T

    plt.figure(figsize=(8, 6))
    plt.imshow(df, aspect="auto")
    plt.colorbar(label="IMPa–A (µm²/L)")
    plt.xticks(range(len(df.columns)), df.columns, rotation=45)
    plt.yticks(range(len(df.index)), df.index)
    plt.title("Matrix Representation of the Area-Based Microplastic Index (IMPa-A) (Sampling Unit × Morphological Category)")
    plt.tight_layout()
    plt.show()
