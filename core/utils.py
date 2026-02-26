import sys
import os

def resource_path(relative_path):
    """
    Retorna o caminho correto tanto no .py quanto no .exe
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
