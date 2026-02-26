import os
import json

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class TelaCriacaoProjeto(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("New Project")
        self.resize(600, 400)

        self.pasta_base = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

       

        # ===============================
        # Título
        # ===============================
        titulo = QLabel("New Microplastic Quantification Project – IMPa")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:18px; font-weight:bold;")

        lbl_nome = QLabel("Project Name:")
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Ex: Microplasticos_River_X")

        lbl_pasta = QLabel("Project Directory:")
        btn_pasta = QPushButton("Select Directory")
        self.lbl_pasta_escolhida = QLabel("No directory selected")
        self.lbl_pasta_escolhida.setStyleSheet("color: gray;")

        btn_pasta.clicked.connect(self.selecionar_pasta)

        btn_criar = QPushButton("Create Project")
        btn_cancelar = QPushButton("Cancel")

        btn_criar.setFixedHeight(35)
        btn_cancelar.setFixedHeight(30)

        btn_criar.clicked.connect(self.criar_projeto)
        btn_cancelar.clicked.connect(
            self.main_window.mostrar_tela_inicial
        )

        # ===============================
        # Layout final
        # ===============================
        layout.addSpacing(10)
        layout.addWidget(titulo)
        layout.addSpacing(15)
        layout.addWidget(lbl_nome)
        layout.addWidget(self.input_nome)
        layout.addSpacing(10)
        layout.addWidget(lbl_pasta)
        layout.addWidget(btn_pasta)
        layout.addWidget(self.lbl_pasta_escolhida)
        layout.addStretch()
        layout.addWidget(btn_criar)
        layout.addWidget(btn_cancelar)

        self.setLayout(layout)

    # ===============================
    # Ações
    # ===============================
    def selecionar_pasta(self):
        pasta = QFileDialog.getExistingDirectory(
            self, "Selecionar pasta do projeto"
        )
        if pasta:
            self.pasta_base = pasta
            self.lbl_pasta_escolhida.setText(pasta)

    def criar_projeto(self):
        nome = self.input_nome.text().strip()

        if not nome:
            QMessageBox.warning(self,"Missing Information", "Please enter the project name.")
            return

        if not self.pasta_base:
            QMessageBox.warning(
                self, "Error", "Please select a project directory."
            )
            return

        caminho = os.path.join(self.pasta_base, nome)

        if os.path.exists(caminho):
            QMessageBox.warning(
                self,
                "Erro",
                "A project with this name already exists."
            )
            return

        try:
            os.makedirs(os.path.join(caminho, "dados"))
            os.makedirs(os.path.join(caminho, "resultados"))
            os.makedirs(os.path.join(caminho, "imagens"))

            # Arquivos base
            with open(os.path.join(caminho, "dados", "pontos_amostrais.json"), "w") as f:
                json.dump({}, f, indent=4)

            with open(os.path.join(caminho, "dados", "calibracoes.json"), "w") as f:
                json.dump({}, f, indent=4)

            with open(os.path.join(caminho, "dados", "microplasticos.json"), "w") as f:
                json.dump([], f, indent=4)

            # Definir projeto ativo
            self.main_window.pasta_projeto = caminho

            QMessageBox.information(
                self,
                "Project created",
                f"Projeto '{nome}' Project successfully created."
            )

            self.main_window.mostrar_tela_inicial()

        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Erro at Project created:\n{e}"
            )
