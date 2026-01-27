import os
import json
from collections import defaultdict

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt


class TelaResultados(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Resultados – IMPₐ e MP Tradicional")
        self.resize(950, 700)

        # ===============================
        # Projeto ativo
        # ===============================
        self.pasta_projeto = self.main_window.pasta_projeto
        if not self.pasta_projeto:
            QMessageBox.critical(self, "Erro", "Nenhum projeto ativo.")
            self.main_window.mostrar_tela_inicial()
            return

        # ===============================
        # Resultados IMPa tradicional
        # ===============================
        self.caminho_resultados = os.path.join(
            self.pasta_projeto, "dados", "impa_mp_resultados.json"
        )

        if not os.path.exists(self.caminho_resultados):
            QMessageBox.critical(self, "Erro", "Resultados do IMPₐ não encontrados.")
            self.main_window.mostrar_tela_inicial()
            return

        with open(self.caminho_resultados, "r", encoding="utf-8") as f:
            self.resultados = json.load(f)

        # ===============================
        # Resultados IMPa–Área (opcional)
        # ===============================
        self.caminho_impa_area = os.path.join(
            self.pasta_projeto, "dados", "impa_area_resultados.json"
        )

        self.resultados_area = None
        if os.path.exists(self.caminho_impa_area):
            with open(self.caminho_impa_area, "r", encoding="utf-8") as f:
                self.resultados_area = json.load(f)

        # ===============================
        # Microplásticos (para área por tipo)
        # ===============================
        self.caminho_micro = os.path.join(
            self.pasta_projeto, "dados", "microplasticos.json"
        )

        self.microplasticos = []
        if os.path.exists(self.caminho_micro):
            with open(self.caminho_micro, "r", encoding="utf-8") as f:
                self.microplasticos = json.load(f)

        # CHAMADA QUE FALTAVA
        self.init_ui()

    # ===============================
    # TEXTO DE RESULTADOS (COMPLETO)
    # ===============================
    def formatar_resultados(self):
        r = self.resultados
        linhas = []

        linhas.append("=== IMPₐ POR PONTO (µm/L) ===")
        for p, v in r["IMPa_por_ponto"].items():
            linhas.append(f"{p:>6} : {v:.3f}")

        linhas.append("\n=== IMPₐ GLOBAL (µm/L) ===")
        linhas.append(f"{r['IMPa_global']:.3f}")

        linhas.append("\n=== IMPₐ POR TIPO (POR PONTO) µm/L ===")
        for ponto, tipos in r["IMPa_por_tipo_por_ponto"].items():
            linhas.append(f"\nPonto {ponto}:")
            for tipo, v in tipos.items():
                linhas.append(f"  {tipo:<12} : {v:.3f}")

        linhas.append("\n=== MP POR PONTO (itens/L) ===")
        for p, v in r["MP_por_ponto"].items():
            linhas.append(f"{p:>6} : {v:.3f}")

        linhas.append("\n=== MP GLOBAL (itens/L) ===")
        linhas.append(f"{r['MP_global']:.3f}")

        linhas.append("\n=== MP POR TIPO (POR PONTO) itens/L ===")
        for ponto, tipos in r["MP_por_tipo_por_ponto"].items():
            linhas.append(f"\nPonto {ponto}:")
            for tipo, v in tipos.items():
                linhas.append(f"  {tipo:<12} : {v:.3f}")

        if self.resultados_area:
            linhas.append("\n=== IMPa–ÁREA POR PONTO (µm²/L) ===")
            for p, v in self.resultados_area["IMPa_area_por_ponto"].items():
                linhas.append(f"{p:>6} : {v:.3f}")

            linhas.append("\n=== IMPa–ÁREA GLOBAL (µm²/L) ===")
            linhas.append(f"{self.resultados_area['IMPa_area_global']:.3f}")

        # Área por tipo
        linhas.append("\n=== IMPa–ÁREA POR TIPO (POR PONTO) µm²/L ===")

        soma_area_tipo = defaultdict(lambda: defaultdict(float))
        for mp in self.microplasticos:
            if mp.get("area_um2") is not None:
                soma_area_tipo[mp["ponto"]][mp["tipo"]] += mp["area_um2"]

        with open(
            os.path.join(self.pasta_projeto, "dados", "pontos_amostrais.json"),
            "r", encoding="utf-8"
        ) as f:
            pontos = json.load(f)

        for ponto, tipos in soma_area_tipo.items():
            V = pontos[ponto]["volume_L"]
            linhas.append(f"\nPonto {ponto}:")
            for tipo, area in tipos.items():
                linhas.append(f"  {tipo:<12} : {(area / V):.3f}")

        return "\n".join(linhas)

    # ===============================
    # INTERFACE
    # ===============================
    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("Resultados do Projeto")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:16px; font-weight:bold;")

        self.texto = QTextEdit()
        self.texto.setReadOnly(True)
        self.texto.setStyleSheet("font-family: Consolas;")
        self.texto.setText(self.formatar_resultados())

        # -------- Linha 1 — IMPₐ --------
        linha_impa = QHBoxLayout()
        btn_impa_ponto = QPushButton("IMPₐ por Ponto")
        btn_impa_tipo = QPushButton("IMPₐ por Tipo")
        btn_impa_percentual = QPushButton("IMPₐ Percentual")
        btn_impa_matriz = QPushButton("Matriz IMPₐ")

        for b in [btn_impa_ponto, btn_impa_tipo, btn_impa_percentual, btn_impa_matriz]:
            b.setFixedHeight(35)
            linha_impa.addWidget(b)

        btn_impa_ponto.clicked.connect(self.visualizar_impa_por_ponto)
        btn_impa_tipo.clicked.connect(self.visualizar_impa_por_tipo)
        btn_impa_percentual.clicked.connect(self.visualizar_percentual_tipo)
        btn_impa_matriz.clicked.connect(self.visualizar_matriz_impa)

        # -------- Linha 2 — MP Tradicional --------
        linha_mp = QHBoxLayout()
        btn_mp_ponto = QPushButton("MP por Ponto")
        btn_mp_tipo = QPushButton("MP por Tipo")
        btn_mp_percentual = QPushButton("MP Percentual")
        btn_mp_matriz = QPushButton("Matriz MP")

        for b in [btn_mp_ponto, btn_mp_tipo, btn_mp_percentual, btn_mp_matriz]:
            b.setFixedHeight(35)
            linha_mp.addWidget(b)

        btn_mp_ponto.clicked.connect(self.visualizar_mp_por_ponto)
        btn_mp_tipo.clicked.connect(self.visualizar_mp_por_tipo)
        btn_mp_percentual.clicked.connect(self.visualizar_mp_percentual)
        btn_mp_matriz.clicked.connect(self.visualizar_matriz_mp)

        # -------- Linha 3 — IMPₐ–Área --------
        linha_area = QHBoxLayout()
        btn_area_ponto = QPushButton("IMPₐ–Área por Ponto")
        btn_area_tipo = QPushButton("IMPₐ–Área por Tipo")
        btn_area_percentual = QPushButton("IMPₐ–Área Percentual")
        btn_area_matriz = QPushButton("Matriz IMPₐ–Área")

        for b in [btn_area_ponto, btn_area_tipo, btn_area_percentual, btn_area_matriz]:
            b.setFixedHeight(35)
            linha_area.addWidget(b)

        btn_area_ponto.clicked.connect(self.visualizar_impa_area_por_ponto)
        btn_area_tipo.clicked.connect(self.visualizar_impa_area_por_tipo)
        btn_area_percentual.clicked.connect(self.visualizar_grafico_percentual_impa_area)
        btn_area_matriz.clicked.connect(self.visualizar_matriz_impa_area)

        # -------- Linha 4 — Outros --------
        linha_outros = QHBoxLayout()
        btn_dist = QPushButton("Distribuição dos Comprimentos")
        btn_box = QPushButton("Boxplot Comprimentos")
        btn_box_area = QPushButton("Boxplot Área")
        btn_pca = QPushButton("PCA")

        for b in [btn_dist, btn_box, btn_box_area, btn_pca]:
            b.setFixedHeight(35)
            linha_outros.addWidget(b)

        btn_dist.clicked.connect(self.visualizar_distribuicao)
        btn_box.clicked.connect(self.visualizar_boxplot)
        btn_box_area.clicked.connect(self.visualizar_boxplot_area)
        btn_pca.clicked.connect(self.visualizar_pca)

        # -------- Navegação --------
        linha_nav = QHBoxLayout()
        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.main_window.mostrar_tela_inicial)
        linha_nav.addStretch()
        linha_nav.addWidget(btn_voltar)

        layout.addWidget(titulo)
        layout.addWidget(self.texto)
        layout.addLayout(linha_impa)
        layout.addLayout(linha_mp)
        layout.addLayout(linha_area)
        layout.addLayout(linha_outros)
        layout.addLayout(linha_nav)

        self.setLayout(layout)

    # ===============================
    # GRÁFICOS — COMPRIMENTO (IMPa)
    # ===============================
    def visualizar_distribuicao(self):
        from core.graficos.grafico_distribuicao import grafico_distribuicao_comprimentos
        grafico_distribuicao_comprimentos(self.pasta_projeto)

    def visualizar_boxplot(self):
        from core.graficos.grafico_boxplot_comprimentos import grafico_boxplot_comprimentos
        grafico_boxplot_comprimentos(self.pasta_projeto)

    def visualizar_matriz_impa(self):
        from core.graficos.grafico_matriz_impa import grafico_matriz_impa
        grafico_matriz_impa(self.pasta_projeto)

    def visualizar_impa_por_ponto(self):
        from core.graficos.grafico_impa_por_ponto import grafico_impa_por_ponto
        grafico_impa_por_ponto(self.pasta_projeto)

    def visualizar_impa_por_tipo(self):
        from core.graficos.grafico_impa_por_tipo import grafico_impa_por_tipo
        grafico_impa_por_tipo(self.pasta_projeto)

    def visualizar_percentual_tipo(self):
        from core.graficos.grafico_percentual_tipo import grafico_impa_percentual_por_tipo
        grafico_impa_percentual_por_tipo(self.pasta_projeto)

    # ===============================
    # PCA
    # ===============================
    def visualizar_pca(self):
        import pandas as pd
        from core.pca_analysis import calcular_pca_com_metadados
        from core.graficos.grafico_pca import plotar_pca
        from core.pca_interpretacao import gerar_texto_interpretacao_pca

        caminho = os.path.join(self.pasta_projeto, "dados", "base_pca.csv")
        df = pd.read_csv(caminho)

        colunas = [c for c in df.columns if c.startswith("IMPa_") or c.startswith("MP_")]

        scores, variancia, loadings = calcular_pca_com_metadados(
            df,
            colunas_numericas=colunas,
            colunas_metadados=["ponto"]
        )

        plotar_pca(scores, variancia, loadings, colunas)

        texto = gerar_texto_interpretacao_pca(
            scores, variancia, loadings, colunas
        )

        QMessageBox.information(
            self,
            "Interpretação da PCA",
            texto
        )

    # ===============================
    # GRÁFICOS — IMPa–ÁREA
    # ===============================
    def visualizar_impa_area_por_ponto(self):
        from core.graficos.grafico_impa_area_por_ponto import grafico_impa_area_por_ponto
        grafico_impa_area_por_ponto(self.pasta_projeto)

    def visualizar_impa_area_por_tipo(self):
        from core.graficos.grafico_impa_area_por_tipo import grafico_impa_area_por_tipo
        grafico_impa_area_por_tipo(self.pasta_projeto)

    def visualizar_matriz_impa_area(self):
        from core.graficos.grafico_matriz_impa_area import grafico_matriz_impa_area
        grafico_matriz_impa_area(self.pasta_projeto)

    def visualizar_boxplot_area(self):
        from core.graficos.grafico_boxplot_area import grafico_boxplot_area_microplasticos
        grafico_boxplot_area_microplasticos(self.pasta_projeto)

    def visualizar_grafico_percentual_impa_area(self):
        from core.graficos.grafico_percentual_impa_area import grafico_impa_area_percentual_por_tipo
        grafico_impa_area_percentual_por_tipo(self.pasta_projeto)

    # ===============================
    # MP TRADICIONAL — GRÁFICOS
    # ===============================
    def visualizar_mp_por_ponto(self):
        from core.graficos.grafico_mp_por_ponto import grafico_mp_por_ponto
        grafico_mp_por_ponto(self.pasta_projeto)

    def visualizar_mp_por_tipo(self):
        from core.graficos.grafico_mp_por_tipo import grafico_mp_por_tipo
        grafico_mp_por_tipo(self.pasta_projeto)

    def visualizar_mp_percentual(self):
        from core.graficos.grafico_mp_percentual_tipo import grafico_mp_percentual_por_tipo
        grafico_mp_percentual_por_tipo(self.pasta_projeto)

    def visualizar_matriz_mp(self):
        from core.graficos.grafico_matriz_mp import grafico_matriz_mp
        grafico_matriz_mp(self.pasta_projeto)
