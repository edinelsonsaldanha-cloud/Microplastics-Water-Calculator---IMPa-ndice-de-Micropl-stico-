import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
import matplotlib
matplotlib.use("QtAgg")


def main():
    app = QApplication(sys.argv)
    janela = MainWindow()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
