import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


def calcular_pca_com_metadados(
    df: pd.DataFrame,
    colunas_numericas: list,
    colunas_metadados: list = None,
    n_componentes: int = 2
):
    """
    Executa PCA apenas com variáveis numéricas,
    preservando metadados (ex.: ponto, periodo).

    Retorna:
    - df_scores : DataFrame com PC1, PC2 + metadados
    - variancia_explicada : array (%)
    - loadings : matriz (variáveis x componentes)
    """

    # ===============================
    # 1. Seleção EXPLÍCITA das variáveis numéricas
    # ===============================
    X = df[colunas_numericas].copy()

    # Forçar conversão numérica
    X = X.apply(pd.to_numeric, errors="coerce")

    if X.shape[1] == 0:
        raise ValueError(
            "Nenhuma variável numérica válida foi fornecida para a PCA."
        )

    # ===============================
    # 2. Remover colunas 100% NaN
    # ===============================
    X = X.dropna(axis=1, how="all")

    if X.shape[1] == 0:
        raise ValueError(
            "Todas as variáveis numéricas estão vazias (NaN)."
        )

    # ===============================
    # 3. Imputação (apenas numéricas)
    # ===============================
    imputer = SimpleImputer(strategy="mean")
    X_imputado = imputer.fit_transform(X)

    # ===============================
    # 4. Padronização
    # ===============================
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputado)

    # ===============================
    # 5. PCA
    # ===============================
    pca = PCA(n_components=n_componentes)
    scores = pca.fit_transform(X_scaled)

    variancia_explicada = pca.explained_variance_ratio_ * 100

    # ===============================
    # 6. Scores
    # ===============================
    df_scores = pd.DataFrame(
        scores,
        columns=[f"PC{i+1}" for i in range(n_componentes)],
        index=df.index
    )

    # ===============================
    # 7. Reanexar metadados
    # ===============================
    if colunas_metadados:
        for col in colunas_metadados:
            if col in df.columns:
                df_scores[col] = df[col]

    # ===============================
    # 8. Loadings
    # ===============================
    loadings = pd.DataFrame(
        pca.components_.T,
        index=X.columns,
        columns=[f"PC{i+1}" for i in range(n_componentes)]
    )

    return df_scores, variancia_explicada, loadings.values
