import os
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class CabecalhoRodapeInstitucional(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(10, 10, 10, 10)

        # ==================================================
        # CAMINHO BASE ABSOLUTO (CORREÇÃO PRINCIPAL)
        # ==================================================
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        pasta_logos = os.path.join(base_path, "resources", "logos")

        # ===============================
        # CABEÇALHO
        # ===============================
        cabecalho = QHBoxLayout()

        # ---------- LOGO ESQUERDA ----------
        caminho_logo_esq = os.path.normpath(
            os.path.join(
            base_path, "..", "resources", "logos", "logo_instituicao.png")
        )

        logo_esq = QLabel()
        if os.path.exists(caminho_logo_esq):
            pix = QPixmap(caminho_logo_esq).scaled(
                90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_esq.setPixmap(pix)
        else:
            logo_esq.setText("LOGO\nUFPA")
            logo_esq.setAlignment(Qt.AlignCenter)

        # ---------- TEXTO CENTRAL ----------
        texto = QVBoxLayout()

        lbl_univ = QLabel("Universidade Federal do Pará")
        lbl_univ.setAlignment(Qt.AlignCenter)
        lbl_univ.setStyleSheet("font-weight:bold; font-size:14px;")

        lbl_lab = QLabel(
            "Laboratório de Geoquímica Ambiental Costeira e Oceânica"
        )
        lbl_lab.setAlignment(Qt.AlignCenter)
        lbl_lab.setStyleSheet("font-size:12px;")

        texto.addWidget(lbl_univ)
        texto.addWidget(lbl_lab)

        # ---------- LOGO DIREITA ----------
        caminho_logo_dir = os.path.normpath(
            os.path.join(base_path, "..", "resources", "logos", "logoimpa.png")
        )

        logo_dir = QLabel()
        if os.path.exists(caminho_logo_dir):
            pix = QPixmap(caminho_logo_dir).scaled(
                90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_dir.setPixmap(pix)
        else:
            logo_dir.setText("LOGO\nIMPₐ")
            logo_dir.setAlignment(Qt.AlignCenter)

        cabecalho.addWidget(logo_esq)
        cabecalho.addStretch()
        cabecalho.addLayout(texto)
        cabecalho.addStretch()
        cabecalho.addWidget(logo_dir)

        # ===============================
        # RODAPÉ
        # ===============================
        rodape = QLabel("Prof. Dr. Edinelson Saldanha")
        rodape.setAlignment(Qt.AlignCenter)
        rodape.setStyleSheet("color: gray; font-size:10px;")

        # ===============================
        # MONTAGEM FINAL
        # ===============================
        layout_principal.addLayout(cabecalho)
        layout_principal.addStretch()
        layout_principal.addWidget(rodape)
