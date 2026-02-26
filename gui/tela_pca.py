from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class TelaPCA(QWidget):
    def __init__(self, df_scores, variancia):
        super().__init__()

        self.setWindowTitle("Análise de Componentes Principais (PCA)")
        self.resize(900, 700)

        layout = QVBoxLayout(self)

        titulo = QLabel("PCA — PC1 × PC2")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:16px; font-weight:bold;")

        layout.addWidget(titulo)

        # ===============================
        # Gráfico
        # ===============================
        fig, ax = plt.subplots(figsize=(7, 6))

        pontos = df_scores["ponto"].unique()
        periodos = df_scores["periodo"].unique()

        for ponto in pontos:
            for periodo in periodos:
                sub = df_scores[
                    (df_scores["ponto"] == ponto) &
                    (df_scores["periodo"] == periodo)
                ]

                ax.scatter(
                    sub["PC1"],
                    sub["PC2"],
                    label=f"{ponto} - {periodo}",
                    s=60
                )

        ax.set_xlabel(f"PC1 ({variancia[0]*100:.1f}%)")
        ax.set_ylabel(f"PC2 ({variancia[1]*100:.1f}%)")
        ax.legend(fontsize=8)
        ax.grid(True)

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
