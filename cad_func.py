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

        # Layout principal
        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        # Cor do fundo geral (azul escuro)
        self.setStyleSheet("""
            QWidget {
                background-color: #01050D;
                color: white;
            }
        """)

        # Topo - Nome do sistema
        nome_sys = QLabel('Sys - Cadastro de Usuários')
        nome_sys.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nome_sys.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.layout_principal.addWidget(nome_sys)

        # Chama a criação da área branca com os campos
        self.criar_formulario()

    def criar_formulario(self):
        # Widget container branco
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #adb5ba;
                color: black;
                border-radius: 15px;
                padding: 20px;
            }
        """)

        grid = QGridLayout()

        # Exemplo de campos
        lb_nome = QLabel('NOME:')
        lb_nome.setStyleSheet("""
            background-color: white;
            font-weight: bold;
            padding: 2px 5px;  /* Ajuste fino da margem interna */
        """)
        lb_nome.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        txt_nome = QLineEdit()
        txt_nome.setStyleSheet('background-color: white; border: black')
        txt_nome.setFixedSize(450, 28)
        txt_nome.setFont(QFont('san-serif', 8))

        lb_email = QLabel('E-mail:')
        lb_email.setStyleSheet('background-color:white; font-weight: bold; ')
        txt_email = QLineEdit()
        txt_email.setStyleSheet('background-color:white; ')

        grid.addWidget(lb_nome, 0, 0)
        grid.addWidget(txt_nome, 0, 1)

        grid.addWidget(lb_email, 1, 0)
        grid.addWidget(txt_email, 1, 1)

        container.setLayout(grid)

        # Centralizar o container no meio da tela
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(container)
        hbox.addStretch()

        self.layout_principal.addLayout(hbox)


app = QApplication(sys.argv)
tela = tela_cad_func()
tela.show()
sys.exit(app.exec())
