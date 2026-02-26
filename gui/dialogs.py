from PySide6.QtWidgets import QMessageBox


def erro(parent, titulo, mensagem):
    QMessageBox.critical(parent, titulo, mensagem)


def info(parent, titulo, mensagem):
    QMessageBox.information(parent, titulo, mensagem)


def aviso(parent, titulo, mensagem):
    QMessageBox.warning(parent, titulo, mensagem)
