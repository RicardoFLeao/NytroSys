from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QMenuBar, QMenu
from PyQt6.QtGui import QAction,  QShortcut, QKeySequence
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from util.estilo import gerar_estilo
from util.fun_telas import tela_ent, tela_cad_fun, tela_cad_cli, tela_cad_for
import sys


class telaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nitro Sys')
        self.setGeometry(QApplication.primaryScreen().availableGeometry())
        self.setWindowIcon(QIcon('imagens/icone.png'))
        self.showMaximized()
        self.menu()
        self.conteudo()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.close)
        QShortcut(QKeySequence(Qt.Key.Key_B), self).activated.connect(lambda: tela_ent(self))


    def menu(self):
        barra_menu = QMenuBar()
        self.setMenuBar(barra_menu)

        menu_prod = QMenu('Ad. Produtos', self)
        menu_enti = QMenu('Cad. Entidades', self)
        menu_fina = QMenu('Financeiro', self)
        menu_movi = QMenu('Movimentação', self)
        menu_cont = QMenu('Contabilidade', self)
        menu_util = QMenu('Utilitários', self)

        barra_menu.addMenu(menu_prod)
        barra_menu.addMenu(menu_enti)
        barra_menu.addMenu(menu_fina)
        barra_menu.addMenu(menu_movi)
        barra_menu.addMenu(menu_cont)
        barra_menu.addMenu(menu_util)

        act_func = QAction('Cad. Funcionários', self)
        act_clie = QAction('Cad. Clientes', self)
        act_forn = QAction('Cad. Fornecedores', self)

        menu_enti.addAction(act_func)
        menu_enti.addSeparator()
        menu_enti.addAction(act_clie)
        menu_enti.addSeparator()
        menu_enti.addAction(act_forn)


        #ações dos menus
        act_func.triggered.connect(lambda: tela_cad_fun(self))
        act_clie.triggered.connect(lambda: tela_cad_cli(self))
        act_forn.triggered.connect(lambda: tela_cad_for(self))
        
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

        #Ações botões

        btnB.clicked.connect(lambda: tela_ent(self))

        bloco_notas = QTextEdit()
        bloco_notas.setPlaceholderText("bloco de notas...")
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
