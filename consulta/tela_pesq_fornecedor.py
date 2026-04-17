import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.padrao import (
    criar_botao,
    criar_botao_sair,
    criar_combobox_padrao,
    criar_label_padrao,
    criar_lineedit_padrao,
)
from util.estilo import gerar_estilo
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

class TelaPesqFornecedor(QWidget):
    def __init__(self, tela_origem=None):
        super().__init__()
        self.tela_origem = tela_origem
        self.setWindowTitle("Pesquisa Fornecedor")
        self.setFixedSize(700, 500)

        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '..', 'imagens', 'icone.png')
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.componentes()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)
        self.edit_pesq.setFocus()
        from entidades.fornecedor.fornecedor_repository import FornecedorRepository
        self.repository = FornecedorRepository()
        self.edit_pesq.returnPressed.connect(self.focar_tabela)
        self.edit_pesq.installEventFilter(self)

        self.tabela_resultado.cellDoubleClicked.connect(
            self.selecionar_fornecedor)
        self.tabela_resultado.itemActivated.connect(self.selecionar_fornecedor)

        QShortcut(QKeySequence('F5'), self).activated.connect(
            self.abrir_cadastro_fornecedor)

    def componentes(self):

        titulo = QLabel("Pesquisa Fornecedor")
        titulo.setStyleSheet("color: orange; font-size: 38px; font: bold;")

        # opções
        label_opc = criar_label_padrao()
        label_opc.setText("Opções")
        label_opc.setContentsMargins(2, 0, 0, 0)
        label_opc.setFixedSize(label_opc.sizeHint())
        label_opc.setStyleSheet("color: white; font-weight: bold")

        self.comb_opc = criar_combobox_padrao()
        self.comb_opc.addItems(
            ["Nome", "Razão Social", "Código", "CPF / CNPJ"])
        self.comb_opc.setFixedWidth(150)

        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc)
        vbox_opc.addWidget(self.comb_opc)

        # pesquisa
        label_pesq = criar_label_padrao()
        label_pesq.setText("Dados a pesquisar")
        label_pesq.setContentsMargins(2, 0, 0, 0)
        label_pesq.setFixedSize(label_pesq.sizeHint())
        label_pesq.setStyleSheet("color: white; font-weight: bold")

        self.edit_pesq = criar_lineedit_padrao()
        self.edit_pesq.setMinimumWidth(300)
        self.edit_pesq.textChanged.connect(self.buscar_fornecedor)

        vbox_pesq = QVBoxLayout()
        vbox_pesq.addWidget(label_pesq)
        vbox_pesq.addWidget(self.edit_pesq)

        hbox_topo = QHBoxLayout()
        hbox_topo.addLayout(vbox_opc)
        hbox_topo.addLayout(vbox_pesq)

        # tabela
        self.tabela_resultado = QTableWidget()
        self.tabela_resultado.setColumnCount(3)
        self.tabela_resultado.setHorizontalHeaderLabels([
            "Código",
            "Nome",
            "CPF / CNPJ"
        ])
        self.tabela_resultado.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_resultado.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_resultado.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection)
        self.tabela_resultado.setAlternatingRowColors(True)
        self.tabela_resultado.verticalHeader().setVisible(False)
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
            QHeaderView::section {
                background-color: #cbdae4;
                color: black;
                font-weight: bold;
                border: none;
            }
        """)

        header = self.tabela_resultado.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        # botões
        self.btn_cadastrar = criar_botao()
        self.btn_cadastrar.setText("F5 - Cadastrar")
        self.btn_cadastrar.clicked.connect(self.abrir_cadastro_fornecedor)

        self.btn_sair = criar_botao()
        self.btn_sair.setText("Esc - Sair")
        self.btn_sair.clicked.connect(self.sair)

        hbox_botoes = QHBoxLayout()
        hbox_botoes.addWidget(self.btn_cadastrar)
        hbox_botoes.addStretch()
        hbox_botoes.addWidget(self.btn_sair)

        # layout geral
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(hbox_topo)
        layout.addWidget(self.tabela_resultado)
        layout.addLayout(hbox_botoes)

        self.setLayout(layout)

    def abrir_cadastro_fornecedor(self):
        from entidades.cad_for import CadFornecedor
        self.janela_cadastro = CadFornecedor(self)
        self.janela_cadastro.show()

    def sair(self):
        self.close()

    def buscar_fornecedor(self):
        texto = self.edit_pesq.text().strip()
        opcao = self.comb_opc.currentText()

        if not texto:
            self.tabela_resultado.setRowCount(0)
            return

        resultados = self.repository.buscar_fornecedor(
            opcao, texto, "Ativos", False)

        self.tabela_resultado.setRowCount(len(resultados))

        for linha, fornecedor in enumerate(resultados):

            nome_exibicao = fornecedor.get("nome_fantasia", "")

            if opcao == "Razão Social":
                nome_exibicao = fornecedor.get("razao_social", "")
            elif opcao in ["Código", "CPF / CNPJ"]:
                nome_exibicao = fornecedor.get(
                    "nome_fantasia", "") or fornecedor.get("razao_social", "")

            valores = [
                fornecedor.get("codigo", ""),
                nome_exibicao,
                fornecedor.get("cpf_cnpj", ""),
            ]

            for coluna, valor in enumerate(valores):
                self.tabela_resultado.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor) if valor else "")
                )

    def selecionar_fornecedor(self, *args):
        if self.tela_origem is None:
            return

        linha = self.tabela_resultado.currentRow()

        if linha < 0:
            return

        item_codigo = self.tabela_resultado.item(linha, 0)
        item_nome = self.tabela_resultado.item(linha, 1)

        if item_codigo is None or item_nome is None:
            return

        codigo = item_codigo.text().strip()
        nome = item_nome.text().strip()

        if hasattr(self.tela_origem, "selecionar_fornecedor"):
            self.tela_origem.selecionar_fornecedor(codigo, nome)

        self.close()

    def focar_tabela(self):
        if self.tabela_resultado.rowCount() > 0:
            self.tabela_resultado.setCurrentCell(0, 0)
            self.tabela_resultado.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.edit_pesq:
            if event.type() == event.Type.KeyPress:
                if event.key() == Qt.Key.Key_Down:
                    self.focar_tabela()
                    return True

        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = TelaPesqFornecedor()
    janela.show()
    sys.exit(app.exec())
