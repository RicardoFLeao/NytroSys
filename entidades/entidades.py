import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from util.estilo import gerar_estilo

class TelaEntidades(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Entidades')

        # Ícone seguro com verificação de caminho
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagens', 'icone.png'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"[ERRO] Ícone não encontrado: {icon_path}")

        self.componentes()
        self.showMaximized()

        QShortcut(QKeySequence(Qt.Key.Key_A), self).activated.connect(self.tela_funcionarios)
        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)

    def componentes(self):

        nometela = QLabel("Cadastro de Entidades")
        nometela.setStyleSheet("color: orange; font-size:38px; font: bold")
        nometela.setContentsMargins(0, 30, 0, 10)


        botao_fun = QPushButton('A - Funcionários')
        botao_cli = QPushButton('B - Clientes')
        botao_for = QPushButton('C - Fornecedores')
        botao_uti = QPushButton('D - Utilitários')
        botao_sair = QPushButton('ESC - Sair')

        botoes = [botao_fun, botao_cli, botao_for, botao_uti, botao_sair]

        for botao in botoes:
            botao.setFixedSize(350, 90)

        # ligações funções nos botões
        botao_fun.clicked.connect(self.tela_funcionarios)
        botao_sair.clicked.connect(self.sair)

        vbox_botoes = QVBoxLayout()
        vbox_botoes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox_botoes.addWidget(botao_fun)
        vbox_botoes.addSpacing(20)
        vbox_botoes.addWidget(botao_cli)
        vbox_botoes.addSpacing(20)
        vbox_botoes.addWidget(botao_for)
        vbox_botoes.addSpacing(20)
        vbox_botoes.addWidget(botao_uti)
        vbox_botoes.addSpacing(20)
        vbox_botoes.addWidget(botao_sair)

        layout_geral = QVBoxLayout()
        layout_geral.setContentsMargins(0, 10, 0, 30)
        layout_geral.addWidget(nometela, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_geral.addLayout(vbox_botoes)
        layout_geral.addStretch()  # Agora empurra o final pra baixo

        self.setLayout(layout_geral)

    def tela_funcionarios(self):
        from cad_fun import CadFuncionarios
        self.janela = CadFuncionarios()
        self.janela.show()
        self.close()

    def sair(self):
        from telaMain import telaPrincipal
        self.janela = telaPrincipal()
        self.janela.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = TelaEntidades()
    janela.show()
    sys.exit(app.exec())
