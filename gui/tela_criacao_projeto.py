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

        self.setWindowTitle("Novo Projeto")
        self.resize(600, 400)

        self.pasta_base = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

       

        # ===============================
        # Título
        # ===============================
        titulo = QLabel("CRIANDO NOVO PROJETO DE QUANTIFICAÇÃO DE MICROPLASTICO-IMP")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:18px; font-weight:bold;")

        lbl_nome = QLabel("Nome do projeto:")
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Ex: Microplasticos_Rio_X")

        lbl_pasta = QLabel("Pasta onde o projeto será salvo:")
        btn_pasta = QPushButton("Selecionar pasta")
        self.lbl_pasta_escolhida = QLabel("Nenhuma pasta selecionada")
        self.lbl_pasta_escolhida.setStyleSheet("color: gray;")

        btn_pasta.clicked.connect(self.selecionar_pasta)

        btn_criar = QPushButton("Criar projeto")
        btn_cancelar = QPushButton("Cancelar")

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
            QMessageBox.warning(self, "Erro", "Informe o nome do projeto.")
            return

        if not self.pasta_base:
            QMessageBox.warning(
                self, "Erro", "Selecione a pasta onde o projeto será salvo."
            )
            return

        caminho = os.path.join(self.pasta_base, nome)

        if os.path.exists(caminho):
            QMessageBox.warning(
                self,
                "Erro",
                "Já existe um projeto com este nome nessa pasta."
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
                "Projeto criado",
                f"Projeto '{nome}' criado com sucesso."
            )

            self.main_window.mostrar_tela_inicial()

        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Erro ao criar o projeto:\n{e}"
            )
