from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from util.funcoes_basicas import centralizar_tela
import sys

class tela_cad_func(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('imagens/nitro_sys2.png'))
        self.setWindowTitle('Cadastro Funcionarios')
        self.setFixedSize(1300, 730)
        centralizar_tela(self)

        # Layout principal (VBox)
        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        # Nome do sistema no topo
        nome_sys = QLabel('Sys - Cadastro Funcionários')
        nome_sys.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nome_sys.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        self.layout_principal.addWidget(nome_sys)
        self.layout_principal.addStretch()

        # Fundo da tela
        self.setStyleSheet("""
            QWidget {
                background-color: #01050D;
                color: white;
            }
        """)

        # Agora cria o bloco com os campos
        self.comp_cad_func()

    def comp_cad_func(self):
        # Container para o formulário
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
                border-radius: 15px;
                padding: 20px;
            }
        """)

        # Layout interno (Grid)
        comp = QGridLayout()

        lb_nome = QLabel('Nome:')
        txt_nome = QLineEdit()

        lb_email = QLabel('Email:')
        txt_email = QLineEdit()

        comp.addWidget(lb_nome, 0, 0)
        comp.addWidget(txt_nome, 0, 1)
        comp.addWidget(lb_email, 1, 0)
        comp.addWidget(txt_email, 1, 1)

        container.setLayout(comp)

        # Centraliza o container dentro do VBox (opcional)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(container)
        hbox.addStretch()

        self.layout_principal.addLayout(hbox)

app = QApplication(sys.argv)  
tela = tela_cad_func()
tela.show()
sys.exit(app.exec())
