from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence, QFont
from PyQt6.QtCore import Qt
from padrao import botao_pesquisa, tabWidget, botao_sair, botao_salvar
from estilo import gerar_estilo
import sys

class cad_funcionarios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro Funcionários")
        self.setWindowIcon(QIcon('imagens/icone.png'))
        # with open('estilo.css', 'r') as estilo:
        #     estilo_css = estilo.read()
        #     self.setStyleSheet(estilo_css)

        self.componentes()

        self.showMaximized()
        QShortcut(QKeySequence('Esc'), self).activated.connect(self.close)

    def componentes(self):
        nometela = QLabel("Cadastro Funcionários")
        nometela.setStyleSheet("color: orange; font-size:38px; font: bold")

        tab = tabWidget()

        # ----------- ABA 1 (Consulta) ------------
        aba1 = QWidget()
        aba1.setStyleSheet('background-color: #cbcdce;  ')

        label_ordem = QLabel('Ordenar por:')
        label_ordem.setFixedSize(label_ordem.sizeHint())

        comb_ordem = QComboBox()
        comb_ordem.addItem("Selecione")
        comb_ordem.model().item(0).setEnabled(False)
        comb_ordem.setStyleSheet('background-color: white; padding: 3px 10px')
        comb_ordem.setFixedWidth(220)

        label_pesq = QLabel('Pesquisar:')
        label_pesq.setFixedSize(label_pesq.sizeHint())

        lnedit_buscar = QLineEdit()
        lnedit_buscar.setFixedWidth(550)
        lnedit_buscar.setStyleSheet('background-color: white; padding: 3px 10px 3px 10px')

        btn_pesq = botao_pesquisa()

        hbox_consulta = QHBoxLayout()
        hbox_consulta.addWidget(label_ordem)
        hbox_consulta.addWidget(comb_ordem)
        hbox_consulta.addWidget(label_pesq)
        hbox_consulta.addWidget(lnedit_buscar)
        hbox_consulta.addWidget(btn_pesq)

        layout_geral_aba1 = QVBoxLayout()
        layout_geral_aba1.setContentsMargins(10, 30, 0, 0)  # margem esquerda e topo
        layout_geral_aba1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba1.addLayout(hbox_consulta)

        aba1.setLayout(layout_geral_aba1)

        # ----------- ABA 2 (Cadastro) ------------
        aba2 = QWidget()
        aba2.setStyleSheet('background-color: #cbcdce;')

        # ----------- Tabs ----------
        tab.addTab(aba1, "Consulta")
        tab.addTab(aba2, "Cadastro")

        # ----------- Botões ----------
        btn_sair = botao_sair()
        btn_sair.clicked.connect(self.sair)

        btn_salvar = botao_salvar()

        hbox = QHBoxLayout()
        hbox.addWidget(btn_sair)
        hbox.addWidget(btn_salvar)

        # ----------- Layout Principal ----------
        vbox = QVBoxLayout()
        vbox.addWidget(nometela, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(tab)
        vbox.addLayout(hbox)
        vbox.setContentsMargins(30, 50, 30, 50)

        self.setLayout(vbox)

    def sair(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = cad_funcionarios()
    janela.show()
    sys.exit(app.exec())
