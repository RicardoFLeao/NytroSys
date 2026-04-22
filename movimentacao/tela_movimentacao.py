import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from util.estilo import gerar_estilo

class TelaMovimentacao(QWidget):
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

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)
        QShortcut(QKeySequence(Qt.Key.Key_B), self).activated.connect(self.tela_saida)


    def componentes(self):

        nometela = QLabel("Movimentações")
        nometela.setStyleSheet("color: orange; font-size:38px; font: bold")
        nometela.setContentsMargins(0, 30, 0, 10)


        self.botao_entrada = QPushButton('A - Entradas')
        self.botao_saida = QPushButton('B - Saídas')
        self.botao_os = QPushButton('C - Ordens de Serviços')
        self.botao_uti = QPushButton('D - Utilitários')
        self.botao_sair = QPushButton('ESC - Sair')

        botoes = [self.botao_entrada, self.botao_saida, self.botao_os, self.botao_uti, self.botao_sair]

        
        for botao in botoes:
            botao.setFixedSize(350, 90)

        # ligações funções nos botões
        self.botao_saida.clicked.connect(self.tela_saida)
        self.botao_sair.clicked.connect(self.sair)

        vbox_botoes = QVBoxLayout()
        vbox_botoes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox_botoes.addWidget(self.botao_entrada)
        vbox_botoes.addSpacing(20)
        vbox_botoes.addWidget(self.botao_saida)
        vbox_botoes.addSpacing(20)
        vbox_botoes.addWidget(self.botao_os)
        vbox_botoes.addSpacing(20)
        vbox_botoes.addWidget(self.botao_uti)
        vbox_botoes.addSpacing(20)
        vbox_botoes.addWidget(self.botao_sair)

        layout_geral = QVBoxLayout()
        layout_geral.setContentsMargins(0, 10, 0, 30)
        layout_geral.addWidget(nometela, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_geral.addLayout(vbox_botoes)
        layout_geral.addStretch()  # Agora empurra o final pra baixo

        self.setLayout(layout_geral)

    def sair(self):
        from telaMain import telaPrincipal
        self.janela = telaPrincipal()
        self.janela.show()
        self.close()

    def tela_saida(self):
        from movimentacao.saida.tela_saida import TelaSaida
        self.janela = TelaSaida(self)
        self.janela.show()
        self.hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = TelaMovimentacao()
    janela.show()
    sys.exit(app.exec())
