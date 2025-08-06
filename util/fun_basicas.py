from PyQt6.QtWidgets import QApplication, QLineEdit
from PyQt6.QtCore import Qt
import requests


def centralizar_tela(widget):
    widget.move(QApplication.primaryScreen(
    ).availableGeometry().center() - widget.rect().center())


def consulta_cep(cep: str) -> dict | None:
    cep = ''.join(filter(str.isdigit, cep))
    if len(cep) != 8:
        return None

    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
        if response.status_code == 200:
            dados = response.json()
            if "erro" in dados:
                return None
            return dados
    except requests.exceptions.RequestException:
        return {}  # Sem internet, retorna dicionário vazio

    return None


class LineEditComEnter(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.focusNextChild()
        else:
            super().keyPressEvent(event)
