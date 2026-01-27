import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use("QtAgg")

def plotar_pca(
    df_scores,
    variancia,
    loadings,
    nomes_variaveis
):
    """
    Gráfico PCA com scores + loadings (biplot científico)
    """

    plt.figure(figsize=(9, 7))

    # ===============================
    # 1. Scatter dos scores
    # ===============================
    grupos = df_scores["ponto"].unique()

    for g in grupos:
        sub = df_scores[df_scores["ponto"] == g]
        plt.scatter(
            sub["PC1"],
            sub["PC2"],
            s=60,
            alpha=0.75,
            label=g
        )

    # ===============================
    # 2. Loadings (vetores)
    # ===============================
    escala = 0.85 * max(
        df_scores["PC1"].abs().max(),
        df_scores["PC2"].abs().max()
    )

    for i, var in enumerate(nomes_variaveis):
        x = loadings[i, 0] * escala
        y = loadings[i, 1] * escala

        plt.arrow(
            0, 0, x, y,
            color="black",
            alpha=0.8,
            width=0.002,
            head_width=0.04,
            length_includes_head=True
        )

        plt.text(
            x * 1.08,
            y * 1.08,
            var.replace("_", " "),
            fontsize=9,
            ha="center",
            va="center"
        )

    # ===============================
    # 3. Eixos e estética
    # ===============================
    plt.axhline(0, color="gray", lw=0.8, alpha=0.5)
    plt.axvline(0, color="gray", lw=0.8, alpha=0.5)

    plt.xlabel(f"PC1 ({variancia[0]:.1f}%)", fontsize=11)
    plt.ylabel(f"PC2 ({variancia[1]:.1f}%)", fontsize=11)

    plt.title(
        "PCA – IMPₐ e MP Tradicional\n(Biplot com variáveis explicativas)",
        fontsize=13,
        weight="bold"
    )

    plt.grid(alpha=0.25)
    plt.legend(title="Ponto amostral", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    plt.show()