from PyQt6.QtWidgets import QApplication, QLineEdit
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QDoubleValidator
import requests

class LineEditComEnter(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.focusNextChild()
        else:
            super().keyPressEvent(event)

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


def validador_preco():
    validador = QDoubleValidator(0.0, 999999.99, 2)
    validador.setNotation(QDoubleValidator.Notation.StandardNotation)
    validador.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
    return validador

def texto_para_float(texto):
    texto = texto.strip()

    if not texto:
        return 0.0

    # troca vírgula por ponto
    texto = texto.replace(",", ".")

    try:
        return float(texto)
    except ValueError:
        return 0.0

def formatar_preco(valor):
    return f"{valor:.2f}".replace(".", ",")