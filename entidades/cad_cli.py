import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtCore import Qt
from util.padrao import (
    criar_botao,
    criar_tab_widget,
    criar_botao_sair,
    criar_botao_salvar,
    criar_label_padrao,
    criar_combobox_padrao,
    criar_lineedit_padrao
)
from util.estilo import gerar_estilo

class CadCliente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro Clientes")
        
        # Ícone seguro com verificação de caminho
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagens', 'icone.png'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"[ERRO] Ícone não encontrado: {icon_path}")


        self.componentes()

        self.showMaximized()

        # teclas atalhos
        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)

    def componentes(self):
        nometela = QLabel("Cadastro Clientes")
        nometela.setStyleSheet("color: orange; font-size:38px; font: bold")

        tab = criar_tab_widget()

        # ----------- ABA 1 (Consulta) ------------
        aba1 = QWidget()
        aba1.setStyleSheet('background-color: #cbcdce;')

        label_opc = criar_label_padrao()
        label_opc.setText('Opções')
        label_opc.setContentsMargins(2, 0, 0, 0)
        label_opc.setFixedSize(label_opc.sizeHint())

        comb_opc = criar_combobox_padrao()
        comb_opc.addItem("Nome")
        comb_opc.setFixedWidth(220)

        label_mdl = criar_label_padrao()
        label_mdl.setText('Modelo')
        label_mdl.setContentsMargins(2, 0, 0, 0)
        label_mdl.setFixedSize(label_mdl.sizeHint())

        comb_mdl = criar_combobox_padrao()
        comb_mdl.addItem('Iniciar com...')
        comb_mdl.setFixedWidth(220)

        label_pesq = criar_label_padrao()
        label_pesq.setText('Dados a pesquisar')
        label_pesq.setContentsMargins(2, 0, 0, 0)
        label_pesq.setFixedSize(label_pesq.sizeHint())

        check_todos = QCheckBox("Todos")

        lnedit_pesq = criar_lineedit_padrao()
        lnedit_pesq.setFixedWidth(810)

        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_opc.addWidget(comb_opc, alignment=Qt.AlignmentFlag.AlignLeft)

        vbox_mdl = QVBoxLayout()
        vbox_mdl.addWidget(label_mdl, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_mdl.addWidget(comb_mdl, alignment=Qt.AlignmentFlag.AlignLeft)

        hbox_pesq = QHBoxLayout()
        hbox_pesq.addWidget(label_pesq, alignment=Qt.AlignmentFlag.AlignLeft)
        hbox_pesq.addWidget(check_todos, alignment=Qt.AlignmentFlag.AlignRight)

        vbox_pesq = QVBoxLayout()
        vbox_pesq.addLayout(hbox_pesq)
        vbox_pesq.addWidget(lnedit_pesq, alignment=Qt.AlignmentFlag.AlignLeft)

        hbox_linha1 = QHBoxLayout()
        hbox_linha1.addLayout(vbox_opc)
        hbox_linha1.addLayout(vbox_mdl)
        hbox_linha1.addLayout(vbox_pesq)

        label_ativo = criar_label_padrao()
        label_ativo.setText('Ativo')
        label_ativo.setContentsMargins(2, 0, 0, 0)
        label_ativo.setFixedSize(label_ativo.sizeHint())

        combo_ativo = criar_combobox_padrao()
        combo_ativo.addItems(["Todos", "Ativo", "Inativo"])
        combo_ativo.setFixedWidth(220)

        btn_pesq = criar_botao()
        btn_pesq.setText("F8 - Pesquisa")
        btn_pesq.clicked.connect(self.preencher_tabela)  # chama função ao clicar

        hbox_linha2 = QHBoxLayout()
        hbox_linha2.addWidget(combo_ativo, alignment=Qt.AlignmentFlag.AlignLeft)
        hbox_linha2.addWidget(btn_pesq)

        vbox_linha2 = QVBoxLayout()
        vbox_linha2.addWidget(label_ativo, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_linha2.addLayout(hbox_linha2)

        # ---------- TABELA DE RESULTADOS ----------
        self.tabela_resultado = QTableWidget()
        self.tabela_resultado.setColumnCount(4)
        self.tabela_resultado.setHorizontalHeaderLabels(["Código", "Nome", "Cargo", "Status"])
        self.tabela_resultado.setStyleSheet("background-color: white; font-size: 13px")
        self.tabela_resultado.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_resultado.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_resultado.setAlternatingRowColors(True)
        self.tabela_resultado.setMaximumHeight(350)
        self.tabela_resultado.setMinimumHeight(300)
        

        #botões controle novo, relatório

        botao_novo = criar_botao()
        botao_novo.setText('F5 - Novo')

        botao_relat = criar_botao()
        botao_relat.setText('Relatórios')

        hbox_botoes_rodape = QHBoxLayout()
        hbox_botoes_rodape.setAlignment(Qt.AlignmentFlag.AlignCenter )
        hbox_botoes_rodape.addWidget(botao_novo)
        hbox_botoes_rodape.addSpacing(5)
        hbox_botoes_rodape.addWidget(botao_relat)
        hbox_botoes_rodape.addStretch()


        layout_geral_aba1 = QVBoxLayout()
        layout_geral_aba1.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba1.addLayout(hbox_linha1)
        layout_geral_aba1.addLayout(vbox_linha2)
        layout_geral_aba1.addWidget(self.tabela_resultado)
        layout_geral_aba1.addStretch()
        layout_geral_aba1.addLayout(hbox_botoes_rodape)
        layout_geral_aba1.addStretch()

        aba1.setLayout(layout_geral_aba1)

        # ----------- ABA 2 (Cadastro) ------------
        aba2 = QWidget()
        aba2.setStyleSheet('background-color: #cbcdce;')

        #table cadastro de clientes

        table_cliente = criar_tab_widget()
        aba_cad = QWidget()
        aba_ref = QWidget()

        table_cliente.addTab(aba_cad, "Dados")
        table_cliente.addTab(aba_ref, 'Referências')

        table_cliente.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #444444;  /* borda mais escura */
            }
                                    
            QTabBar::tab {
            background-color: orange;
            color: black;
            padding: 4px 10px;
            margin-top: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
                                    
            QTabBar::tab:selected {
            background-color: orange;
            font: bold;
        }
            QTabBar::tab:!selected {
            margin-top: 8px;
        }
        """)

        vbox_tabs_cliente = QVBoxLayout()
        vbox_tabs_cliente.addWidget(table_cliente)
        vbox_tabs_cliente.setContentsMargins(20,20,20,20)

        aba2.setLayout(vbox_tabs_cliente)

        # ----------- Tabs ----------
        tab.addTab(aba1, "Consulta")
        tab.addTab(aba2, "Cadastro")

        # Botões parte inferior da tela
        btn_sair = criar_botao_sair()
        btn_sair.clicked.connect(self.sair)

        btn_salvar = criar_botao_salvar()

        hbox_botoes = QHBoxLayout()
        hbox_botoes.addStretch()
        hbox_botoes.addWidget(btn_sair)
        hbox_botoes.addSpacing(40)
        hbox_botoes.addWidget(btn_salvar)
        hbox_botoes.addStretch()

        # ----------- Layout Principal ----------
        vbox = QVBoxLayout()
        vbox.addWidget(nometela, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(tab)
        vbox.addLayout(hbox_botoes)
        vbox.setContentsMargins(110, 50, 110, 50)

        self.setLayout(vbox)

    def preencher_tabela(self):
        # Dados simulados
        dados = [
            ["1", "João da Silva", "Analista", "Ativo"],
            ["2", "Maria Souza", "Gerente", "Inativo"],
            ["3", "Carlos Oliveira", "Supervisor", "Ativo"]
        ]

        self.tabela_resultado.setRowCount(len(dados))

        for linha, dados_linha in enumerate(dados):
            for coluna, valor in enumerate(dados_linha):
                self.tabela_resultado.setItem(linha, coluna, QTableWidgetItem(valor))

    def sair(self):
        from entidades.tela_ent import TelaEntidades
        self.janela = TelaEntidades()
        self.janela.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = CadCliente()
    janela.show()
    sys.exit(app.exec())
