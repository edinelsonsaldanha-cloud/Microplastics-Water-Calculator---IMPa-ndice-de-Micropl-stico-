import json
import os
from collections import defaultdict


def calcular_impa_e_mp(pasta_projeto):
    """
    Calcula:
    - IMPa por ponto (µm/L)
    - IMPa global (µm/L)
    - IMPa por tipo por ponto (µm/L)

    - MP tradicional por ponto (itens/L)
    - MP tradicional global (itens/L)
    - MP tradicional por tipo por ponto (itens/L)
    """

    caminho_mp = os.path.join(pasta_projeto, "dados", "microplasticos.json")
    caminho_pontos = os.path.join(pasta_projeto, "dados", "pontos_amostrais.json")

    if not os.path.exists(caminho_mp):
        raise FileNotFoundError("Arquivo microplasticos.json não encontrado.")

    if not os.path.exists(caminho_pontos):
        raise FileNotFoundError("Arquivo pontos_amostrais.json não encontrado.")

    with open(caminho_mp, "r", encoding="utf-8") as f:
        microplasticos = json.load(f)

    with open(caminho_pontos, "r", encoding="utf-8") as f:
        pontos = json.load(f)

    # =====================================================
    # ACUMULADORES
    # =====================================================

    # Comprimento (IMPa)
    soma_comprimento = defaultdict(float)                 # µm por ponto
    soma_comprimento_tipo = defaultdict(lambda: defaultdict(float))

    # Contagem (MP tradicional)
    contagem_mp = defaultdict(int)                         # itens por ponto
    contagem_mp_tipo = defaultdict(lambda: defaultdict(int))

    # =====================================================
    # ACUMULAR MICROPLÁSTICOS
    # =====================================================
    for mp in microplasticos:
        ponto = mp["ponto"]
        tipo = mp["tipo"]

        # ----- IMPa (comprimento) -----
        comprimento = mp.get("comprimento_um")
        if comprimento is not None:
            soma_comprimento[ponto] += comprimento
            soma_comprimento_tipo[ponto][tipo] += comprimento

        # ----- MP tradicional (contagem) -----
        contagem_mp[ponto] += 1
        contagem_mp_tipo[ponto][tipo] += 1

    # =====================================================
    # IMPa POR PONTO (µm/L)
    # =====================================================
    IMPa_por_ponto = {}

    for ponto, dados in pontos.items():
        V = dados["volume_L"]
        if V <= 0:
            raise ValueError(f"Volume inválido no ponto {ponto}")

        IMPa_por_ponto[ponto] = soma_comprimento[ponto] / V

    # =====================================================
    # MP POR PONTO (itens/L)
    # =====================================================
    MP_por_ponto = {}

    for ponto, dados in pontos.items():
        V = dados["volume_L"]
        if V <= 0:
            raise ValueError(f"Volume inválido no ponto {ponto}")

        MP_por_ponto[ponto] = contagem_mp[ponto] / V

    # =====================================================
    # IMPa POR TIPO (POR PONTO) (µm/L)
    # =====================================================
    IMPa_por_tipo_por_ponto = {}

    for ponto, tipos in soma_comprimento_tipo.items():
        V = pontos[ponto]["volume_L"]
        IMPa_por_tipo_por_ponto[ponto] = {
            tipo: valor / V
            for tipo, valor in tipos.items()
        }

    # =====================================================
    # MP POR TIPO (POR PONTO) (itens/L)  🔹 NOVO 🔹
    # =====================================================
    MP_por_tipo_por_ponto = {}

    for ponto, tipos in contagem_mp_tipo.items():
        V = pontos[ponto]["volume_L"]
        MP_por_tipo_por_ponto[ponto] = {
            tipo: qtd / V
            for tipo, qtd in tipos.items()
        }

    # =====================================================
    # GLOBAIS
    # =====================================================
    soma_comprimento_total = sum(soma_comprimento.values())
    soma_itens_total = sum(contagem_mp.values())
    soma_volume_total = sum(p["volume_L"] for p in pontos.values())

    IMPa_global = soma_comprimento_total / soma_volume_total
    MP_global = soma_itens_total / soma_volume_total

    # =====================================================
    # RESULTADOS
    # =====================================================
    resultados = {
        "IMPa_por_ponto": IMPa_por_ponto,
        "IMPa_global": IMPa_global,
        "IMPa_por_tipo_por_ponto": IMPa_por_tipo_por_ponto,

        "MP_por_ponto": MP_por_ponto,
        "MP_global": MP_global,
        "MP_por_tipo_por_ponto": MP_por_tipo_por_ponto  # 🔹 NOVO 🔹
    }

    # =====================================================
    # SALVAR
    # =====================================================
    caminho_saida = os.path.join(
        pasta_projeto, "dados", "impa_mp_resultados.json"
    )

    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    return resultados


    # =====================================================
    # PCA
    # =====================================================

    from core.gerar_base_pca import gerar_base_pca
    gerar_base_pca(pasta_projeto)

