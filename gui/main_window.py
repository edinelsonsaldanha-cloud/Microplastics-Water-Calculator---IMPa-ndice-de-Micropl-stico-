import os
import json

from PySide6.QtWidgets import QFileDialog, QMessageBox

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from gui.tela_inicial import TelaInicial


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quantificação de Microplásticos - Índice de Microplásticos em Água - IMPₐ")
        self.resize(1300, 850)
        self.setMinimumSize(1100, 750)

        # Projeto ativo
        self.pasta_projeto = None

        # Container central
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.setCentralWidget(self.container)

        self.mostrar_tela_inicial()

    # ===============================
    # Utilitário
    # ===============================
    def limpar_tela(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    # ===============================
    # Navegação entre telas
    # ===============================
    def mostrar_tela_inicial(self):
        self.limpar_tela()
        self.layout.addWidget(TelaInicial(self))

    def mostrar_criacao_projeto(self):
        from gui.tela_criacao_projeto import TelaCriacaoProjeto
        self.limpar_tela()
        self.layout.addWidget(TelaCriacaoProjeto(self))

    def mostrar_pontos_amostrais(self):
        from gui.tela_pontos_amostrais import TelaPontosAmostrais
        self.limpar_tela()
        self.layout.addWidget(TelaPontosAmostrais(self))

    def mostrar_calibracao(self):
        from gui.tela_calibracao import TelaCalibracao
        self.limpar_tela()
        self.layout.addWidget(TelaCalibracao(self))

    def mostrar_medicao(self):
        from gui.tela_medicao import TelaMedicao
        self.limpar_tela()
        self.layout.addWidget(TelaMedicao(self))

    def mostrar_resultados(self):
        from gui.tela_resultados import TelaResultados
        self.limpar_tela()
        self.layout.addWidget(TelaResultados(self))

        
        
    # ===============================
    # Abrir Projeto
    # ===============================
    def abrir_projeto(self):
        pasta = QFileDialog.getExistingDirectory(
            self,
            "Selecione a pasta do projeto IMPₐ"
        )

        if not pasta:
            return

        dados = os.path.join(pasta, "dados")
        resultados = os.path.join(pasta, "resultados")
        imagens = os.path.join(pasta, "imagens")

        arquivos_necessarios = [
            os.path.join(dados, "pontos_amostrais.json"),
            os.path.join(dados, "calibracoes.json"),
            os.path.join(dados, "microplasticos.json")
        ]

        if not (
            os.path.isdir(dados)
            and os.path.isdir(resultados)
            and os.path.isdir(imagens)
        ):
            QMessageBox.critical(
                self,
                "Projeto inválido",
                "A pasta selecionada não possui a estrutura de um projeto IMPₐ."
            )
            return

        for arq in arquivos_necessarios:
            if not os.path.exists(arq):
                QMessageBox.critical(
                    self,
                    "Projeto inválido",
                    f"Arquivo obrigatório não encontrado:\n{os.path.basename(arq)}"
                )
                return

        # Projeto válido → ativar
        self.pasta_projeto = pasta

        QMessageBox.information(
            self,
            "Projeto carregado",
            "Projeto IMPₐ carregado com sucesso."
        )

        self.mostrar_tela_inicial()
