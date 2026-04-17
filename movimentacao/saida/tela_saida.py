import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence

from util.estilo import gerar_estilo


class TelaSaida(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Saída')

        self.componentes()
        self.showMaximized()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)
    def componentes(self):

        titulo = QLabel("Saídas")
        titulo.setStyleSheet("color: orange; font-size:38px; font: bold")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFixedHeight(50)

        self.quadro = QFrame()
        self.quadro.setStyleSheet("""
            QFrame {
                background-color: #d9d9d9;
                border-radius: 10px;
            }
        """)
        self.quadro.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.botao_venda = QPushButton("Vendas")
        self.botao_consultas = QPushButton("Consultas")
        self.botao_relatorios = QPushButton("Relatórios")
        self.botao_sair = QPushButton("ESC - Sair")

        self.botao_sair.clicked.connect(self.sair)

        botoes = [self.botao_venda, self.botao_consultas, self.botao_relatorios, self.botao_sair]

        for botao in botoes:
            botao.setFixedSize(180, 60)
            botao.setStyleSheet("""
                QPushButton {
                    background-color: #031740;
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: bold;
                    border: 2px solid #364956;
                    border-radius: 8px;
                }
                                
                QPushButton:hover {
                    background-color: #030C26;
                    font-size: 15px;
                }
            """)

        layout_botoes = QVBoxLayout()
        layout_botoes.setSpacing(20)
        layout_botoes.setContentsMargins(0, 0, 0, 0)
        layout_botoes.addWidget(self.botao_venda)
        layout_botoes.addWidget(self.botao_consultas)
        layout_botoes.addWidget(self.botao_relatorios)
        layout_botoes.addStretch()
        layout_botoes.addWidget(self.botao_sair)

        layout_quadro = QVBoxLayout()
        layout_quadro.setContentsMargins(0, 0, 0, 0)
        self.quadro.setLayout(layout_quadro)

        layout_centro = QHBoxLayout()
        layout_centro.setContentsMargins(0, 0, 0, 0)
        layout_centro.setSpacing(30)
        layout_centro.addLayout(layout_botoes, 0)
        layout_centro.addWidget(self.quadro, 1)

        layout_geral = QVBoxLayout()
        layout_geral.setContentsMargins(20, 10, 20, 20)
        layout_geral.setSpacing(10)
        layout_geral.addWidget(titulo, 0)
        layout_geral.addLayout(layout_centro, 1)

        self.setLayout(layout_geral)

    def sair(self):
        from movimentacao.tela_movimentacao import TelaMovimentacao
        self.janela = TelaMovimentacao()
        self.janela.show()
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(gerar_estilo())
    janela = TelaSaida()
    janela.show()
    sys.exit(app.exec())