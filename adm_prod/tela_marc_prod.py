import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '','..')))

from adm_prod.marca_service import MarcaService
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QCheckBox,
)

from PyQt6.QtGui import QIcon, QShortcut, QKeySequence, QColor
from PyQt6.QtCore import Qt

from util.estilo import gerar_estilo
from util.padrao import (
    criar_botao,
    criar_tab_widget,
    criar_label_padrao,
    criar_combobox_padrao,
    criar_lineedit_padrao,
)
from util.fun_basicas import LineEditComEnter


class TelaMarcaProd(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Marca dos Produtos')
        self.setWindowIcon(QIcon('imagens/icone.png'))
        self.setFixedSize(800,600)
        self.service = MarcaService()
        self.status_marca_atual = "A"
        self.componentes()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)
        QShortcut(QKeySequence('F5'), self).activated.connect(self.novo)
        self.tabela_resultado.setRowCount(0)

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

        self.cheque_todos = QCheckBox('Todos')

        self.edit_pesq = criar_lineedit_padrao()
        self.edit_pesq.setMinimumWidth(300)
        self.edit_pesq.textChanged.connect(self.pesquisar_digito)

        hbox_pesquisa = QHBoxLayout()
        hbox_pesquisa.addWidget(label_pesq)
        hbox_pesquisa.addStretch()
        hbox_pesquisa.addWidget(self.cheque_todos)

        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc)
        vbox_opc.addWidget(self.comb_opc)

        vbox_pesq = QVBoxLayout()
        vbox_pesq.addLayout(hbox_pesquisa)
        vbox_pesq.addWidget(self.edit_pesq)

        hbox_linha1 = QHBoxLayout()
        hbox_linha1.addLayout(vbox_opc)
        hbox_linha1.addLayout(vbox_pesq)


        self.combo_ativo = criar_combobox_padrao()
        self.combo_ativo.addItems(["Ativo", "Excluído", "Todos"])
        self.combo_ativo.setFixedWidth(220)

        self.btn_pesquisar = criar_botao()
        self.btn_pesquisar.setText('F8 - Pesquisar')
        self.btn_pesquisar.clicked.connect(self.pesquisar)
        
        hbox_ativo = QHBoxLayout()
        hbox_ativo.addWidget(self.combo_ativo)
        hbox_ativo.addStretch()
        hbox_ativo.addWidget(self.btn_pesquisar)

        hbox_linha2 = QHBoxLayout()
        hbox_linha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_linha2.addLayout(hbox_ativo)


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

        self.botao_alterar = criar_botao()
        self.botao_alterar.setText('Alterar')
        self.botao_alterar.clicked.connect(self.alterar)

        self.botao_sair = criar_botao()
        self.botao_sair.setText('Sair')
        self.botao_sair.clicked.connect(self.sair)

        hbox_botoes_rodape = QHBoxLayout()
        hbox_botoes_rodape.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_botoes_rodape.addWidget(self.botao_novo)
        hbox_botoes_rodape.addSpacing(5)
        hbox_botoes_rodape.addWidget(self.botao_alterar)
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

        cod_marca = criar_label_padrao()
        cod_marca.setText('Código')
        cod_marca.setContentsMargins(2, 0, 0, 0)
        cod_marca.setFixedSize(cod_marca.sizeHint())

        self.edit_cod_marca = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cod_marca.setFixedWidth(90)
        self.edit_cod_marca.setReadOnly(True)

        vbox_cod_marca = QVBoxLayout()
        vbox_cod_marca.addWidget(cod_marca)
        vbox_cod_marca.addWidget(self.edit_cod_marca)

        desc_marca = criar_label_padrao()
        desc_marca.setText('Descrição')
        desc_marca.setContentsMargins(2, 0, 0, 0)
        desc_marca.setFixedSize(desc_marca.sizeHint())

        self.edit_desc_marca = criar_lineedit_padrao()
        self.edit_desc_marca.setMinimumWidth(300)

        vbox_desc_marca = QVBoxLayout()
        vbox_desc_marca.addWidget(desc_marca)
        vbox_desc_marca.addWidget(self.edit_desc_marca)

        hbox_cad_marca_linha_1 = QHBoxLayout()
        hbox_cad_marca_linha_1.addLayout(vbox_cod_marca)
        hbox_cad_marca_linha_1.addLayout(vbox_desc_marca)

        self.botao_salvar = criar_botao()
        self.botao_salvar.setText('Salvar')
        self.botao_salvar.clicked.connect(self.salvar)

        self.botao_excluir = criar_botao()
        self.botao_excluir.setText('Excluir')
        self.botao_excluir.clicked.connect(self.excluir)

        self.botao_sair_cadastro = criar_botao()
        self.botao_sair_cadastro.setText('Sair')
        self.botao_sair_cadastro.clicked.connect(self.sair)

        hbox_botoes_cadastro = QHBoxLayout()
        hbox_botoes_cadastro.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_botoes_cadastro.addWidget(self.botao_salvar)
        hbox_botoes_cadastro.addSpacing(5)
        hbox_botoes_cadastro.addWidget(self.botao_excluir)
        hbox_botoes_cadastro.addSpacing(5)
        hbox_botoes_cadastro.addWidget(self.botao_sair_cadastro)

        layout_geral_aba2 = QVBoxLayout()
        layout_geral_aba2.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba2.addLayout(hbox_cad_marca_linha_1)
        layout_geral_aba2.addStretch()
        layout_geral_aba2.addLayout(hbox_botoes_cadastro)
        layout_geral_aba2.addSpacing(10)

        aba2.setLayout(layout_geral_aba2)

        self.tab.addTab(aba1, 'Consulta')
        self.tab.addTab(aba2, 'Cadastro')

        vbox = QVBoxLayout()
        vbox.addWidget(nometela, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        vbox.addWidget(self.tab)
        vbox.setContentsMargins(20, 20, 20, 20)

        self.setLayout(vbox)

    def novo(self):
        self.edit_cod_marca.clear()
        self.edit_desc_marca.clear()
        self.status_marca_atual = "A"
        self.botao_excluir.setText("Excluir")
        self.tab.setCurrentIndex(1)
        self.edit_desc_marca.setFocus()

    def salvar(self):
        codigo = self.edit_cod_marca.text().strip()
        nome = self.edit_desc_marca.text().strip()

        if codigo:
            resultado = self.service.atualizar_marca(codigo, nome)
        else:
            resultado = self.service.salvar_marca(nome)

        if resultado["sucesso"]:
            QMessageBox.information(self, "Sucesso", resultado["mensagem"])
            self.edit_cod_marca.clear()
            self.edit_desc_marca.clear()

            self.status_marca_atual = "A"
            self.botao_excluir.setText("Excluir")

            self.tab.setCurrentIndex(0)
            self.preencher_tabela()
        else:
            QMessageBox.warning(self, "Aviso", resultado["mensagem"])
            self.edit_desc_marca.setFocus()
        
    def preencher_tabela(self, status_filtro=None):
        texto = self.edit_pesq.text().strip()
        opcao = self.comb_opc.currentText()

        if status_filtro is None:
            if self.cheque_todos.isChecked():
                status_filtro = "Todos"
            else:
                status_filtro = self.combo_ativo.currentText()

        dados = self.service.listar_marcas(texto, opcao, status_filtro)

        self.tabela_resultado.setRowCount(len(dados))

        for linha, marca in enumerate(dados):
            codigo = str(marca["codigo"])
            nome = str(marca["nome"])
            status = str(marca["status"])

            if status == "A":
                status_texto = "Ativo"
            else:
                status_texto = "Excluído"

            item_codigo = QTableWidgetItem(codigo)
            item_nome = QTableWidgetItem(nome)
            item_status = QTableWidgetItem(status_texto)

            if status_texto == "Excluído":
                item_status.setForeground(QColor("red"))

            self.tabela_resultado.setItem(linha, 0, item_codigo)
            self.tabela_resultado.setItem(linha, 1, item_nome)
            self.tabela_resultado.setItem(linha, 2, item_status)


    def excluir(self):
        codigo = self.edit_cod_marca.text().strip()

        if not codigo:
            QMessageBox.warning(self, "Aviso", "Nenhuma marca carregada.")
            return

        if self.status_marca_atual == "A":
            acao = "excluir"
        else:
            acao = "ativar"

        msg = QMessageBox(self)
        msg.setWindowTitle("Confirmar")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText(f"Deseja {acao} a marca código {codigo}?")

        btn_sim = msg.addButton("Sim", QMessageBox.ButtonRole.YesRole)
        btn_nao = msg.addButton("Não", QMessageBox.ButtonRole.NoRole)

        msg.setDefaultButton(btn_nao)
        msg.exec()

        if msg.clickedButton() != btn_sim:
            return

        resultado = self.service.alterar_status_marca(codigo, self.status_marca_atual)

        if resultado["sucesso"]:
            QMessageBox.information(self, "Sucesso", resultado["mensagem"])
            self.edit_cod_marca.clear()
            self.edit_desc_marca.clear()
            self.status_marca_atual = "A"
            self.botao_excluir.setText("Excluir")
            self.tab.setCurrentIndex(0)
            self.preencher_tabela()
        else:
            QMessageBox.warning(self, "Aviso", resultado["mensagem"])


    def pesquisar_digito(self):
        texto = self.edit_pesq.text().strip()

        # se não digitou nada → não busca
        if not texto:
            self.tabela_resultado.setRowCount(0)
            return

        # se marcou "Todos"
        if self.cheque_todos.isChecked():
            status_filtro = "Todos"
        else:
            status_filtro = self.combo_ativo.currentText()

        self.preencher_tabela(status_filtro=status_filtro)

    def alterar(self):
        linha = self.tabela_resultado.currentRow()

        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma marca na tabela.")
            return

        item_codigo = self.tabela_resultado.item(linha, 0)
        item_nome = self.tabela_resultado.item(linha, 1)
        item_status = self.tabela_resultado.item(linha, 2)

        if item_codigo is None or item_nome is None or item_status is None:
            QMessageBox.warning(self, "Aviso", "Não foi possível carregar a marca.")
            return

        self.edit_cod_marca.setText(item_codigo.text().strip())
        self.edit_desc_marca.setText(item_nome.text().strip())

        status_texto = item_status.text().strip()

        if status_texto == "Ativo":
            self.status_marca_atual = "A"
            self.botao_excluir.setText("Excluir")
        else:
            self.status_marca_atual = "E"
            self.botao_excluir.setText("Ativar")

        self.tab.setCurrentIndex(1)
        self.edit_desc_marca.setFocus()


    def pesquisar(self):
        texto = self.edit_pesq.text().strip()

        if self.cheque_todos.isChecked():
            status_filtro = "Todos"
        else:
            status_filtro = self.combo_ativo.currentText()

      
        self.preencher_tabela(status_filtro=status_filtro)


    def sair(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = TelaMarcaProd()
    janela.show()
    sys.exit(app.exec())
