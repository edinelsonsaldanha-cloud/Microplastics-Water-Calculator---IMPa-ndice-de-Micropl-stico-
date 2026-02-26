import json
import os
from collections import defaultdict


def calcular_impa_area(pasta_projeto):
    """
    Calcula o IMPa baseado em ÁREA (µm²/L)

    Retorna e salva:
    - IMPa_area_por_ponto
    - IMPa_area_por_tipo_por_ponto
    - IMPa_area_global
    """

    caminho_mp = os.path.join(
        pasta_projeto, "dados", "microplasticos.json"
    )
    caminho_pontos = os.path.join(
        pasta_projeto, "dados", "pontos_amostrais.json"
    )

    if not os.path.exists(caminho_mp):
        raise FileNotFoundError("Arquivo microplasticos.json não encontrado.")

    if not os.path.exists(caminho_pontos):
        raise FileNotFoundError("Arquivo pontos_amostrais.json não encontrado.")

    with open(caminho_mp, "r", encoding="utf-8") as f:
        microplasticos = json.load(f)

    with open(caminho_pontos, "r", encoding="utf-8") as f:
        pontos = json.load(f)

    # ===============================
    # Acumuladores
    # ===============================
    soma_area = defaultdict(float)  # µm² por ponto
    soma_area_tipo = defaultdict(lambda: defaultdict(float))  # µm² por ponto e tipo

    # ===============================
    # Acumular áreas
    # ===============================
    for mp in microplasticos:
        area = mp.get("area_um2")
        ponto = mp.get("ponto")
        tipo = mp.get("tipo")

        if area is None:
            continue

        soma_area[ponto] += area
        soma_area_tipo[ponto][tipo] += area

    # ===============================
    # Cálculo por ponto
    # ===============================
    IMPa_area_por_ponto = {}
    IMPa_area_por_tipo = {}

    for ponto, dados in pontos.items():
        V = dados["volume_L"]

        if V <= 0:
            raise ValueError(f"Volume inválido no ponto {ponto}")

        # Por ponto
        IMPa_area_por_ponto[ponto] = soma_area[ponto] / V

        # Por tipo dentro do ponto
        IMPa_area_por_tipo[ponto] = {}
        for tipo, area_tipo in soma_area_tipo[ponto].items():
            IMPa_area_por_tipo[ponto][tipo] = area_tipo / V

    # ===============================
    # Cálculo global
    # ===============================
    soma_area_total = sum(soma_area.values())
    soma_volume_total = sum(p["volume_L"] for p in pontos.values())

    if soma_volume_total <= 0:
        raise ValueError("Volume total inválido para cálculo global.")

    IMPa_area_global = soma_area_total / soma_volume_total

    # ===============================
    # Resultado consolidado
    # ===============================
    resultados_area = {
        "IMPa_area_por_ponto": IMPa_area_por_ponto,
        "IMPa_area_por_tipo_por_ponto": IMPa_area_por_tipo,
        "IMPa_area_global": IMPa_area_global
    }

    # ===============================
    # Salvar
    # ===============================
    caminho_saida = os.path.join(
        pasta_projeto, "dados", "impa_area_resultados.json"
    )

    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados_area, f, indent=4, ensure_ascii=False)

    return resultados_area

