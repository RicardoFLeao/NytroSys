from PyQt6.QtWidgets import QPushButton, QTabWidget, QLabel, QComboBox, QLineEdit
from PyQt6.QtGui import QIcon, QFont

# Cores de exemplo (pode manter se estiver usando em outro lugar)
exem = {
    "cor1": "#01050D",
    "cor2": "#030C26",
    "cor3": "#031740",
    "cor4": "#364959",
    "cor5": "#70818C",
    "branco": "#FFFFFF"
}

# BOTÃO DE PESQUISA - PADRÃO 
def criar_botao():
    botao = QPushButton()
    botao.setStyleSheet("""
        QPushButton {
            background-color: white; 
            color: black;
            border-radius: 3px; 
            border: 1px solid #364959; 
            font-size: 12px;
            font-weight: normal;
        }
        QPushButton:hover {
            background-color: #e6f2ff;
            border: 1px solid #70818c;
            font-size: 14px;
        }
    """)
    botao.setFixedSize(130, 27)
    return botao

# TABWIDGET - PADRÃO
def criar_tab_widget():
    tabs = QTabWidget()
    tabs.setStyleSheet("""
        QTabBar::tab:first {
            margin-left: 6px;
        }
        QTabBar::tab {
            background-color: #cbcdce;
            color: black;
            padding: 4px 10px;
            margin-top: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        QTabBar::tab:selected {
            background-color: #cbcdce;
            font: bold;
        }
        QTabBar::tab:!selected {
            margin-top: 8px;
        }
    """)
    return tabs

# BOTÃO SAIR - PADRÃO
def criar_botao_sair():
    botao = QPushButton("ESC - Sair")
    botao.setStyleSheet("""
        QPushButton {
            background-color: #031740; 
            color: #FFFFFF;
            border-radius: 5px; 
            border: 2px solid #364959; 
            font-size: 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #ffe6e6;
            border: 1px solid #ff4d4d;
            color: black;
        }
    """)
    botao.setFixedSize(230, 70)
    return botao

# BOTÃO SALVAR - PADRÃO
def criar_botao_salvar():
    botao = QPushButton("F12 - Salvar")
    botao.setStyleSheet("""
        QPushButton {
            background-color: #031740; 
            color: #FFFFFF;
            border-radius: 5px; 
            border: 2px solid #364959; 
            font-size: 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e6ffe6;
            border: 1px solid #33cc33;
            color: black;
        }
    """)
    botao.setFixedSize(230, 70)
    return botao

# LABEL PADRÃO
def criar_label_padrao():
    lbl = QLabel("")
    lbl.setStyleSheet("font-size: 14px")
    return lbl

# COMBOBOX PADRÃO
def criar_combobox_padrao():
    cbx = QComboBox()
    cbx.setStyleSheet("background-color: white")
    return cbx

# LINEEDIT PADRÃO
def criar_lineedit_padrao(classe=QLineEdit):
    lnedit = classe()
    lnedit.setStyleSheet("background-color: white; color: black; font-size: 14px")
    return lnedit

