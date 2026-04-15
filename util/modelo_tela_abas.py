

# tela salva somente como modelo para futuras telas 


from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
)
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtCore import Qt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.estilo import gerar_estilo
from util.padrao import (
    criar_botao,
    criar_tab_widget,
    criar_label_padrao,
    criar_combobox_padrao,
    criar_lineedit_padrao,
)


class TelaMarcaProd(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Marca dos Produto')
        self.setWindowIcon(QIcon('imagens/icone.png'))
        self.setFixedSize(800,600)
        self.componentes()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)
        QShortcut(QKeySequence('F5'), self).activated.connect(self.novo)

    def componentes(self):
        nometela = QLabel('Marca dos Produtos')
        nometela.setStyleSheet('color: orange; font-size: 38px; font: bold;')

        self.tab = criar_tab_widget()

        # aba 1 consulta
        aba1 = QWidget()
        aba1.setStyleSheet('background-color: #cbcdce;')

        label_opc = criar_label_padrao()
        label_opc.setText('Opções')
        label_opc.setContentsMargins(2, 0, 0, 0)
        label_opc.setFixedSize(label_opc.sizeHint())

        self.comb_opc = criar_combobox_padrao()
        self.comb_opc.addItems(['Descrição', 'Código'])
        self.comb_opc.setFixedWidth(220)

        label_pesq = criar_label_padrao()
        label_pesq.setText('Dados a pesquisar')
        label_pesq.setContentsMargins(2, 0, 0, 0)
        label_pesq.setFixedSize(label_pesq.sizeHint())

        self.edit_pesq = criar_lineedit_padrao()
        self.edit_pesq.setMinimumWidth(300)


        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc)
        vbox_opc.addWidget(self.comb_opc)

        vbox_pesq = QVBoxLayout()
        vbox_pesq.addWidget(label_pesq)
        vbox_pesq.addWidget(self.edit_pesq)

        hbox_linha1 = QHBoxLayout()
        hbox_linha1.addLayout(vbox_opc)
        hbox_linha1.addLayout(vbox_pesq)


        self.combo_ativo = criar_combobox_padrao()
        self.combo_ativo.addItems(["Ativo", "Excluido", "Todos"])
        self.combo_ativo.setFixedWidth(220)

        vbox_ativo = QVBoxLayout()
        vbox_ativo.addWidget(self.combo_ativo)

        hbox_linha2 = QHBoxLayout()
        hbox_linha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_linha2.addLayout(vbox_ativo)


        self.tabela_resultado = QTableWidget()
        self.tabela_resultado.setColumnCount(3)
        self.tabela_resultado.setHorizontalHeaderLabels(['Código', 'Descrição', 'Status'])
        self.tabela_resultado.setStyleSheet('''
            QTableWidget {
                background-color: white;
                font-size: 13px;
            }

            QTableWidget::item:selected {
                background-color: #031740;
                color: white;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 5px;
            }
        ''')
        self.tabela_resultado.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_resultado.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_resultado.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabela_resultado.setAlternatingRowColors(True)
        self.tabela_resultado.setMinimumHeight(300)
        self.tabela_resultado.verticalHeader().setVisible(False)

        header = self.tabela_resultado.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.tabela_resultado.setColumnWidth(2, 80)

        self.botao_novo = criar_botao()
        self.botao_novo.setText('F5 - Novo')
        self.botao_novo.clicked.connect(self.novo)

        # self.botao_salvar = criar_botao()
        # self.botao_salvar.setText('Salvar')
        # self.botao_salvar.clicked.connect(self.salvar)

        # self.botao_excluir = criar_botao()
        # self.botao_excluir.setText('Excluir')
        # self.botao_excluir.clicked.connect(self.excluir)

        self.botao_sair = criar_botao()
        self.botao_sair.setText('Sair')
        self.botao_sair.clicked.connect(self.sair)

        hbox_botoes_rodape = QHBoxLayout()
        hbox_botoes_rodape.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_botoes_rodape.addWidget(self.botao_novo)
        hbox_botoes_rodape.addSpacing(5)
        hbox_botoes_rodape.addWidget(self.botao_sair)

        layout_geral_aba1 = QVBoxLayout()
        layout_geral_aba1.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba1.addLayout(hbox_linha1)
        layout_geral_aba1.addLayout(hbox_linha2)
        layout_geral_aba1.addWidget(self.tabela_resultado)
        layout_geral_aba1.addSpacing(10)
        layout_geral_aba1.addLayout(hbox_botoes_rodape)
        layout_geral_aba1.addSpacing(10)

        aba1.setLayout(layout_geral_aba1)

        # aba 2 cadastro vazia por enquanto
        aba2 = QWidget()
        aba2.setStyleSheet('background-color: #cbcdce;')

        layout_geral_aba2 = QVBoxLayout()
        layout_geral_aba2.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba2.addStretch()
        aba2.setLayout(layout_geral_aba2)

        self.tab.addTab(aba1, 'Consulta')
        self.tab.addTab(aba2, 'Cadastro')

        vbox = QVBoxLayout()
        vbox.addWidget(nometela, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        vbox.addWidget(self.tab)
        vbox.setContentsMargins(20, 20, 20, 20)

        self.setLayout(vbox)

    def novo(self):
        self.tab.setCurrentIndex(1)

    def salvar(self):
        pass

    def excluir(self):
        pass

    def sair(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = TelaMarcaProd()
    janela.show()
    sys.exit(app.exec())
