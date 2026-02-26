import os
import json
import numpy as np
import cv2

from core.calculo_impa import calcular_impa_e_mp
from core.calculo_impa_area import calcular_impa_area

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog,
    QComboBox, QMessageBox, QListWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage


class TelaMedicao(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Microplastic Measurement – IMPa")
        self.resize(1200, 800)

        self.pasta_projeto = self.main_window.pasta_projeto
        if not self.pasta_projeto:
            QMessageBox.critical(self, "Warning", "No active project.")
            self.main_window.mostrar_tela_inicial()
            return

        self.caminho_cal = os.path.join(self.pasta_projeto, "dados", "calibracoes.json")
        self.caminho_pontos = os.path.join(self.pasta_projeto, "dados", "pontos_amostrais.json")
        self.caminho_micro = os.path.join(self.pasta_projeto, "dados", "microplasticos.json")
        self.pasta_imagens = os.path.join(self.pasta_projeto, "imagens")

        with open(self.caminho_cal, "r", encoding="utf-8") as f:
            self.calibracoes = json.load(f)

        with open(self.caminho_pontos, "r", encoding="utf-8") as f:
            self.pontos_amostrais = json.load(f)

        self.microplasticos = []
        if os.path.exists(self.caminho_micro):
            with open(self.caminho_micro, "r", encoding="utf-8") as f:
                self.microplasticos = json.load(f)

        self.img_original = None
        self.img_display = None
        self.imagem_path = None
        self.pontos_display = []

        self.escala = 1.0
        self.offset_x = 0
        self.offset_y = 0

        self.modo_edicao = False
        self.idx_editando = None
        self.ponto_selecionado = None

        self.init_ui()
    def init_ui(self):
        layout_principal = QVBoxLayout()
        layout_central = QHBoxLayout()

        col_img = QVBoxLayout()
        barra = QHBoxLayout()

        self.combo_ponto = QComboBox()
        self.combo_ponto.addItems(self.pontos_amostrais.keys())
        self.combo_ponto.currentTextChanged.connect(self.atualizar_lista)

        self.combo_objetiva = QComboBox()
        self.combo_objetiva.addItems(self.calibracoes.keys())

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Fiber", "Fragment", "Film", "Pellet", "Other"])

        # NOVA VARIÁVEL COR
        self.combo_cor = QComboBox()
        self.combo_cor.addItems(["Blue", "Black", "Green", "Red", "Gray"])

        btn_img = QPushButton("Load Image")
        btn_salvar = QPushButton("Save Microplastic")

        btn_img.clicked.connect(self.carregar_imagem)
        btn_salvar.clicked.connect(self.salvar_microplastico)

        barra.addWidget(QLabel("Sampling Unit:"))
        barra.addWidget(self.combo_ponto)
        barra.addWidget(QLabel("Objective Lens:"))
        barra.addWidget(self.combo_objetiva)
        barra.addWidget(QLabel("Morphological Category:"))
        barra.addWidget(self.combo_tipo)
        barra.addWidget(QLabel("Color:"))
        barra.addWidget(self.combo_cor)
        barra.addStretch()
        barra.addWidget(btn_img)
        barra.addWidget(btn_salvar)

        self.lbl_img = QLabel("No image loaded.")
        self.lbl_img.setAlignment(Qt.AlignCenter)
        self.lbl_img.setMinimumSize(800, 500)
        self.lbl_img.setStyleSheet("border:1px solid gray;")

        self.lbl_info = QLabel("Normal mode")
        self.lbl_info.setAlignment(Qt.AlignCenter)

        col_img.addLayout(barra)
        col_img.addWidget(self.lbl_img)
        col_img.addWidget(self.lbl_info)

        col_lista = QVBoxLayout()
        col_lista.addWidget(QLabel("Sampling Unit"))

        self.lista = QListWidget()
        self.lista.itemClicked.connect(self.carregar_microplastico)
        col_lista.addWidget(self.lista)

        btn_editar = QPushButton("Edit Points")
        btn_remover = QPushButton("Remove Point")
        btn_excluir_mp = QPushButton("Delete Microplastic")
        btn_salvar_ed = QPushButton("Save Changes")
        btn_cancelar = QPushButton("Cancel Editing")

        btn_editar.clicked.connect(self.entrar_edicao)
        btn_remover.clicked.connect(self.remover_ponto)
        btn_excluir_mp.clicked.connect(self.excluir_microplastico)
        btn_salvar_ed.clicked.connect(self.salvar_edicao)
        btn_cancelar.clicked.connect(self.cancelar_edicao)

        col_lista.addWidget(btn_editar)
        col_lista.addWidget(btn_remover)
        col_lista.addWidget(btn_excluir_mp)
        col_lista.addWidget(btn_salvar_ed)
        col_lista.addWidget(btn_cancelar)

        layout_central.addLayout(col_img, 4)
        layout_central.addLayout(col_lista, 1)

        rodape = QHBoxLayout()

        btn_calc = QPushButton("Compute IMPa-L")
        btn_calc.clicked.connect(self.calcular_impa)

        btn_calc_area = QPushButton("Compute IMPa-A")
        btn_calc_area.clicked.connect(self.calcular_impa_area)

        btn_voltar = QPushButton("Back")
        btn_voltar.clicked.connect(self.main_window.mostrar_tela_inicial)

        rodape.addWidget(btn_calc)
        rodape.addWidget(btn_calc_area)
        rodape.addStretch()
        rodape.addWidget(btn_voltar)

        layout_principal.addLayout(layout_central)
        layout_principal.addLayout(rodape)

        self.setLayout(layout_principal)
        self.atualizar_lista()
    # =====================================================
    # IMAGEM
    # =====================================================
    def carregar_imagem(self):
        arq, _ = QFileDialog.getOpenFileName(
            self, "Select Image", self.pasta_imagens,
            "Images (*.png *.jpg *.jpeg *.tif)"
        )
        if not arq:
            return

        self.imagem_path = arq
        self.img_original = cv2.imread(arq)
        self.pontos_display = []
        self.preparar_imagem()

    def preparar_imagem(self):
        h, w, _ = self.img_original.shape
        lw, lh = self.lbl_img.width(), self.lbl_img.height()

        self.escala = min(lw / w, lh / h)
        nw, nh = int(w * self.escala), int(h * self.escala)

        self.img_display = cv2.resize(self.img_original, (nw, nh))
        self.offset_x = (lw - nw) // 2
        self.offset_y = (lh - nh) // 2

        self.lbl_img.mousePressEvent = self.registrar_clique
        self.atualizar_display()

    def registrar_clique(self, event):
        x = int(event.position().x()) - self.offset_x
        y = int(event.position().y()) - self.offset_y

        if not (0 <= x < self.img_display.shape[1] and 0 <= y < self.img_display.shape[0]):
            return

        if self.modo_edicao:
            d = [np.linalg.norm(np.array(p) - np.array((x, y))) for p in self.pontos_display]
            self.ponto_selecionado = int(np.argmin(d))
            self.lbl_info.setText(f"Point {self.ponto_selecionado + 1} selected")
        else:
            self.pontos_display.append((x, y))

        self.atualizar_display()

    def atualizar_display(self):
        if self.img_display is None:
            return

        img = self.img_display.copy()

        for i, p in enumerate(self.pontos_display):
            cor = (0, 255, 255) if i == self.ponto_selecionado else (0, 0, 255)
            cv2.circle(img, p, 4, cor, -1)

        for i in range(len(self.pontos_display) - 1):
            cv2.line(img, self.pontos_display[i], self.pontos_display[i + 1], (255, 0, 0), 2)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, _ = img_rgb.shape

        self.lbl_img.setPixmap(QPixmap.fromImage(
            QImage(img_rgb.data, w, h, 3 * w, QImage.Format_RGB888)
        ))





    
    # =====================================================
    # LISTA
    # =====================================================
    def atualizar_lista(self):
        self.lista.clear()
        p = self.combo_ponto.currentText()

        for i, mp in enumerate(self.microplasticos):
            if mp["ponto"] != p:
                continue

            area = mp.get("area_um2")
            area_txt = f"{area:.1f} µm²" if area else "—"
            cor = mp.get("cor", "—")

            self.lista.addItem(
                f"{i} | {mp['imagem']} | {mp['tipo']} | {cor} | "
                f"{mp['comprimento_um']:.1f} µm | {area_txt}"
            )

    def carregar_microplastico(self, item):
        idx = int(item.text().split("|")[0])
        mp = self.microplasticos[idx]

        caminho = os.path.join(self.pasta_imagens, mp["imagem"])
        if not os.path.exists(caminho):
            QMessageBox.warning(self, "Error", "Image file not found.")
            return

        self.img_original = cv2.imread(caminho)
        self.imagem_path = caminho

        self.combo_ponto.setCurrentText(mp["ponto"])
        self.combo_tipo.setCurrentText(mp["tipo"])
        self.combo_objetiva.setCurrentText(mp["objetiva"])

        if "cor" in mp:
            self.combo_cor.setCurrentText(mp["cor"])

        self.preparar_imagem()

        self.pontos_display = [
            (int(x * self.escala), int(y * self.escala))
            for x, y in mp["pontos_px"]
        ]

        self.modo_edicao = False
        self.ponto_selecionado = None
        self.atualizar_display()

    # =====================================================
    # SALVAR MICROPLÁSTICO
    # =====================================================
    def salvar_microplastico(self):
        if len(self.pontos_display) < 2:
            return

        pontos_reais = [(x / self.escala, y / self.escala) for x, y in self.pontos_display]

        comprimento_px = sum(
            np.linalg.norm(np.array(pontos_reais[i + 1]) - np.array(pontos_reais[i]))
            for i in range(len(pontos_reais) - 1)
        )

        objetiva = self.combo_objetiva.currentText()
        fator = self.calibracoes[objetiva]["um_por_pixel"]
        comprimento_um = comprimento_px * fator

        area_um2 = None
        if self.poligono_fechado():
            area_um2 = self.calcular_area_microplastico()

        self.microplasticos.append({
            "ponto": self.combo_ponto.currentText(),
            "imagem": os.path.basename(self.imagem_path),
            "objetiva": objetiva,
            "tipo": self.combo_tipo.currentText(),
            "cor": self.combo_cor.currentText(),  # NOVA VARIÁVEL
            "pontos_px": pontos_reais,
            "comprimento_um": comprimento_um,
            "area_um2": area_um2
        })

        with open(self.caminho_micro, "w", encoding="utf-8") as f:
            json.dump(self.microplasticos, f, indent=4, ensure_ascii=False)

        self.atualizar_lista()
        self.pontos_display = []

    # =====================================================
    # CÁLCULOS
    # =====================================================
    def calcular_impa(self):
        calcular_impa_e_mp(self.pasta_projeto)
        QMessageBox.information(self, "OK", "IMPa-L computed.")

    def calcular_impa_area(self):
        calcular_impa_area(self.pasta_projeto)
        QMessageBox.information(self, "OK", "IMPa-A computed.")

    # =====================================================
    # POLÍGONO / ÁREA
    # =====================================================
    def poligono_fechado(self, tolerancia_px=5):
        if len(self.pontos_display) < 3:
            return False
        return np.linalg.norm(
            np.array(self.pontos_display[0]) -
            np.array(self.pontos_display[-1])
        ) <= tolerancia_px

    def calcular_area_microplastico(self):
        pontos_reais = [(x / self.escala, y / self.escala) for x, y in self.pontos_display]
        area = 0.0
        for i in range(len(pontos_reais)):
            x1, y1 = pontos_reais[i]
            x2, y2 = pontos_reais[(i + 1) % len(pontos_reais)]
            area += (x1 * y2 - x2 * y1)
        area_px2 = abs(area) / 2.0

        fator = self.calibracoes[self.combo_objetiva.currentText()]["um_por_pixel"]
        return area_px2 * (fator ** 2)

    # =====================================================
    # EXCLUIR
    # =====================================================
    def excluir_microplastico(self):
        item = self.lista.currentItem()
        if not item:
            QMessageBox.warning(self, "Warning", "Select a microplastic to delete.")
            return

        idx = int(item.text().split("|")[0])

        resp = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this microplastic?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resp != QMessageBox.Yes:
            return

        del self.microplasticos[idx]

        with open(self.caminho_micro, "w", encoding="utf-8") as f:
            json.dump(self.microplasticos, f, indent=4, ensure_ascii=False)

        self.pontos_display = []
        self.ponto_selecionado = None
        self.img_display = None
        self.lbl_img.setText("No image loaded.")

        self.atualizar_lista()

        QMessageBox.information(self, "Deleted", "Microplastic removed successfully.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.excluir_microplastico()

    # =====================================================
    # EDIÇÃO
    # =====================================================
    def entrar_edicao(self):
        item = self.lista.currentItem()
        if not item:
            return
        self.idx_editando = int(item.text().split("|")[0])
        self.modo_edicao = True
        self.lbl_info.setText("Editing mode active")

    def remover_ponto(self):
        if self.ponto_selecionado is None or len(self.pontos_display) <= 2:
            return
        del self.pontos_display[self.ponto_selecionado]
        self.ponto_selecionado = None
        self.atualizar_display()

    def salvar_edicao(self):
        if self.idx_editando is None:
            return

        mp = self.microplasticos[self.idx_editando]

        pontos_reais = [(x / self.escala, y / self.escala) for x, y in self.pontos_display]

        comprimento_px = sum(
            np.linalg.norm(np.array(pontos_reais[i + 1]) - np.array(pontos_reais[i]))
            for i in range(len(pontos_reais) - 1)
        )

        fator = self.calibracoes[mp["objetiva"]]["um_por_pixel"]

        mp["pontos_px"] = pontos_reais
        mp["comprimento_um"] = comprimento_px * fator
        mp["cor"] = self.combo_cor.currentText()

        if self.poligono_fechado():
            mp["area_um2"] = self.calcular_area_microplastico()

        with open(self.caminho_micro, "w", encoding="utf-8") as f:
            json.dump(self.microplasticos, f, indent=4, ensure_ascii=False)

        self.modo_edicao = False
        self.ponto_selecionado = None
        self.atualizar_lista()
        self.lbl_info.setText("Changes saved")

    def cancelar_edicao(self):
        self.modo_edicao = False
        self.ponto_selecionado = None
        self.lbl_info.setText("Normal mode")







