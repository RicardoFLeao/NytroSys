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


class TelaPesqFuncionario(QDialog):
    def __init__(self, tela_origem=None):
        super().__init__()
        self.tela_origem = tela_origem
        self.setWindowTitle("Pesquisa Vendedor")
        self.setFixedSize(700, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'imagens', 'icone.png')
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.componentes()

        from entidades.funcionario.funcionario_repository import FuncionarioRepository
        self.repository = FuncionarioRepository()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.close)

        self.edit_pesq.setFocus()
        self.edit_pesq.textChanged.connect(self.buscar_funcionario)
        # self.edit_pesq.returnPressed.connect(self.focar_tabela)
        self.edit_pesq.installEventFilter(self)

        self.tabela_resultado.itemActivated.connect(self.selecionar_funcionario)
        self.tabela_resultado.currentCellChanged.connect(self.destacar_linha)

    def componentes(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #031740;
                border: 1px solid #70818C;
                border-radius: 6px;
            }
        """)


        titulo = QLabel("Pesquisa Vendedor")
        titulo.setStyleSheet("""
            color: orange;
            background-color: #031740;
            font-size: 38px;
            font: bold;
        """)

        label_opc = criar_label_padrao()
        label_opc.setText("Opções")
        label_opc.setContentsMargins(2, 0, 0, 0)
        label_opc.setFixedSize(label_opc.sizeHint())
        label_opc.setStyleSheet("""
            color: white;
            background-color: #031740;
            font-weight: bold
        """)

        self.comb_opc = criar_combobox_padrao()
        self.comb_opc.addItems(["Nome", "Código", "Usuário"])
        self.comb_opc.setFixedWidth(150)

        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc)
        vbox_opc.addWidget(self.comb_opc)

        label_pesq = criar_label_padrao()
        label_pesq.setText("Dados a pesquisar")
        label_pesq.setContentsMargins(2, 0, 0, 0)
        label_pesq.setFixedSize(label_pesq.sizeHint())
        label_pesq.setStyleSheet("""
            color: white;
            background-color: #031740;
            font-weight: bold
        """)

        self.edit_pesq = criar_lineedit_padrao()
        self.edit_pesq.setMinimumWidth(300)

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
            "Usuário"
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

        self.btn_sair = criar_botao()
        self.btn_sair.setText("Esc - Sair")
        self.btn_sair.clicked.connect(self.close)
        self.btn_sair.setAutoDefault(False)
        self.btn_sair.setDefault(False)


        hbox_botoes = QHBoxLayout()
        hbox_botoes.addStretch()
        hbox_botoes.addWidget(self.btn_sair)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(hbox_topo)
        layout.addWidget(self.tabela_resultado)
        layout.addLayout(hbox_botoes)

        self.setLayout(layout)


    def buscar_funcionario(self):
        texto = self.edit_pesq.text().strip()
        opcao = self.comb_opc.currentText()

        if not texto:
            self.tabela_resultado.setRowCount(0)
            return

        resultados = self.repository.buscar_funcionario(opcao, texto, "Ativos", False)

        self.tabela_resultado.setRowCount(len(resultados))

        for linha, funcionario in enumerate(resultados):
            codigo = funcionario.get("codigo", "")
            nome = funcionario.get("nome", "")
            usuario = funcionario.get("apelido", "")

            self.tabela_resultado.setItem(linha, 0, QTableWidgetItem(str(codigo)))
            self.tabela_resultado.setItem(linha, 1, QTableWidgetItem(str(nome)))
            self.tabela_resultado.setItem(linha, 2, QTableWidgetItem(str(usuario)))


    def selecionar_funcionario(self, *args):
        if self.tela_origem is None:
            return

        linha = self.tabela_resultado.currentRow()

        if linha < 0:
            return

        item_codigo = self.tabela_resultado.item(linha, 0)
        item_apelido = self.tabela_resultado.item(linha, 2)

        if not item_codigo or not item_apelido:
            return

        codigo = item_codigo.text().strip()
        apelido = item_apelido.text().strip()

        if hasattr(self.tela_origem, "selecionar_vendedor"):
            self.tela_origem.selecionar_vendedor(codigo, apelido)

        self.close()

    def focar_tabela(self):
        if self.tabela_resultado.rowCount() > 0:
            self.tabela_resultado.setCurrentCell(0, 0)
            self.tabela_resultado.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.edit_pesq and event.type() == event.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Down, Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.focar_tabela()
                return True

        return super().eventFilter(obj, event)

    def destacar_linha(self, linha_atual, coluna_atual, linha_anterior, coluna_anterior):
        for linha in range(self.tabela_resultado.rowCount()):
            for coluna in range(self.tabela_resultado.columnCount()):
                item = self.tabela_resultado.item(linha, coluna)
                if item:
                    fonte = item.font()
                    fonte.setBold(False)
                    item.setFont(fonte)

        if linha_atual < 0:
            return

        for coluna in range(self.tabela_resultado.columnCount()):
            item = self.tabela_resultado.item(linha_atual, coluna)
            if item:
                fonte = item.font()
                fonte.setBold(True)
                item.setFont(fonte)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = TelaPesqFuncionario()
    janela.exec()