import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView)
from bd import atualizar_quantidade_produto
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtCore import Qt
QHeaderView
from util.estilo import gerar_estilo
from util.padrao import (
    criar_botao,
    criar_botao_sair,
    criar_label_padrao,
    criar_lineedit_padrao,
    criar_tab_widget,
    criar_combobox_padrao
)
from util.fun_basicas import LineEditComEnter

from bd import pesquisar_produtos_estoque, salvar_historico_estoque

class LineEditBusca(LineEditComEnter):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Down:
            tela = self.parent()
            while tela is not None:
                if hasattr(tela, "focar_tabela_resultado"):
                    tela.focar_tabela_resultado()
                    return
                tela = tela.parent()
        super().keyPressEvent(event)


class TelaAcertoEstoque(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Estoque Manual")
        self.setWindowIcon(QIcon("imagens/icone.png"))
        # self.showMaximized()
        self.componentes()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)


    # def componentes(self):
    def componentes(self):
        # título
        nometela = QLabel("Acerto Estoque Manual")
        nometela.setStyleSheet("color: orange; font-size: 38px; font: bold;")
        nometela.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # quadro cinza principal
        quadro_cinza = QWidget()
        quadro_cinza.setStyleSheet("background-color: #cbcdce;")

        # layout interno do quadro
        layout_quadro = QVBoxLayout()
        layout_quadro.setContentsMargins(20, 20, 20, 20)
        layout_quadro.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        #campo opções 
        label_opcoes = criar_label_padrao()
        label_opcoes.setText('Opções')
        label_opcoes.setContentsMargins(2, 0, 0, 0)
        label_opcoes.setFixedSize(label_opcoes.sizeHint())

        self.combo_opcoes = criar_combobox_padrao()
        self.combo_opcoes.addItems(['Descrição', 'Código', 'Referências'])
        self.combo_opcoes.setFixedWidth(220)
        self.combo_opcoes.currentTextChanged.connect(self.buscar_produto)
        

        vbox_opcoes = QVBoxLayout()
        vbox_opcoes.addWidget(label_opcoes)
        vbox_opcoes.addWidget(self.combo_opcoes)

        #campo dados a pesquisar 

        label_dados_pesquisar = criar_label_padrao()
        label_dados_pesquisar.setText('Dados a pesquisar')
        label_dados_pesquisar.setContentsMargins(2, 0, 0, 0)
        label_dados_pesquisar.setFixedSize(label_dados_pesquisar.sizeHint())

        self.edit_dados_pesquisar = LineEditBusca()
        self.edit_dados_pesquisar.setStyleSheet(criar_lineedit_padrao().styleSheet())
        self.edit_dados_pesquisar.textChanged.connect(self.buscar_produto)
        
        vbox_dados_pesquisar = QVBoxLayout()
        vbox_dados_pesquisar.addWidget(label_dados_pesquisar)
        vbox_dados_pesquisar.addWidget(self.edit_dados_pesquisar)

        #layout linha 1
        hbox_linha1 = QHBoxLayout()
        hbox_linha1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_linha1.addLayout(vbox_opcoes)
        hbox_linha1.addLayout(vbox_dados_pesquisar)

        # ---------- TABELA DE RESULTADOS ----------
        self.tabela_resultado = QTableWidget()
        self.tabela_resultado.setColumnCount(4)
        self.tabela_resultado.setHorizontalHeaderLabels(["Código", "Descrição", "Quant.", "Tipo"])
        self.tabela_resultado.setStyleSheet("""
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
        """)


        header = self.tabela_resultado.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)   # Código
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Descrição
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)   # Quant

        self.tabela_resultado.setColumnWidth(0, 90)
        self.tabela_resultado.setColumnWidth(2, 90)
        self.tabela_resultado.setColumnHidden(3, True)

        # começo linha 2

        label_codigo = criar_label_padrao()
        label_codigo.setText('Código')
        label_codigo.setContentsMargins(2, 0, 0, 0)
        label_codigo.setFixedSize(label_codigo.sizeHint())

        self.line_edit_codigo = criar_lineedit_padrao()
        self.line_edit_codigo.setFixedWidth(90)
        self.line_edit_codigo.setReadOnly(True)

        vbox_codigo = QVBoxLayout()
        vbox_codigo.addWidget(label_codigo)
        vbox_codigo.addWidget(self.line_edit_codigo)
      
      
        #campo descrição
        label_descricao = criar_label_padrao()
        label_descricao.setText('Descrição')
        label_descricao.setContentsMargins(2, 0, 0, 0)
        label_descricao.setFixedSize(label_descricao.sizeHint())

        self.edit_descricao = criar_lineedit_padrao()
        self.edit_descricao.setReadOnly(True)

        vbox_descricao = QVBoxLayout()
        vbox_descricao.addWidget(label_descricao)
        vbox_descricao.addWidget(self.edit_descricao)

        #campo quantidade 
        label_quantidade = criar_label_padrao()
        label_quantidade.setText('Quantidade')
        label_quantidade.setContentsMargins(2, 0, 0, 0)
        label_quantidade.setFixedSize(label_quantidade.sizeHint())

        self.edit_quantidade = criar_lineedit_padrao()
        self.edit_quantidade.setFixedWidth(90)
        self.edit_quantidade.setReadOnly(True)

        vbox_quantidade = QVBoxLayout()
        vbox_quantidade.addWidget(label_quantidade)
        vbox_quantidade.addWidget(self.edit_quantidade)


        #campo quantidade atual

        label_nova_quant = criar_label_padrao()
        label_nova_quant.setText('Nova Quant.')
        label_nova_quant.setContentsMargins(2, 0, 0, 0)
        label_nova_quant.setFixedSize(label_nova_quant.sizeHint())

        self.edit_nova_quant = criar_lineedit_padrao()
        self.edit_nova_quant.setFixedWidth(90)

        vbox_nova_quant = QVBoxLayout()
        vbox_nova_quant.addWidget(label_nova_quant)
        vbox_nova_quant.addWidget(self.edit_nova_quant)

        hbox_linha2 = QHBoxLayout()
        hbox_linha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_linha2.addLayout(vbox_codigo)
        hbox_linha2.addLayout(vbox_descricao)
        hbox_linha2.addLayout(vbox_quantidade)
        hbox_linha2.addLayout(vbox_nova_quant)


        #tabela de itens alterados

        self.tabela_alterados = QTableWidget()
        self.tabela_alterados.setColumnCount(4)
        self.tabela_alterados.setHorizontalHeaderLabels(["Código", "Descrição", "Quant. Ant.", "Quant. Atual"])
        self.tabela_alterados.setStyleSheet("""
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
        """)
        

        header = self.tabela_alterados.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)   # Código
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Descrição
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)   # Quant Ant.
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)   # Quant Atual

        self.tabela_alterados.setColumnWidth(0, 90)
        self.tabela_alterados.setColumnWidth(2, 90)
        self.tabela_alterados.setColumnWidth(3, 90)

        self.btn_imprimir = criar_botao()
        self.btn_imprimir.setText("Imprimir")

        hbox_btn_imprimir = QHBoxLayout()
        hbox_btn_imprimir.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox_btn_imprimir.addWidget(self.btn_imprimir)

        layout_quadro.addLayout(hbox_linha1)
        layout_quadro.addWidget(self.tabela_resultado)
        layout_quadro.addLayout(hbox_linha2)
        layout_quadro.addWidget(self.tabela_alterados)
        layout_quadro.addLayout(hbox_btn_imprimir)
        layout_quadro.addStretch()

        quadro_cinza.setLayout(layout_quadro)

        # botões inferiores
        self.btn_sair = criar_botao_sair()
        self.btn_sair.clicked.connect(self.sair)

        hbox_botoes = QHBoxLayout()
        hbox_botoes.addStretch()
        hbox_botoes.addWidget(self.btn_sair)
        hbox_botoes.addSpacing(40)
        # hbox_botoes.addWidget(self.btn_confirmar)
        hbox_botoes.addStretch()

        # layout principal da tela
        vbox_geral = QVBoxLayout()
        vbox_geral.addWidget(nometela)
        vbox_geral.addWidget(quadro_cinza)
        vbox_geral.addSpacing(10)
        vbox_geral.addLayout(hbox_botoes)
        vbox_geral.setContentsMargins(20, 20, 20, 20)

        self.setLayout(vbox_geral)

        self.tabela_resultado.cellClicked.connect(self.selecionar_produto)
        self.edit_dados_pesquisar.returnPressed.connect(self.selecionar_primeiro_resultado)
        self.edit_nova_quant.returnPressed.connect(self.registrar_acerto)
        self.tabela_resultado.keyPressEvent = self.keyPressTabela



    def confirmar_entrada(self):
        QMessageBox.information(self, "Aviso", "Função de entrada de estoque ainda será ligada ao banco.")

    def focar_tabela_resultado(self):
        if self.tabela_resultado.rowCount() == 0:
            return

        self.tabela_resultado.setFocus()
        self.tabela_resultado.selectRow(0)
        
    def keyPressTabela(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            linha = self.tabela_resultado.currentRow()
            if linha >= 0:
                self.selecionar_produto(linha, 0)
        else:
            QTableWidget.keyPressEvent(self.tabela_resultado, event)

    def selecionar_produto(self, linha, coluna):
        codigo = self.tabela_resultado.item(linha, 0).text()
        descricao = self.tabela_resultado.item(linha, 1).text()
        quantidade = self.tabela_resultado.item(linha, 2).text()
        tipo = self.tabela_resultado.item(linha, 3).text().strip().lower()
        self.tipo_quantidade = tipo

        self.line_edit_codigo.setText(codigo)
        self.edit_descricao.setText(descricao)
        self.edit_quantidade.setText(quantidade)
        self.edit_nova_quant.setText("0")
        self.edit_nova_quant.setFocus()
        self.edit_nova_quant.selectAll()
        

    def selecionar_primeiro_resultado(self):
        if self.tabela_resultado.rowCount() == 0:
            return

        self.tabela_resultado.selectRow(0)
        self.selecionar_produto(0, 0)
        self.edit_nova_quant.setFocus()

    def registrar_acerto(self):
        codigo = self.line_edit_codigo.text().strip()
        descricao = self.edit_descricao.text().strip()
        quant_antiga = self.edit_quantidade.text().strip()
        quant_nova = self.edit_nova_quant.text().strip()

        # valida vazio
        if not codigo or not quant_nova:
            return

        # valida texto inválido primeiro
        try:
            teste = quant_nova.replace(",", ".")
            float(teste)
        except:
            QMessageBox.warning(self, "Erro", "Digite uma quantidade válida.")
            self.edit_nova_quant.setFocus()
            self.edit_nova_quant.selectAll()
            return

        # valida inteiro
        quant_nova = float(quant_nova.replace(",", "."))

        if hasattr(self, "tipo_quantidade"):
            if self.tipo_quantidade.strip().lower() == "inteiro":
                if not quant_nova.is_integer():
                    QMessageBox.warning(self, "Erro", "Apenas quantidade inteira.")
                    self.edit_nova_quant.setFocus()
                    self.edit_nova_quant.selectAll()
                    return
                quant_nova = int(quant_nova)

        if not atualizar_quantidade_produto(codigo, quant_nova):
            QMessageBox.warning(self, "Erro", "Não foi possível atualizar o estoque.")
            return

        salvar_historico_estoque(codigo, descricao, quant_antiga, quant_nova, "admin")

        linha = self.tabela_alterados.rowCount()
        self.tabela_alterados.insertRow(linha)

        self.tabela_alterados.setItem(linha, 0, QTableWidgetItem(codigo))
        self.tabela_alterados.setItem(linha, 1, QTableWidgetItem(descricao))
        self.tabela_alterados.setItem(linha, 2, QTableWidgetItem(quant_antiga))
        self.tabela_alterados.setItem(linha, 3, QTableWidgetItem(str(quant_nova)))

        self.line_edit_codigo.clear()
        self.edit_descricao.clear()
        self.edit_quantidade.clear()
        self.edit_nova_quant.clear()
        self.edit_dados_pesquisar.clear()
        self.tabela_resultado.setRowCount(0)
        self.edit_dados_pesquisar.setFocus()
   
   
    def buscar_produto(self, *args):
        texto = self.edit_dados_pesquisar.text().strip()
        opcao = self.combo_opcoes.currentText()

        if not texto:
            self.tabela_resultado.setRowCount(0)
            return

        mapa_opcoes = {
            "Descrição": "descricao",
            "Código": "codigo",
            "Referências": "referencia"
        }

        campo_busca = mapa_opcoes.get(opcao, "descricao")

        resultados = pesquisar_produtos_estoque(opcao, texto)

        self.tabela_resultado.setRowCount(len(resultados))

        for linha, produto in enumerate(resultados):
            for coluna, valor in enumerate(produto):
                self.tabela_resultado.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def sair(self):
        from telaMain import telaPrincipal
        self.janela = telaPrincipal()
        self.janela.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = TelaAcertoEstoque()
    janela.showMaximized()
    sys.exit(app.exec())