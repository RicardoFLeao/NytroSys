from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QAction,  QShortcut, QKeySequence
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from estilo import gerar_estilo
import sys


class telaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        print(">>> telaPrincipal foi chamada!")  # ← TESTE CRÍTICO
        self.setWindowTitle('Nitro Sys')
        self.setGeometry(QApplication.primaryScreen().availableGeometry())
        self.setWindowIcon(QIcon('imagens/Nitro_sys2.png'))
        self.showMaximized()
        self.menu()
        self.conteudo()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.close)

    def menu(self):
        barra_menu = self.menuBar()

        barra_menu.addMenu('Ad. Produtos')
        barra_menu.addMenu('Cad. Entidades')
        barra_menu.addMenu('Financeiro')
        barra_menu.addMenu('Movimentação')
        barra_menu.addMenu('Contabilidade')
        barra_menu.addMenu('Utilitários')
        
        menu_sair = QAction('Sair', self)
        menu_sair.triggered.connect(self.close)
        barra_menu.addAction(menu_sair)

    def conteudo(self):
        conteudo = QWidget()
        layout_principal = QVBoxLayout()

        titulo = QLabel(
            '<span style="color: white;">Nitro </span><span style="color: #FFA500;">Sys</span>')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 75px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        layout_principal.addWidget(titulo)

        layout_horizontal = QHBoxLayout()
        layout_botoes = QGridLayout()
        layout_botoes.setHorizontalSpacing(60)
        layout_botoes.setVerticalSpacing(40)

        btnA = QPushButton('A - Administração de Produtos')
        btnB = QPushButton('B - Cadastro de Entidades')
        btnC = QPushButton('C - Financeiro')
        btnD = QPushButton('D - Movimentação')
        btnE = QPushButton('E - Contabilidade')
        btnF = QPushButton('F - Utilitários')

        botoes = [btnA, btnB, btnC, btnD, btnE, btnF]
        for botao in botoes:
            botao.setFixedSize(350, 90)

        layout_botoes.addWidget(btnA, 0, 0)
        layout_botoes.addWidget(btnD, 0, 1)
        layout_botoes.addWidget(btnB, 1, 0)
        layout_botoes.addWidget(btnE, 1, 1)
        layout_botoes.addWidget(btnC, 2, 0)
        layout_botoes.addWidget(btnF, 2, 1)

        bloco_notas = QTextEdit()
        bloco_notas.setPlaceholderText("bloco de notas para anotação...")
        bloco_notas.setFixedSize(400, 300)
        bloco_notas.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        layout_horizontal.setContentsMargins(50, 75, 50, 50)
        layout_horizontal.addLayout(layout_botoes)
        layout_horizontal.addSpacing(50)
        layout_horizontal.addWidget(bloco_notas)

        layout_principal.addLayout(layout_horizontal)
        layout_principal.addStretch()

        conteudo.setLayout(layout_principal)
        conteudo.setContentsMargins(0, 75, 0, 0)
        self.setCentralWidget(conteudo)


# Teste isolado (executar tela principal sem login)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    tela = telaPrincipal()
    tela.show()
    sys.exit(app.exec())
