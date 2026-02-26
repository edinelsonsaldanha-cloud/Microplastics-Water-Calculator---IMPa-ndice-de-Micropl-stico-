import numpy as np
import pandas as pd


def gerar_texto_interpretacao_pca(
    df_scores: pd.DataFrame,
    variancia_explicada: np.ndarray,
    loadings: np.ndarray,
    nomes_variaveis: list
):
    """
    Gera texto interpretativo automático para PCA (PC1 e PC2)
    """

    texto = []

    # ===============================
    # Variância explicada
    # ===============================
    texto.append(
        f"A Análise de Componentes Principais (PCA) revelou que os dois "
        f"primeiros componentes explicam conjuntamente "
        f"{variancia_explicada[:2].sum():.1f}% da variância total dos dados, "
        f"sendo {variancia_explicada[0]:.1f}% associada ao PC1 e "
        f"{variancia_explicada[1]:.1f}% ao PC2."
    )

    # ===============================
    # Variáveis dominantes em cada PC
    # ===============================
    idx_pc1 = np.argsort(np.abs(loadings[:, 0]))[::-1][:3]
    idx_pc2 = np.argsort(np.abs(loadings[:, 1]))[::-1][:3]

    vars_pc1 = ", ".join([nomes_variaveis[i] for i in idx_pc1])
    vars_pc2 = ", ".join([nomes_variaveis[i] for i in idx_pc2])

    texto.append(
        f"O primeiro componente principal (PC1) é fortemente influenciado "
        f"pelas variáveis {vars_pc1}, indicando que este eixo representa "
        f"principalmente a variação associada à intensidade e composição "
        f"dos microplásticos quantificados."
    )

    texto.append(
        f"O segundo componente principal (PC2) apresenta maior contribuição "
        f"das variáveis {vars_pc2}, sugerindo um gradiente secundário "
        f"relacionado a diferenças específicas na distribuição dos tipos "
        f"de microplásticos."
    )

    # ===============================
    # Organização dos pontos
    # ===============================
    centroides = (
        df_scores
        .groupby("ponto")[["PC1", "PC2"]]
        .mean()
    )

    texto.append(
        "A distribuição dos pontos amostrais no espaço multivariado indica "
        "a existência de padrões de similaridade e diferenciação entre os "
        "locais de amostragem. Pontos próximos entre si no gráfico de scores "
        "apresentam características semelhantes quanto aos índices de "
        "microplásticos, enquanto pontos mais distantes refletem condições "
        "ambientais contrastantes."
    )

    texto.append(
        "De modo geral, a PCA evidencia que as variações observadas nos índices "
        "IMPₐ e MP tradicional são suficientes para discriminar os pontos "
        "amostrais, reforçando a utilidade da abordagem multivariada para a "
        "interpretação integrada dos dados de microplásticos em água."
    )

    return "\n\n".join(texto)
