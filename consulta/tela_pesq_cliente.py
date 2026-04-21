import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.padrao import (
    criar_botao,
    criar_combobox_padrao,
    criar_label_padrao,
    criar_lineedit_padrao,
)
from util.estilo import gerar_estilo
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)


class TelaPesqCliente(QDialog):
    def __init__(self, tela_origem=None):
        super().__init__()
        self.tela_origem = tela_origem
        self.setWindowTitle("Pesquisa Cliente")
        self.setFixedSize(760, 520)
        self.setModal(True)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog
        )

        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '..', 'imagens', 'icone.png')
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        from entidades.cliente.cliente_service import ClienteService
        self.service = ClienteService()

        self.componentes()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)
        QShortcut(QKeySequence('F5'), self).activated.connect(
            self.abrir_cadastro_cliente
        )

        self.edit_pesq.setFocus()
        self.edit_pesq.returnPressed.connect(self.focar_tabela)
        self.edit_pesq.installEventFilter(self)

        self.tabela_resultado.cellDoubleClicked.connect(self.selecionar_cliente)
        self.tabela_resultado.itemActivated.connect(self.selecionar_cliente)

    def componentes(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #031740;
                border: 1px solid #70818C;
                border-radius: 6px;
            }
        """)

        titulo = QLabel("Pesquisa Cliente")
        titulo.setStyleSheet("""
            color: orange;
            font-size: 38px;
            font: bold;
            background-color: #031740;
        """)

        label_opc = criar_label_padrao()
        label_opc.setText("Opções")
        label_opc.setContentsMargins(2, 0, 0, 0)
        label_opc.setFixedSize(label_opc.sizeHint())
        label_opc.setStyleSheet(
            "color: white; font-weight: bold; background-color: #031740;"
        )

        self.comb_opc = criar_combobox_padrao()
        self.comb_opc.addItems([
            "Nome",
            "Razão Social",
            "Código",
            "CPF / CNPJ"
        ])
        self.comb_opc.setFixedWidth(150)

        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc)
        vbox_opc.addWidget(self.comb_opc)

        label_pesq = criar_label_padrao()
        label_pesq.setText("Dados a pesquisar")
        label_pesq.setContentsMargins(2, 0, 0, 0)
        label_pesq.setFixedSize(label_pesq.sizeHint())
        label_pesq.setStyleSheet(
            "color: white; font-weight: bold; background-color: #031740;"
        )

        self.edit_pesq = criar_lineedit_padrao()
        self.edit_pesq.setMinimumWidth(320)
        self.edit_pesq.textChanged.connect(self.buscar_cliente)

        vbox_pesq = QVBoxLayout()
        vbox_pesq.addWidget(label_pesq)
        vbox_pesq.addWidget(self.edit_pesq)

        hbox_topo = QHBoxLayout()
        hbox_topo.addLayout(vbox_opc)
        hbox_topo.addLayout(vbox_pesq)

        self.tabela_resultado = QTableWidget()
        self.tabela_resultado.setColumnCount(3)
        self.tabela_resultado.setHorizontalHeaderLabels([
            "Código",
            "Nome",
            "CPF / CNPJ"
        ])
        self.tabela_resultado.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.tabela_resultado.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabela_resultado.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
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

        self.btn_cadastrar = criar_botao()
        self.btn_cadastrar.setText("F5 - Cadastrar")
        self.btn_cadastrar.clicked.connect(self.abrir_cadastro_cliente)
        self.btn_cadastrar.setAutoDefault(False)
        self.btn_cadastrar.setDefault(False)

        self.btn_sair = criar_botao()
        self.btn_sair.setText("Esc - Sair")
        self.btn_sair.clicked.connect(self.sair)
        self.btn_sair.setAutoDefault(False)
        self.btn_sair.setDefault(False)

        hbox_botoes = QHBoxLayout()
        hbox_botoes.addWidget(self.btn_cadastrar)
        hbox_botoes.addStretch()
        hbox_botoes.addWidget(self.btn_sair)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(hbox_topo)
        layout.addWidget(self.tabela_resultado)
        layout.addLayout(hbox_botoes)

        self.setLayout(layout)

    def abrir_cadastro_cliente(self):
        from entidades.cad_cli import CadCliente
        self.janela_cadastro = CadCliente(self)
        self.janela_cadastro.show()

    def sair(self):
        self.close()

    def buscar_cliente(self):
        texto = self.edit_pesq.text().strip()
        opcao = self.comb_opc.currentText()

        if not texto:
            self.tabela_resultado.setRowCount(0)
            return

        resultados = self.service.buscar_cliente(
            opcao, texto, "Ativos", False
        )

        self.tabela_resultado.setRowCount(len(resultados))

        for linha, cliente in enumerate(resultados):
            nome_exibicao = (
                cliente.get("nome")
                or cliente.get("nome_fantasia")
                or cliente.get("razao_social")
                or ""
            )

            if opcao == "Razão Social":
                nome_exibicao = cliente.get("razao_social", "") or nome_exibicao
            elif opcao in ["Código", "CPF / CNPJ"]:
                nome_exibicao = (
                    cliente.get("nome")
                    or cliente.get("nome_fantasia")
                    or cliente.get("razao_social")
                    or ""
                )

            valores = [
                cliente.get("codigo", ""),
                nome_exibicao,
                cliente.get("cpf_cnpj", ""),
            ]

            for coluna, valor in enumerate(valores):
                self.tabela_resultado.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor) if valor else "")
                )

    def selecionar_cliente(self, *args):
        if self.tela_origem is None:
            return

        linha = self.tabela_resultado.currentRow()
        if linha < 0:
            return

        item_codigo = self.tabela_resultado.item(linha, 0)
        item_nome = self.tabela_resultado.item(linha, 1)
        item_cpf = self.tabela_resultado.item(linha, 2)

        if item_codigo is None or item_nome is None:
            return

        codigo = item_codigo.text().strip()
        nome = item_nome.text().strip()
        cpf = item_cpf.text().strip() if item_cpf else ""

        if hasattr(self.tela_origem, "selecionar_cliente"):
            self.tela_origem.selecionar_cliente(codigo, nome, cpf)

        self.close()

    def focar_tabela(self):
        if self.tabela_resultado.rowCount() > 0:
            self.tabela_resultado.setCurrentCell(0, 0)
            self.tabela_resultado.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.edit_pesq and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Down:
                self.focar_tabela()
                return True

        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(gerar_estilo())
    janela = TelaPesqCliente()
    janela.exec()