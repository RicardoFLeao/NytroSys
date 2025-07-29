from PyQt6.QtWidgets import QPushButton, QTabWidget
from estilo import cores
from PyQt6.QtGui import QIcon

exem = {
    "cor1": "#01050D",
    "cor2": "#030C26",
    "cor3": "#031740",
    "cor4": "#364959",
    "cor5": "#70818C",
    "branco": "#FFFFFF"
}

# BOTÃO DE PESQUISA - PADRÃO 
def botao_pesquisa():
    botao = QPushButton("F8 - Pesquisar")
    botao.setIcon(QIcon("icons/pesquisar.png"))
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
            border: 1px solid #1e90ff;
            font-size: 14px;
        }
    """)

    botao.setFixedSize(130, 27)
    return botao

#TabWidget - PADRAO
def tabWidget():
    tabWidget = QTabWidget()
    tabWidget.setStyleSheet("""
    QTabBar::tab:first{
        margin-left: 6px;
    }
                    
    QTabBar::tab {
        background-color: #cbcdce;
        color: black;
        padding: 4px 10px;  /* ← Reduzido */
        margin-top: 2px;    /* ← Pode controlar altura geral */
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
    }
                            
    QTabBar::tab:selected {
        background-color: #82888a;
        font: bold;
    }
    QTabBar::tab:!selected{
        margin-top: 8px}
""")
    return tabWidget

#BOTÃO SAIR - PADRÃO
def botao_sair():
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

#BOTÃO SALVAR - PADRÃO
def botao_salvar():
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

