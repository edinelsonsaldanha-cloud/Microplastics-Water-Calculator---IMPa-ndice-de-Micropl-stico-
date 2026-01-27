import os
import json
import numpy as np
import cv2

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,
    QComboBox, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage


class TelaCalibracao(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Calibração Microscópica")
        self.resize(950, 720)

        # ===============================
        # Projeto ativo
        # ===============================
        self.pasta_projeto = self.main_window.pasta_projeto

        if not self.pasta_projeto:
            QMessageBox.critical(
                self,
                "Erro",
                "Nenhum projeto ativo.\nCrie ou abra um projeto primeiro."
            )
            self.main_window.mostrar_tela_inicial()
            return

        os.makedirs(os.path.join(self.pasta_projeto, "dados"), exist_ok=True)

        self.caminho_cal = os.path.join(
            self.pasta_projeto, "dados", "calibracoes.json"
        )

        # ===============================
        # Estado interno
        # ===============================
        self.img_original = None
        self.img_display = None
        self.imagem_path = None

        self.pontos_display = []
        self.escala = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.img_disp_w = 0
        self.img_disp_h = 0

        self.init_ui()

    # ===============================
    # Interface
    # ===============================
    def init_ui(self):
#
  #      from gui.widgets.cabecalho_rodape_institucional import (
  #  CabecalhoRodapeInstitucional
#)

#        
        layout = QVBoxLayout()
        
        
        # Barra superior
        barra = QHBoxLayout()

        self.combo_objetiva = QComboBox()
        self.combo_objetiva.addItems(
            ["4x", "10x", "20x", "40x", "100x"]
        )

        self.input_distancia = QLineEdit()
        self.input_distancia.setPlaceholderText(
            "Distância real entre os pontos (µm)"
        )

        btn_img = QPushButton("Carregar imagem da escala")
        btn_reset = QPushButton("Refazer pontos")
        btn_calibrar = QPushButton("Calibrar e salvar")
        btn_voltar = QPushButton("Voltar")

        btn_img.clicked.connect(self.carregar_imagem)
        btn_reset.clicked.connect(self.resetar_pontos)
        btn_calibrar.clicked.connect(self.calibrar)
        btn_voltar.clicked.connect(
            self.main_window.mostrar_tela_inicial
        )

        barra.addWidget(QLabel("Objetiva:"))
        barra.addWidget(self.combo_objetiva)
        barra.addSpacing(10)
        barra.addWidget(QLabel("Distância real (µm):"))
        barra.addWidget(self.input_distancia)
        barra.addStretch()
        barra.addWidget(btn_img)
        barra.addWidget(btn_reset)
        barra.addWidget(btn_calibrar)

        # Área da imagem
        self.lbl_img = QLabel("Nenhuma imagem carregada")
        self.lbl_img.setAlignment(Qt.AlignCenter)
        self.lbl_img.setMinimumHeight(520)
        self.lbl_img.setStyleSheet("border: 1px solid gray;")

        # Info
        self.lbl_info = QLabel("Clique em dois pontos da régua de escala.")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("font-weight: bold;")
       
        #layout.addWidget(CabecalhoRodapeInstitucional(self))
        layout.addLayout(barra)
        layout.addSpacing(10)
        layout.addWidget(self.lbl_img)
        layout.addSpacing(10)
        layout.addWidget(self.lbl_info)
        layout.addStretch()
        layout.addWidget(btn_voltar)
        
        self.setLayout(layout)

    # ===============================
    # Carregar imagem
    # ===============================
    def carregar_imagem(self):
        from PySide6.QtWidgets import QFileDialog

        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar imagem da escala",
            "",
            "Imagens (*.png *.jpg *.jpeg *.tif)"
        )

        if not arquivo:
            return

        self.imagem_path = arquivo
        self.img_original = cv2.imread(arquivo)

        if self.img_original is None:
            QMessageBox.critical(self, "Erro", "Erro ao carregar imagem.")
            return

        self.pontos_display = []

        h, w, _ = self.img_original.shape
        lbl_w = self.lbl_img.width()
        lbl_h = self.lbl_img.height()

        self.escala = min(lbl_w / w, lbl_h / h)

        new_w = int(w * self.escala)
        new_h = int(h * self.escala)

        self.img_display = cv2.resize(
            self.img_original,
            (new_w, new_h),
            interpolation=cv2.INTER_AREA
        )

        self.img_disp_w = new_w
        self.img_disp_h = new_h

        self.offset_x = (lbl_w - new_w) // 2
        self.offset_y = (lbl_h - new_h) // 2

        self.atualizar_display()
        self.lbl_img.mousePressEvent = self.registrar_clique
        self.lbl_info.setText("Clique em DOIS pontos da escala.")

    # ===============================
    # Clique do mouse
    # ===============================
    def registrar_clique(self, event):
        if self.img_display is None or len(self.pontos_display) >= 2:
            return

        x_lbl = int(event.position().x())
        y_lbl = int(event.position().y())

        x_img = x_lbl - self.offset_x
        y_img = y_lbl - self.offset_y

        if (
            x_img < 0 or y_img < 0
            or x_img >= self.img_disp_w
            or y_img >= self.img_disp_h
        ):
            return

        self.pontos_display.append((x_img, y_img))
        self.atualizar_display()

        self.lbl_info.setText(
            f"Pontos selecionados: {len(self.pontos_display)}/2"
        )

    # ===============================
    # Atualizar imagem
    # ===============================
    def atualizar_display(self):
        if self.img_display is None:
            return

        img = self.img_display.copy()

        for p in self.pontos_display:
            cv2.circle(img, p, 4, (0, 0, 255), -1)

        if len(self.pontos_display) == 2:
            cv2.line(
                img,
                self.pontos_display[0],
                self.pontos_display[1],
                (255, 0, 0),
                2
            )

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, _ = img_rgb.shape

        qimg = QImage(
            img_rgb.data,
            w,
            h,
            3 * w,
            QImage.Format_RGB888
        )

        self.lbl_img.setPixmap(QPixmap.fromImage(qimg))

    # ===============================
    # Reset
    # ===============================
    def resetar_pontos(self):
        self.pontos_display = []
        self.atualizar_display()
        self.lbl_info.setText("Pontos resetados. Clique novamente.")

    # ===============================
    # Calibrar e salvar
    # ===============================
    def calibrar(self):
        if len(self.pontos_display) < 2:
            QMessageBox.warning(
                self, "Erro", "Selecione dois pontos da escala."
            )
            return

        try:
            dist_real_um = float(self.input_distancia.text())
        except ValueError:
            QMessageBox.warning(
                self,
                "Erro",
                "Informe a distância real em micrômetros (µm)."
            )
            return

        p1 = np.array(self.pontos_display[0]) / self.escala
        p2 = np.array(self.pontos_display[1]) / self.escala

        dist_px = np.linalg.norm(p2 - p1)
        fator = dist_real_um / dist_px

        objetiva = self.combo_objetiva.currentText()

        calibracoes = {}
        if os.path.exists(self.caminho_cal):
            with open(self.caminho_cal, "r", encoding="utf-8") as f:
                calibracoes = json.load(f)

        calibracoes[objetiva] = {
            "um_por_pixel": fator,
            "distancia_real_um": dist_real_um,
            "pixels_medidos": dist_px
        }

        with open(self.caminho_cal, "w", encoding="utf-8") as f:
            json.dump(calibracoes, f, indent=4, ensure_ascii=False)

        QMessageBox.information(
            self,
            "Calibração salva",
            f"Objetiva {objetiva} calibrada com sucesso.\n"
            f"{fator:.4f} µm/px"
        )

        self.resetar_pontos()

