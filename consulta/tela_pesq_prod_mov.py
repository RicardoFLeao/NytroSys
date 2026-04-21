import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from adm_prod.produto_service import ProdutoService
from util.estilo import gerar_estilo
from util.padrao import (
    criar_botao,
    criar_lineedit_padrao,
    criar_combobox_padrao,
)
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
    QFrame,
    QTableWidgetItem
)
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence, QPixmap
from PyQt6.QtCore import Qt


class TelaConsProd(QDialog):
    def __init__(self, tela_origem=None):
        super().__init__()
        self.tela_origem = tela_origem
        self.service = ProdutoService()
        self.produtos = []
        self.setWindowTitle("Pesquisa de Produtos")
        self.setMinimumSize(1100, 650)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '..', 'imagens', 'icone.png')
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.componentes()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.reject)
        QShortcut(QKeySequence('Return'),
                  self).activated.connect(self.selecionar)
        QShortcut(QKeySequence('Enter'), self).activated.connect(
            self.selecionar)
        QShortcut(QKeySequence('F7'), self).activated.connect(self.detalhe)

        self.edit_buscar.textChanged.connect(self.buscar_produtos)
        self.tabela.currentCellChanged.connect(
            self.mostrar_produto_selecionado)
        self.edit_buscar.installEventFilter(self)

    def componentes(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #031740;
                border: 1px solid #70818C;
                border-radius: 6px;
            }
        """)

        titulo = QLabel("Pesquisa de Produtos")
        titulo.setStyleSheet("""
            color: orange;
            background-color: #031740;
            font-size: 28px;
            font-weight: bold;
        """)

        topo = QHBoxLayout()
        topo.addWidget(titulo)
        topo.addStretch()

        label_buscar = QLabel("Buscar:")
        label_buscar.setStyleSheet("""
            font-size: 16px;
            background-color: #031740;
            font-weight: bold;
            color: white;
        """)

        self.edit_buscar = criar_lineedit_padrao()
        self.edit_buscar.setMinimumHeight(34)

        label_filtrar = QLabel("Filtrar por:")
        label_filtrar.setStyleSheet("""
            font-size: 16px;
            background-color: #031740;
            font-weight: bold;
            color: white;
        """)

        self.combo_filtrar = criar_combobox_padrao()
        self.combo_filtrar.addItems(
            ["Todos", "Descrição", "Código", "Cód. Barras", "Referências"])
        self.combo_filtrar.setCurrentIndex(0)
        self.combo_filtrar.setFixedWidth(180)

        linha_busca = QHBoxLayout()
        linha_busca.addSpacing(15)
        linha_busca.addWidget(label_buscar)
        linha_busca.addWidget(self.edit_buscar, 1)
        linha_busca.addSpacing(40)
        linha_busca.addWidget(label_filtrar)
        linha_busca.addWidget(self.combo_filtrar)

        self.tabela = QTableWidget()
        self.tabela.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels([
            "Código", "Descrição", "Marca", "Referencia", "Valor", "Unid.", "Quantidade"
        ])
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: white;
                font-size: 13px;
                border: 1px solid #70818C;
                gridline-color: #d0d7de;
                alternate-background-color: #f5f5f5;
            }

            QTableWidget::item {
                padding: 4px;
            }

            QTableWidget::item:hover {
                background-color: #eef5fb;
                
            }

            QHeaderView::section {
                background-color: #cbdae4;
                color: black;
                font-weight: bold;
                border: none;
                padding: 6px;
            }
        """)

        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        self.label_localizacao = QLabel("Localização:")
        self.label_localizacao.setStyleSheet("""
            font-size: 15px;
            color: white;
            background-color: #031740;
            font-weight: bold;
        """)

        label_rua = QLabel("Rua")
        label_bloco = QLabel("Bloco")
        label_prateleira = QLabel("Prateleira")
        label_gaveta = QLabel("Gaveta")

        for lbl in [label_rua, label_bloco, label_prateleira, label_gaveta]:
            lbl.setStyleSheet("""
                color: white;
                background-color: #031740;
                font-size: 13px;
                font-weight: bold;
            """)

        self.edit_rua = criar_lineedit_padrao()
        self.edit_bloco = criar_lineedit_padrao()
        self.edit_prateleira = criar_lineedit_padrao()
        self.edit_gaveta = criar_lineedit_padrao()

        for edit in [self.edit_rua, self.edit_bloco, self.edit_prateleira, self.edit_gaveta]:
            edit.setReadOnly(True)
            edit.setFixedHeight(26)

        linha_loc = QHBoxLayout()
        linha_loc.setSpacing(10)

        linha_loc.addWidget(self.label_localizacao)
        linha_loc.addSpacing(10)

        linha_loc.addWidget(label_rua)
        linha_loc.addWidget(self.edit_rua)

        linha_loc.addWidget(label_bloco)
        linha_loc.addWidget(self.edit_bloco)

        linha_loc.addWidget(label_prateleira)
        linha_loc.addWidget(self.edit_prateleira)

        linha_loc.addWidget(label_gaveta)
        linha_loc.addWidget(self.edit_gaveta)

        self.label_aplicacao = QLabel("Aplicação:")
        self.label_aplicacao.setStyleSheet("""
            font-size: 15px;
            color: white;
            background-color: #031740;
            font-weight: bold;
        """)

        self.edit_aplicacao = criar_lineedit_padrao()

        linha_aplicacao = QHBoxLayout()
        linha_aplicacao.addSpacing(10)
        linha_aplicacao.addWidget(self.label_aplicacao)
        linha_aplicacao.addSpacing(10)
        linha_aplicacao.addWidget(self.edit_aplicacao)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(12)
        info_layout.addLayout(linha_loc)
        info_layout.addLayout(linha_aplicacao)
        info_layout.addStretch()

        self.label_foto = QLabel()
        self.label_foto.setFixedSize(220, 170)
        self.label_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_foto.setStyleSheet("""
            background-color: white;
            border: 1px solid #70818C;
        """)
        self.label_foto.setText("Sem foto")

        area_inferior = QHBoxLayout()
        area_inferior.setSpacing(20)
        area_inferior.addLayout(info_layout, 1)
        area_inferior.addWidget(self.label_foto)

        self.label_esc = QLabel("Esc - Sair")
        self.label_esc.setStyleSheet("""
            color: orange;
            background-color: #031740;
            font-size: 16px;
            font-weight: bold;
        """)

        self.label_enter = QLabel("Enter - Selecionar")
        self.label_enter.setStyleSheet("""
            color: orange;
            background-color: #031740;
            font-size: 16px;
            font-weight: bold;
        """)

        self.btn_detalhe = criar_botao()
        self.btn_detalhe.setText("F7 - Detalhe")
        self.btn_detalhe.clicked.connect(self.detalhe)

        rodape = QHBoxLayout()
        rodape.addWidget(self.label_esc)
        rodape.addStretch()
        rodape.addWidget(self.label_enter)
        rodape.addSpacing(20)
        rodape.addWidget(self.btn_detalhe)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        layout.addLayout(topo)
        layout.addLayout(linha_busca)
        layout.addWidget(self.tabela, 1)
        layout.addLayout(area_inferior)
        layout.addLayout(rodape)

        self.setLayout(layout)

    def selecionar(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            return

        item_codigo = self.tabela.item(linha, 0)
        if not item_codigo:
            return

        codigo = item_codigo.text().strip()
        if not codigo:
            return

        produto = self.service.buscar_produto_por_codigo(codigo)
        if not produto:
            return

        if self.tela_origem:
            resultado = self.tela_origem.receber_produto_pesquisa(produto)

            if resultado is False:
                self.show()
                self.raise_()
                self.activateWindow()
                self.edit_buscar.setFocus()
                self.edit_buscar.selectAll()
                return

        self.close()

    def detalhe(self):
        print("abrir detalhe do produto")

    def buscar_produtos(self):
        texto = self.edit_buscar.text().strip().upper()
        opcao = self.combo_filtrar.currentText()

        self.tabela.setRowCount(0)
        self.produtos = []

        if len(texto) < 1:
            self.tabela.setRowCount(0)
            return

        self.produtos = self.service.pesquisar_produtos_para_consulta(
            opcao,
            texto,
            buscar_todos=False,
            status="Ativo",
        )

        if not self.produtos:
            return

        self.tabela.setRowCount(len(self.produtos))

        for linha, produto in enumerate(self.produtos):
            unidade = str(produto.get("un_venda") or "")
            codigo = str(produto.get("codigo", ""))
            descricao = str(produto.get("descricao", ""))

            cod_marca = produto.get("cod_marca")
            marca = ""

            if cod_marca:
                marca_encontrada = self.service.buscar_marca_por_codigo(
                    cod_marca)
                if marca_encontrada:
                    marca = str(marca_encontrada.get("nome") or "")

            referencia = str(produto.get("ref_fornecedor") or "")

            preco = produto.get("preco_venda", 0)
            try:
                preco = f"{float(preco):.2f}".replace(".", ",")
            except (ValueError, TypeError):
                preco = "0,00"

            # ===== QUANTIDADE =====
            quant_valor = produto.get("quantidade", 0)
            try:
                quant_float = float(quant_valor)
            except (ValueError, TypeError):
                quant_float = 0

            quantidade = str(quant_valor)

            # ===== INSERE NA TABELA =====
            self.tabela.setItem(linha, 0, QTableWidgetItem(codigo))
            self.tabela.setItem(linha, 1, QTableWidgetItem(descricao))
            self.tabela.setItem(linha, 2, QTableWidgetItem(marca))
            self.tabela.setItem(linha, 3, QTableWidgetItem(referencia))
            self.tabela.setItem(linha, 4, QTableWidgetItem(preco))
            self.tabela.setItem(linha, 5, QTableWidgetItem(unidade))
            self.tabela.setItem(linha, 6, QTableWidgetItem(quantidade))
            # ===== COR VERMELHA SE ESTOQUE <= 0 =====
            if quant_float <= 0:
                for col in range(self.tabela.columnCount()):
                    item = self.tabela.item(linha, col)
                    if item:
                        item.setForeground(Qt.GlobalColor.red)

        if self.tabela.rowCount() > 0:
            self.tabela.setCurrentCell(0, 0)

    def mostrar_produto_selecionado(self, linha_atual, coluna_atual, linha_anterior, coluna_anterior):
        linha = linha_atual

        if linha < 0:
            return
        item_codigo = self.tabela.item(linha, 0)
        if not item_codigo:
            return

        codigo = item_codigo.text().strip()
        if not codigo:
            return

        produto = self.service.buscar_produto_por_codigo(codigo)
        if not produto:
            return

        self.edit_rua.setText(str(produto.get("rua") or ""))
        self.edit_bloco.setText(str(produto.get("bloco") or ""))
        self.edit_prateleira.setText(str(produto.get("prateleira") or ""))
        self.edit_gaveta.setText(str(produto.get("gaveta") or ""))
        self.edit_aplicacao.setText(str(produto.get("aplicacao") or ""))

        caminho_foto = str(produto.get("foto_1") or "").strip()

        if caminho_foto and os.path.exists(caminho_foto):
            pixmap = QPixmap(caminho_foto)
            pixmap = pixmap.scaled(
                self.label_foto.width(),
                self.label_foto.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.label_foto.setPixmap(pixmap)
            self.label_foto.setText("")
        else:
            self.label_foto.clear()
            self.label_foto.setText("Sem foto")

        # resetar todas as linhas
        for l in range(self.tabela.rowCount()):
            for c in range(self.tabela.columnCount()):
                item = self.tabela.item(l, c)
                if item:
                    font = item.font()
                    font.setBold(False)
                    item.setFont(font)

                    # fundo padrão (linha normal)
                    item.setBackground(Qt.GlobalColor.white)

                    coluna_quant = self.tabela.columnCount() - 1
                    item_quant = self.tabela.item(l, coluna_quant)

                    quant_float = 0
                    if item_quant:
                        try:
                            quant_float = float(
                                item_quant.text().replace(",", "."))
                        except ValueError:
                            quant_float = 0

                    if quant_float <= 0:
                        item.setForeground(Qt.GlobalColor.red)
                    else:
                        item.setForeground(Qt.GlobalColor.black)

        # aplicar bold na linha selecionada
        for c in range(self.tabela.columnCount()):
            item = self.tabela.item(linha, c)
            if item:
                font = item.font()
                font.setBold(True)
                item.setFont(font)

                # fundo da linha selecionada
                from PyQt6.QtGui import QColor
                item.setBackground(QColor("#dbe7f0"))

                coluna_quant = self.tabela.columnCount() - 1
                item_quant = self.tabela.item(linha, coluna_quant)

                quant_float = 0
                if item_quant:
                    try:
                        quant_float = float(
                            item_quant.text().replace(",", "."))
                    except ValueError:
                        quant_float = 0

                if quant_float <= 0:
                    item.setForeground(Qt.GlobalColor.red)
                else:
                    item.setForeground(Qt.GlobalColor.black)

    def eventFilter(self, obj, event):
        if obj == self.edit_buscar and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Down:
                if self.tabela.rowCount() > 0:
                    self.tabela.setFocus()
                    self.tabela.setCurrentCell(0, 0)
                    return True

        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(gerar_estilo())
    janela = TelaConsProd()
    janela.exec()
