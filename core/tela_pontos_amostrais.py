import os
import json

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox
)
from PySide6.QtCore import Qt


class TelaPontosAmostrais(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Register Sampling Units – IMPa")
        self.resize(650, 450)

        # ===============================
        # Projeto ativo
        # ===============================
        self.pasta_projeto = self.main_window.pasta_projeto

        if not self.pasta_projeto:
            QMessageBox.critical(
                self,
                "Erro",
                "No active project.\nPlease create or open a project first."
            )
            self.main_window.mostrar_tela_inicial()
            return

        self.caminho_dados = os.path.join(
            self.pasta_projeto, "dados"
        )
        os.makedirs(self.caminho_dados, exist_ok=True)

        self.caminho_pontos = os.path.join(
            self.caminho_dados, "pontos_amostrais.json"
        )

        # ===============================
        # Carregar pontos existentes
        # ===============================
        self.pontos = {}

        if os.path.exists(self.caminho_pontos):
            with open(self.caminho_pontos, "r", encoding="utf-8") as f:
                self.pontos = json.load(f)

        self.init_ui()
        self.atualizar_lista()

    # ===============================
    # Interface
    # ===============================
    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("Register Sampling Units – IMPa")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:16px;font-weight:bold;")

        # Entrada
        form = QHBoxLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID (ex: A01)")

        self.input_volume = QLineEdit()
        self.input_volume.setPlaceholderText("Volume (L)")

        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Description (optional)")

        form.addWidget(self.input_id)
        form.addWidget(self.input_volume)
        form.addWidget(self.input_desc)

        # Botões
        botoes = QHBoxLayout()

        btn_add = QPushButton("Add / Update")
        btn_remover = QPushButton("Remove Selected")
        btn_salvar = QPushButton("Save Sampling Units")
        btn_voltar = QPushButton("Back")

        btn_add.clicked.connect(self.adicionar_ponto)
        btn_remover.clicked.connect(self.remover_ponto)
        btn_salvar.clicked.connect(self.salvar)
        btn_voltar.clicked.connect(
            self.main_window.mostrar_tela_inicial
        )

        botoes.addWidget(btn_add)
        botoes.addWidget(btn_remover)
        botoes.addWidget(btn_salvar)
        botoes.addWidget(btn_voltar)

        # Lista
        self.lista = QListWidget()

        layout.addWidget(titulo)
        layout.addSpacing(10)
        layout.addLayout(form)
        layout.addSpacing(10)
        layout.addLayout(botoes)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Registered Sampling Units:"))
        layout.addWidget(self.lista)

        self.setLayout(layout)

    # ===============================
    # Lógica
    # ===============================
    def adicionar_ponto(self):
        pid = self.input_id.text().strip()
        vol = self.input_volume.text().strip()
        desc = self.input_desc.text().strip()

        if not pid:
            QMessageBox.warning(self, "Erro", "Enter the sampling unit ID.")
            return

        try:
            vol = float(vol)
            if vol <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self, "Erro", "Volume must be a positive number."
            )
            return

        self.pontos[pid] = {
            "volume_L": vol,
            "descricao": desc
        }

        self.input_id.clear()
        self.input_volume.clear()
        self.input_desc.clear()

        self.atualizar_lista()

    def remover_ponto(self):
        item = self.lista.currentItem()
        if not item:
            return

        pid = item.text().split(" | ")[0]
        del self.pontos[pid]
        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.clear()
        for pid, dados in self.pontos.items():
            texto = f"{pid} | {dados['volume_L']} L"
            if dados.get("descricao"):
                texto += f" | {dados['descricao']}"
            self.lista.addItem(texto)

    def salvar(self):
        if not self.pontos:
            QMessageBox.warning(
                self, "Erro", "No sampling units registered."
            )
            return

        with open(self.caminho_pontos, "w", encoding="utf-8") as f:
            json.dump(self.pontos, f, indent=4, ensure_ascii=False)

        QMessageBox.information(
            self,
            "Success",
            "Sampling units saved successfully."
        )

        self.main_window.mostrar_tela_inicial()
