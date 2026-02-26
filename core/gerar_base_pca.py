import os
import json
import pandas as pd
from collections import defaultdict


def gerar_base_pca(pasta_projeto):
    """
    Gera automaticamente a base_pca.csv a partir dos resultados do IMPₐ.

    Cada linha representa um ponto amostral.
    Cada coluna representa uma variável numérica (IMPa e MP por tipo).
    """

    caminho_resultados = os.path.join(
        pasta_projeto, "dados", "impa_mp_resultados.json"
    )

    if not os.path.exists(caminho_resultados):
        raise FileNotFoundError(
            "Arquivo impa_mp_resultados.json não encontrado."
        )

    with open(caminho_resultados, "r", encoding="utf-8") as f:
        r = json.load(f)

    # ===============================
    # Estrutura auxiliar
    # ===============================
    linhas = []
    tipos = set()

    # Descobrir todos os tipos existentes
    for ponto, dados in r["IMPa_por_tipo_por_ponto"].items():
        tipos.update(dados.keys())

    tipos = sorted(tipos)

    # ===============================
    # Construção linha a linha
    # ===============================
    for ponto in r["IMPa_por_ponto"].keys():

        linha = {"ponto": ponto}

        # IMPa por tipo
        for tipo in tipos:
            linha[f"IMPa_{tipo}"] = (
                r["IMPa_por_tipo_por_ponto"]
                .get(ponto, {})
                .get(tipo, 0.0)
            )

        # MP por tipo
        for tipo in tipos:
            linha[f"MP_{tipo}"] = (
                r["MP_por_tipo_por_ponto"]
                .get(ponto, {})
                .get(tipo, 0.0)
            )

        linhas.append(linha)

    # ===============================
    # DataFrame final
    # ===============================
    df = pd.DataFrame(linhas)

    # Garantia de tipos numéricos
    for col in df.columns:
        if col != "ponto":
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # ===============================
    # Salvar CSV
    # ===============================
    caminho_saida = os.path.join(
        pasta_projeto, "dados", "base_pca.csv"
    )

    df.to_csv(caminho_saida, index=False, encoding="utf-8")

    return df

