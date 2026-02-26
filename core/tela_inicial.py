import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class TelaInicial(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # ===============================
        # Cabeçalho institucional
        # ===============================
        cabecalho = QHBoxLayout()

        caminho_logo_esq = os.path.join(
            os.path.dirname(__file__),
            "..", "resources", "logos", "logo_instituicao.png"
        )
        caminho_logo_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "resources", "logos", "logo_impa.png"
        )

        lbl_logo_esq = QLabel()
        lbl_logo_dir = QLabel()

        if os.path.exists(caminho_logo_esq):
            pix = QPixmap(caminho_logo_esq).scaled(
                80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            lbl_logo_esq.setPixmap(pix)

        if os.path.exists(caminho_logo_dir):
            pix = QPixmap(caminho_logo_dir).scaled(
                80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            lbl_logo_dir.setPixmap(pix)

        texto_inst = QVBoxLayout()
        lbl_uni = QLabel("FEDERAL UNIVERSITY OF PARÁ")
        lbl_lab = QLabel(
            "COASTAL AND OCEANIC ENVIRONMENTAL GEOCHEMISTRY LABORATORY – LABGECO"
        )

        for lbl in (lbl_uni, lbl_lab):
            lbl.setAlignment(Qt.AlignCenter)

        lbl_uni.setStyleSheet("font-size:16px; font-weight:bold;")
        lbl_lab.setStyleSheet("font-size:16px; color:black; font-weight:bold;")

        texto_inst.addWidget(lbl_uni)
        texto_inst.addWidget(lbl_lab)

        cabecalho.addWidget(lbl_logo_esq)
        cabecalho.addStretch()
        cabecalho.addLayout(texto_inst)
        cabecalho.addStretch()
        cabecalho.addWidget(lbl_logo_dir)

        # ===============================
        # Título do sistema
        # ===============================
        titulo = QLabel("MICROPLASTIC QUANTIFICATION\nMicroplastic Index for Water, Soil, and Food Matrices – IMPa Version 1.0")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:16px; font-weight:bold;")

        subtitulo = QLabel(
            "Microplastic Quantification Based on Count, Length, Area, and Morphological Classification"
        )
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("color: gray; font-weight:bold;")

        # ===============================
        # Botões de projeto
        # ===============================
        btn_novo = QPushButton("Create New Project")
        btn_abrir = QPushButton("Open Existing Project")
        btn_novo.setFixedHeight(40)
        btn_abrir.setFixedHeight(40)

        btn_novo.clicked.connect(
            self.main_window.mostrar_criacao_projeto
        )
        btn_abrir.clicked.connect(
            self.main_window.abrir_projeto
        )

        # ===============================
        # Botões de trabalho
        # ===============================
        btn_pontos = QPushButton("Register Sampling Units")
        btn_calibracao = QPushButton("Microscope Calibration")
        btn_medicao = QPushButton("Microplastic Measurement")
        btn_resultados = QPushButton("Results (IMPa-L / IMPa-A / MP)")
        btn_sair = QPushButton("Exit")

        for b in [btn_pontos, btn_calibracao, btn_medicao, btn_resultados]:
            b.setFixedHeight(40)

        btn_sair.setFixedHeight(30)

        btn_pontos.clicked.connect(
            self.main_window.mostrar_pontos_amostrais
        )
        btn_calibracao.clicked.connect(
            self.main_window.mostrar_calibracao
        )
        btn_medicao.clicked.connect(
            self.main_window.mostrar_medicao
        )
        btn_resultados.clicked.connect(
            self.main_window.mostrar_resultados
        )
        btn_sair.clicked.connect(self.main_window.close)

        # ===============================
        # Rodapé
        # ===============================
        rodape = QLabel(
            "Developed by Prof. Edinelson Saldanha, Ph.D."
        )
        rodape.setAlignment(Qt.AlignRight)
        rodape.setStyleSheet("color:black; font-size:12px;")

        # ===============================
        # Layout final
        # ===============================
        layout.addLayout(cabecalho)
        layout.addSpacing(10)
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(25)

        layout.addWidget(btn_novo)
        layout.addWidget(btn_abrir)
        layout.addSpacing(15)

        layout.addWidget(btn_pontos)
        layout.addWidget(btn_calibracao)
        layout.addWidget(btn_medicao)
        layout.addWidget(btn_resultados)

        layout.addStretch()
        layout.addWidget(btn_sair)
        layout.addWidget(rodape)

        self.setLayout(layout)
