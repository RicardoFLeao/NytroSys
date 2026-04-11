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


def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    # 1º dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma * 10 % 11) % 10

    # 2º dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{dig1}{dig2}"


def validar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6] + pesos1

    # 1º dígito
    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    resto = soma % 11
    dig1 = 0 if resto < 2 else 11 - resto

    # 2º dígito
    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    resto = soma % 11
    dig2 = 0 if resto < 2 else 11 - resto

    return cnpj[-2:] == f"{dig1}{dig2}"