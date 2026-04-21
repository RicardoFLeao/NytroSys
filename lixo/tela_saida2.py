import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QHBoxLayout, QLineEdit, QCheckBox,
    QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence, QPixmap

from util.estilo import gerar_estilo
from util.fun_basicas import LineEditComEnter
from util.padrao import criar_label_padrao, criar_lineedit_padrao


class TelaSaida(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Saída')
        self.produto_atual = None
        self.bloquear_tratamento_tabela = False

        self.componentes()
        self.showMaximized()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)
        QShortcut(QKeySequence('F8'), self.edit_busca_produto).activated.connect(self.abrir_pesquisa_produto)

        QShortcut(QKeySequence(Qt.Key.Key_Down), self.tabela).activated.connect(self.descer_tabela_quantidade)
        QShortcut(QKeySequence(Qt.Key.Key_Up), self.tabela).activated.connect(self.subir_tabela_quantidade)

        self.atalho_enter_tabela = QShortcut(QKeySequence('Return'), self.tabela)
        self.atalho_enter_tabela.setContext(Qt.ShortcutContext.WidgetShortcut)
        self.atalho_enter_tabela.activated.connect(self.enter_tabela)

        self.atalho_enter_tabela2 = QShortcut(QKeySequence('Enter'), self.tabela)
        self.atalho_enter_tabela2.setContext(Qt.ShortcutContext.WidgetShortcut)
        self.atalho_enter_tabela2.activated.connect(self.enter_tabela)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_data_hora)
        self.timer.start(1000)

        self.tabela.cellClicked.connect(self.clicar_tabela)
        self.tabela.itemChanged.connect(self.tratar_edicao_tabela)

        self.edit_busca_produto.returnPressed.connect(self.ir_para_tabela_quantidade)

    def componentes(self):
        titulo = QLabel("Saída")
        titulo.setStyleSheet("color: orange; font-size: 40px; font: bold")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFixedHeight(55)

        self.quadro = QFrame()
        self.quadro.setStyleSheet("""
            QFrame {
                background-color: #d9d9d9;
                border-radius: 10px;
            }
        """)

        self.botao_venda = QPushButton("Vendas")
        self.botao_consultas = QPushButton("Consultas")
        self.botao_relatorios = QPushButton("Relatórios")
        self.botao_sair = QPushButton("ESC - Sair")
        self.botao_sair.clicked.connect(self.sair)

        for b in [self.botao_venda, self.botao_consultas, self.botao_relatorios, self.botao_sair]:
            b.setFixedSize(180, 60)
            b.setStyleSheet("""
                QPushButton {
                    background-color: #031740;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                }
            """)

        layout_botoes = QVBoxLayout()
        layout_botoes.setSpacing(20)
        layout_botoes.addWidget(self.botao_venda)
        layout_botoes.addWidget(self.botao_consultas)
        layout_botoes.addWidget(self.botao_relatorios)
        layout_botoes.addStretch()
        layout_botoes.addWidget(self.botao_sair)

        layout_quadro = QVBoxLayout()
        layout_quadro.setContentsMargins(20, 10, 20, 10)
        layout_quadro.setSpacing(8)

        self.label_num = QLabel("Nº Venda:")
        self.label_num.setStyleSheet("font-size:14px; font-weight:bold; color:#031740;")

        self.edit_num = QLineEdit("0001")
        self.edit_num.setFixedSize(80, 28)
        self.edit_num.setStyleSheet("""
            QLineEdit {
                background: white;
                color: black;
                border: 1px solid #9a9a9a;
                border-radius: 5px;
                padding-left: 5px;
            }
        """)

        topo_esq = QHBoxLayout()
        topo_esq.setSpacing(6)
        topo_esq.addWidget(self.label_num)
        topo_esq.addWidget(self.edit_num)
        topo_esq.addStretch()

        self.check_orc = QCheckBox("Orçamento")
        self.check_cfe = QCheckBox("CFE")
        self.check_nfe = QCheckBox("NFE")

        for check in [self.check_orc, self.check_cfe, self.check_nfe]:
            check.setStyleSheet("""
                QCheckBox {
                    background: transparent;
                    color: black;
                    font-weight: bold;
                }
            """)

        self.label_data = QLabel()
        self.label_data.setFixedHeight(28)
        self.label_data.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: bold;
            }
        """)

        topo_dir = QHBoxLayout()
        topo_dir.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        topo_dir.setSpacing(8)
        topo_dir.addWidget(self.check_orc)
        topo_dir.addWidget(self.check_cfe)
        topo_dir.addWidget(self.check_nfe)
        topo_dir.addSpacing(10)
        topo_dir.addWidget(self.label_data)

        topo = QHBoxLayout()
        topo.setSpacing(10)
        topo.addLayout(topo_esq)
        topo.addStretch()
        topo.addLayout(topo_dir)

        linha = QFrame()
        linha.setFixedHeight(2)
        linha.setStyleSheet("background:#364959;")

        self.label_cliente = criar_label_padrao()
        self.label_cliente.setText("Cliente:")
        self.label_cliente.setFixedSize(self.label_cliente.sizeHint())

        self.cod_cliente = criar_lineedit_padrao()
        self.cod_cliente.setFixedWidth(70)
        self.cod_cliente.setPlaceholderText("Cod. Cli.")

        self.edit_cliente = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cliente.setMinimumWidth(500)
        self.edit_cliente.setPlaceholderText("F8 - Pesquisa clientes")

        self.label_cpf_cliente = criar_label_padrao()
        self.label_cpf_cliente.setText("CPF")
        self.label_cpf_cliente.setFixedSize(self.label_cpf_cliente.sizeHint())

        self.edit_cpf_cliente = criar_lineedit_padrao()
        self.edit_cpf_cliente.setFixedWidth(150)

        linha_cliente = QHBoxLayout()
        linha_cliente.setSpacing(10)
        linha_cliente.addWidget(self.label_cliente)
        linha_cliente.addWidget(self.cod_cliente)
        linha_cliente.addWidget(self.edit_cliente)
        linha_cliente.addWidget(self.label_cpf_cliente)
        linha_cliente.addWidget(self.edit_cpf_cliente)

        self.label_vendedor = criar_label_padrao()
        self.label_vendedor.setText("Vendedor:")
        self.label_vendedor.setFixedSize(self.label_vendedor.sizeHint())

        self.cod_vendedor = criar_lineedit_padrao()
        self.cod_vendedor.setFixedWidth(70)
        self.cod_vendedor.setPlaceholderText("Cod. Vend.")

        self.edit_vendedor = criar_lineedit_padrao(LineEditComEnter)
        self.edit_vendedor.setFixedWidth(150)
        self.edit_vendedor.setPlaceholderText("F8 - Pesquisa vendedor")

        self.label_desconto = criar_label_padrao()
        self.label_desconto.setText("Desconto:")
        self.label_desconto.setFixedSize(self.label_desconto.sizeHint())

        self.edit_desconto = criar_lineedit_padrao(LineEditComEnter)
        self.edit_desconto.setFixedWidth(70)
        self.edit_desconto.setPlaceholderText('ctrl+d')

        self.label_percentual = criar_label_padrao()
        self.label_percentual.setText("%")
        self.label_percentual.setFixedSize(self.label_percentual.sizeHint())

        linha_vendedor_desconto = QHBoxLayout()
        linha_vendedor_desconto.setSpacing(10)
        linha_vendedor_desconto.addWidget(self.label_vendedor)
        linha_vendedor_desconto.addWidget(self.cod_vendedor)
        linha_vendedor_desconto.addWidget(self.edit_vendedor)
        linha_vendedor_desconto.addWidget(self.label_desconto)
        linha_vendedor_desconto.addWidget(self.edit_desconto)
        linha_vendedor_desconto.addWidget(self.label_percentual)
        linha_vendedor_desconto.addStretch()

        bloco_esquerdo = QVBoxLayout()
        bloco_esquerdo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        bloco_esquerdo.setSpacing(8)
        bloco_esquerdo.addLayout(linha_cliente)
        bloco_esquerdo.addLayout(linha_vendedor_desconto)

        self.label_total_prod_titulo = criar_label_padrao()
        self.label_total_prod_titulo.setText("Total Produtos:")
        self.label_total_prod_titulo.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #222222;
                background: transparent;
                border: none;
            }
        """)
        self.label_total_prod_titulo.setFixedSize(self.label_total_prod_titulo.sizeHint())

        self.label_total_produtos = QLabel("R$ 0,00")
        self.label_total_produtos.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #1f2c5c;
                background: transparent;
                border: none;
            }
        """)

        linha_total_prod = QHBoxLayout()
        linha_total_prod.setSpacing(10)
        linha_total_prod.addWidget(self.label_total_prod_titulo)
        linha_total_prod.addWidget(self.label_total_produtos)
        linha_total_prod.addStretch()

        self.label_total_venda_titulo = criar_label_padrao()
        self.label_total_venda_titulo.setText("Total Venda:")
        self.label_total_venda_titulo.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1f2c5c;
                background: transparent;
                border: none;
            }
        """)

        self.label_total_venda = QLabel("R$ 0,00")
        self.label_total_venda.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #1f2c5c;
                background: transparent;
                border: none;
            }
        """)

        linha_total_venda = QHBoxLayout()
        linha_total_venda.setSpacing(10)
        linha_total_venda.addWidget(self.label_total_venda_titulo)
        linha_total_venda.addWidget(self.label_total_venda)
        linha_total_venda.addStretch()

        linha_vertical = QFrame()
        linha_vertical.setFrameShape(QFrame.Shape.VLine)
        linha_vertical.setStyleSheet("color: #c8c8c8;")

        bloco_direito = QVBoxLayout()
        bloco_direito.setAlignment(Qt.AlignmentFlag.AlignTop)
        bloco_direito.setSpacing(8)
        bloco_direito.addLayout(linha_total_prod)
        bloco_direito.addLayout(linha_total_venda)

        linha_dados = QHBoxLayout()
        linha_dados.setAlignment(Qt.AlignmentFlag.AlignTop)
        linha_dados.setSpacing(15)
        linha_dados.addLayout(bloco_esquerdo, 1)
        linha_dados.addWidget(linha_vertical)
        linha_dados.addLayout(bloco_direito)

        self.label_busca_produto = criar_label_padrao()
        self.label_busca_produto.setText("Busca de produtos")
        self.label_busca_produto.setFixedSize(self.label_busca_produto.sizeHint())

        self.label_quantidade = criar_label_padrao()
        self.label_quantidade.setText("Quantidade")
        self.label_quantidade.setFixedSize(self.label_quantidade.sizeHint())

        self.label_unitario = criar_label_padrao()
        self.label_unitario.setText("Unitário")
        self.label_unitario.setFixedSize(self.label_unitario.sizeHint())

        self.edit_busca_produto = criar_lineedit_padrao()
        self.edit_busca_produto.setMinimumHeight(34)

        self.edit_quantidade_item = QLineEdit()
        self.edit_quantidade_item.setFixedSize(120, 34)
        self.edit_quantidade_item.setText("0,00")

        self.edit_unitario_item = criar_lineedit_padrao()
        self.edit_unitario_item.setFixedSize(120, 34)
        self.edit_unitario_item.setText("0,00")

        self.edit_quantidade_item.setStyleSheet(self.edit_unitario_item.styleSheet())
        self.edit_quantidade_item.returnPressed.connect(self.ir_para_unitario)
        self.edit_unitario_item.returnPressed.connect(self.adicionar_produto_tabela)

        topo_busca_esquerda = QVBoxLayout()
        topo_busca_esquerda.setSpacing(4)

        linha_label_busca = QHBoxLayout()
        linha_label_busca.setSpacing(8)
        linha_label_busca.addWidget(self.label_busca_produto)
        linha_label_busca.addStretch()

        topo_busca_esquerda.addLayout(linha_label_busca)
        topo_busca_esquerda.addWidget(self.edit_busca_produto)

        topo_busca_quant = QVBoxLayout()
        topo_busca_quant.setSpacing(4)
        topo_busca_quant.addWidget(self.label_quantidade)
        topo_busca_quant.addWidget(self.edit_quantidade_item)

        topo_busca_unit = QVBoxLayout()
        topo_busca_unit.setSpacing(4)
        topo_busca_unit.addWidget(self.label_unitario)
        topo_busca_unit.addWidget(self.edit_unitario_item)

        linha_topo_produtos = QHBoxLayout()
        linha_topo_produtos.setSpacing(18)
        linha_topo_produtos.addLayout(topo_busca_esquerda, 1)
        linha_topo_produtos.addLayout(topo_busca_quant)
        linha_topo_produtos.addLayout(topo_busca_unit)

        self.label_prod = QLabel("PRODUTOS")
        self.label_prod.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_prod.setFixedHeight(22)
        self.label_prod.setStyleSheet("""
            QLabel {
                font: bold;
                color: orange;
                background-color: #031740;
                font-size: 12px;
                border: none;
                padding: 0px;
                margin: 0px;
                border-radius: 0px;
            }
        """)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(8)
        self.tabela.setRowCount(12)
        self.tabela.setHorizontalHeaderLabels([
            "Item",
            "Cód",
            "Descrição",
            "UN",
            "Quant",
            "Preço Unit.",
            "Preço c/ Desc.",
            "Total Unitário"
        ])
        self.tabela.setContentsMargins(0, 0, 0, 0)
        self.tabela.setFrameShape(QFrame.Shape.NoFrame)
        self.tabela.setShowGrid(True)
        self.tabela.setGridStyle(Qt.PenStyle.SolidLine)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.tabela.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.verticalHeader().setDefaultSectionSize(26)
        self.tabela.horizontalHeader().setFixedHeight(28)

        self.tabela.setStyleSheet("""
            QTableWidget {
                background: white;
                alternate-background-color: #f7f9fc;
                border: 1px solid #cfd6dd;
                gridline-color: #c7ced6;
                font-size: 12px;
            }

            QHeaderView::section {
                background: #2f4b87;
                color: white;
                font-weight: bold;
                border-right: 1px solid #243866;
                border-bottom: 1px solid #243866;
                padding: 4px;
            }

            QTableWidget::item {
                border-right: 1px solid #d4d8dd;
                border-bottom: 1px solid #d4d8dd;
                padding-left: 4px;
            }

            QTableWidget::item:selected {
                background: #dbe8ff;
                color: black;
            }
        """)

        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)

        self.tabela.setColumnWidth(0, 55)
        self.tabela.setColumnWidth(1, 80)
        self.tabela.setColumnWidth(3, 50)
        self.tabela.setColumnWidth(4, 80)
        self.tabela.setColumnWidth(5, 110)
        self.tabela.setColumnWidth(6, 120)
        self.tabela.setColumnWidth(7, 120)

        bloco_produtos = QVBoxLayout()
        bloco_produtos.setContentsMargins(0, 0, 0, 0)
        bloco_produtos.setSpacing(6)
        bloco_produtos.addLayout(linha_topo_produtos)
        bloco_produtos.addWidget(self.label_prod)
        bloco_produtos.addWidget(self.tabela, 1)

        self.label_localizacao = criar_label_padrao()
        self.label_localizacao.setText("Localização:")
        self.label_localizacao.setFixedSize(self.label_localizacao.sizeHint())

        label_rua = criar_label_padrao()
        label_rua.setText("Rua")
        label_rua.setFixedSize(label_rua.sizeHint())

        label_bloco = criar_label_padrao()
        label_bloco.setText("Bloco")
        label_bloco.setFixedSize(label_bloco.sizeHint())

        label_prateleira = criar_label_padrao()
        label_prateleira.setText("Prateleira")
        label_prateleira.setFixedSize(label_prateleira.sizeHint())

        label_gaveta = criar_label_padrao()
        label_gaveta.setText("Gaveta")
        label_gaveta.setFixedSize(label_gaveta.sizeHint())

        self.valor_rua = criar_lineedit_padrao()
        self.valor_rua.setReadOnly(True)
        self.valor_rua.setFixedWidth(150)

        self.valor_bloco = criar_lineedit_padrao()
        self.valor_bloco.setReadOnly(True)
        self.valor_bloco.setFixedWidth(150)

        self.valor_prateleira = criar_lineedit_padrao()
        self.valor_prateleira.setReadOnly(True)
        self.valor_prateleira.setFixedWidth(150)

        self.valor_gaveta = criar_lineedit_padrao()
        self.valor_gaveta.setReadOnly(True)
        self.valor_gaveta.setFixedWidth(150)

        linha_localizacao = QHBoxLayout()
        linha_localizacao.setAlignment(Qt.AlignmentFlag.AlignLeft)
        linha_localizacao.addWidget(self.label_localizacao)
        linha_localizacao.addWidget(label_rua)
        linha_localizacao.addWidget(self.valor_rua)
        linha_localizacao.addWidget(label_bloco)
        linha_localizacao.addWidget(self.valor_bloco)
        linha_localizacao.addWidget(label_prateleira)
        linha_localizacao.addWidget(self.valor_prateleira)
        linha_localizacao.addWidget(label_gaveta)
        linha_localizacao.addWidget(self.valor_gaveta)

        self.label_aplicacao = criar_label_padrao()
        self.label_aplicacao.setText("Aplicação:")
        self.label_aplicacao.setFixedSize(self.label_aplicacao.sizeHint())

        self.valor_aplicacao = criar_lineedit_padrao()
        self.valor_aplicacao.setReadOnly(True)

        linha_aplicacao = QHBoxLayout()
        linha_aplicacao.addWidget(self.label_aplicacao)
        linha_aplicacao.setSpacing(17)
        linha_aplicacao.addWidget(self.valor_aplicacao)

        def criar_botao(texto):
            botao = QPushButton(texto)
            botao.setFixedHeight(40)
            botao.setStyleSheet("""
                QPushButton {
                    background-color: #031740;
                    color: white;
                    font-weight: bold;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #030C26;
                }
            """)
            return botao

        self.btn_novo = criar_botao("F5 - Novo")
        self.btn_gravar = criar_botao("F12 - Finalizar")
        self.btn_cancelar = criar_botao("F3 - Cancelar")

        linha_botoes = QHBoxLayout()
        linha_botoes.setSpacing(10)
        linha_botoes.addWidget(self.btn_novo)
        linha_botoes.addWidget(self.btn_gravar)
        linha_botoes.addWidget(self.btn_cancelar)

        bloco_esquerdo_inf = QVBoxLayout()
        bloco_esquerdo_inf.setSpacing(6)
        bloco_esquerdo_inf.addLayout(linha_localizacao)
        bloco_esquerdo_inf.addLayout(linha_aplicacao)
        bloco_esquerdo_inf.addLayout(linha_botoes)

        self.label_foto = QLabel()
        self.label_foto.setFixedSize(180, 140)
        self.label_foto.setStyleSheet("""
            QLabel {
                background: white;
                border: 1px solid #cfd6dd;
            }
        """)
        self.label_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_foto.setScaledContents(True)
        self.label_foto.setText("Sem foto")

        linha_inferior = QHBoxLayout()
        linha_inferior.setSpacing(15)
        linha_inferior.addLayout(bloco_esquerdo_inf, 1)
        linha_inferior.addWidget(self.label_foto)

        bloco_produtos.addLayout(linha_inferior)

        layout_quadro.addLayout(topo)
        layout_quadro.addWidget(linha)
        layout_quadro.addLayout(linha_dados)
        layout_quadro.addLayout(bloco_produtos, 1)

        self.quadro.setLayout(layout_quadro)

        layout_centro = QHBoxLayout()
        layout_centro.setSpacing(30)
        layout_centro.addLayout(layout_botoes)
        layout_centro.addWidget(self.quadro)

        layout_geral = QVBoxLayout()
        layout_geral.addWidget(titulo)
        layout_geral.addLayout(layout_centro)

        self.setLayout(layout_geral)
        self.atualizar_data_hora()

    def atualizar_data_hora(self):
        agora = QDateTime.currentDateTime()
        self.label_data.setText(agora.toString("dd/MM/yyyy HH:mm:ss"))

    def sair(self):
        from movimentacao.tela_movimentacao import TelaMovimentacao
        self.janela = TelaMovimentacao()
        self.janela.show()
        self.close()

    def abrir_pesquisa_produto(self):
        from consulta.tela_pesq_prod_mov import TelaConsProd
        self.tela_pesquisa = TelaConsProd(self)
        self.tela_pesquisa.show()

    def receber_produto_pesquisa(self, produto):
        self.produto_atual = produto

        self.edit_busca_produto.setText(str(produto.get("descricao") or ""))
        self.edit_unitario_item.setText(str(produto.get("preco_venda") or "0,00"))

        self.valor_rua.setText(str(produto.get("rua") or ""))
        self.valor_bloco.setText(str(produto.get("bloco") or ""))
        self.valor_prateleira.setText(str(produto.get("prateleira") or ""))
        self.valor_gaveta.setText(str(produto.get("gaveta") or ""))
        self.valor_aplicacao.setText(str(produto.get("aplicacao") or ""))

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

        self.edit_quantidade_item.setFocus()
        self.edit_quantidade_item.selectAll()

    def criar_item(self, texto="", editavel=False):
        item = QTableWidgetItem(texto)
        if not editavel:
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item

    def linha_vazia(self):
        for i in range(self.tabela.rowCount()):
            item_descricao = self.tabela.item(i, 2)
            if not item_descricao or not item_descricao.text().strip():
                return i
        return -1

    def texto_float(self, texto):
        texto = (texto or "").strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            return 0.0

    def formatar_decimal(self, valor):
        return f"{valor:.2f}".replace(".", ",")

    def atualizar_linha_tabela(self, linha):
        item_qtd = self.tabela.item(linha, 4)
        item_preco = self.tabela.item(linha, 5)

        if not item_qtd or not item_preco:
            return

        quantidade = self.texto_float(item_qtd.text())
        preco = self.texto_float(item_preco.text())
        total = quantidade * preco

        self.bloquear_tratamento_tabela = True
        self.tabela.blockSignals(True)

        item_qtd.setText(self.formatar_decimal(quantidade))
        item_preco.setText(self.formatar_decimal(preco))

        item_desc = self.tabela.item(linha, 6)
        if not item_desc:
            item_desc = self.criar_item("0,00", editavel=False)
            self.tabela.setItem(linha, 6, item_desc)
        item_desc.setText(self.formatar_decimal(preco))

        item_total = self.tabela.item(linha, 7)
        if not item_total:
            item_total = self.criar_item("0,00", editavel=False)
            self.tabela.setItem(linha, 7, item_total)
        item_total.setText(self.formatar_decimal(total))

        self.tabela.blockSignals(False)
        self.bloquear_tratamento_tabela = False

    def remover_linha_tabela(self, linha):
        self.bloquear_tratamento_tabela = True
        self.tabela.blockSignals(True)

        for col in range(self.tabela.columnCount()):
            self.tabela.setItem(linha, col, self.criar_item("", editavel=False))

        self.tabela.blockSignals(False)
        self.bloquear_tratamento_tabela = False

        self.renumerar_itens_tabela()
        self.edit_busca_produto.setFocus()

    def renumerar_itens_tabela(self):
        self.bloquear_tratamento_tabela = True
        self.tabela.blockSignals(True)

        contador = 1
        for linha in range(self.tabela.rowCount()):
            item_desc = self.tabela.item(linha, 2)
            if item_desc and item_desc.text().strip():
                item_num = self.tabela.item(linha, 0)
                if not item_num:
                    item_num = self.criar_item("", editavel=False)
                    self.tabela.setItem(linha, 0, item_num)
                item_num.setText(str(contador))
                contador += 1
            else:
                item_num = self.tabela.item(linha, 0)
                if item_num:
                    item_num.setText("")

        self.tabela.blockSignals(False)
        self.bloquear_tratamento_tabela = False

    def limpar_info_produto(self):
        self.valor_rua.clear()
        self.valor_bloco.clear()
        self.valor_prateleira.clear()
        self.valor_gaveta.clear()
        self.valor_aplicacao.clear()
        self.label_foto.clear()
        self.label_foto.setText("Sem foto")

    def adicionar_produto_tabela(self):
        descricao = self.edit_busca_produto.text().strip()
        if not descricao:
            return

        if not self.produto_atual:
            return

        linha = self.linha_vazia()
        if linha < 0:
            return

        codigo = str(self.produto_atual.get("codigo") or "")
        unidade = str(self.produto_atual.get("un_venda") or "")
        quantidade = self.texto_float(self.edit_quantidade_item.text())
        preco = self.texto_float(self.edit_unitario_item.text())

        self.bloquear_tratamento_tabela = True
        self.tabela.blockSignals(True)

        self.tabela.setItem(linha, 0, self.criar_item(str(linha + 1), editavel=False))
        self.tabela.setItem(linha, 1, self.criar_item(codigo, editavel=False))
        self.tabela.setItem(linha, 2, self.criar_item(descricao, editavel=False))
        self.tabela.setItem(linha, 3, self.criar_item(unidade, editavel=False))
        self.tabela.setItem(linha, 4, self.criar_item(self.formatar_decimal(quantidade), editavel=True))
        self.tabela.setItem(linha, 5, self.criar_item(self.formatar_decimal(preco), editavel=True))
        self.tabela.setItem(linha, 6, self.criar_item(self.formatar_decimal(preco), editavel=False))
        self.tabela.setItem(linha, 7, self.criar_item(self.formatar_decimal(quantidade * preco), editavel=False))

        self.tabela.blockSignals(False)
        self.bloquear_tratamento_tabela = False

        self.edit_busca_produto.clear()
        self.edit_quantidade_item.setText("0,00")
        self.edit_unitario_item.setText("0,00")
        self.limpar_info_produto()
        self.edit_busca_produto.setFocus()

    def ir_para_unitario(self):
        self.edit_unitario_item.setFocus()
        self.edit_unitario_item.selectAll()


    def ir_para_tabela_quantidade(self):
        for linha in range(self.tabela.rowCount()):
            item_descricao = self.tabela.item(linha, 2)
            item_quantidade = self.tabela.item(linha, 4)

            if item_descricao and item_descricao.text().strip() and item_quantidade:
                self.tabela.setFocus()
                self.tabela.setCurrentCell(linha, 4)
                return


    def clicar_tabela(self, linha, coluna):
        item_descricao = self.tabela.item(linha, 2)
        if not item_descricao or not item_descricao.text().strip():
            return

        if coluna == 4:
            self.tabela.setCurrentCell(linha, 4)
            item = self.tabela.item(linha, 4)
            if item:
                self.tabela.editItem(item)

        elif coluna == 5:
            self.tabela.setCurrentCell(linha, 5)
            item = self.tabela.item(linha, 5)
            if item:
                self.tabela.editItem(item)

    def descer_tabela_quantidade(self):
        linha = self.tabela.currentRow()
        coluna = self.tabela.currentColumn()

        if linha < 0:
            return

        proxima_linha = linha + 1
        if proxima_linha >= self.tabela.rowCount():
            return

        item_descricao = self.tabela.item(proxima_linha, 2)
        if not item_descricao or not item_descricao.text().strip():
            return

        if coluna not in (4, 5):
            coluna = 4

        self.tabela.setCurrentCell(proxima_linha, coluna)


    def subir_tabela_quantidade(self):
        linha = self.tabela.currentRow()
        coluna = self.tabela.currentColumn()

        if linha <= 0:
            return

        linha_anterior = linha - 1

        item_descricao = self.tabela.item(linha_anterior, 2)
        if not item_descricao or not item_descricao.text().strip():
            return

        if coluna not in (4, 5):
            coluna = 4

        self.tabela.setCurrentCell(linha_anterior, coluna)


    def tratar_edicao_tabela(self, item):
        if self.bloquear_tratamento_tabela:
            return

        if not item:
            return

        linha = item.row()
        coluna = item.column()

        if coluna not in (4, 5):
            return

        item_desc = self.tabela.item(linha, 2)
        if not item_desc or not item_desc.text().strip():
            return

        texto = item.text().strip()

        if not texto:
            item.setText("0,00")
            return

        texto_teste = texto.replace(",", ".")

        try:
            valor = float(texto_teste)
        except ValueError:
            self.bloquear_tratamento_tabela = True
            item.setText("0,00")
            self.bloquear_tratamento_tabela = False
            return

        if coluna == 4 and valor == 0:
            self.remover_linha_tabela(linha)
            return

        self.bloquear_tratamento_tabela = True
        item.setText(self.formatar_decimal(valor))
        self.bloquear_tratamento_tabela = False

        self.atualizar_linha_tabela(linha)



    def enter_tabela(self):
        linha = self.tabela.currentRow()
        coluna = self.tabela.currentColumn()

        if linha < 0:
            return

        item_desc = self.tabela.item(linha, 2)
        if not item_desc or not item_desc.text().strip():
            return

        if coluna == 4:
            item_quantidade = self.tabela.item(linha, 4)
            if not item_quantidade:
                return

            quantidade = self.texto_float(item_quantidade.text())
            if quantidade == 0:
                self.remover_linha_tabela(linha)
                return

            self.atualizar_linha_tabela(linha)

            item_preco = self.tabela.item(linha, 5)
            if item_preco:
                self.tabela.setCurrentCell(linha, 5)
                self.tabela.editItem(item_preco)
            return

        if coluna == 5:
            self.atualizar_linha_tabela(linha)

            item_quantidade = self.tabela.item(linha, 4)
            if item_quantidade:
                self.tabela.setCurrentCell(linha, 4)
                self.tabela.editItem(item_quantidade)


    def keyPressEvent(self, event):
        if self.tabela.hasFocus():
            linha = self.tabela.currentRow()
            coluna = self.tabela.currentColumn()

            if linha >= 0 and coluna in (4, 5):
                texto = event.text()

                if texto and (texto.isdigit() or texto in ",."):
                    item = self.tabela.item(linha, coluna)
                    if item:
                        self.tabela.editItem(item)

                        editor = self.tabela.findChild(QLineEdit)
                        if editor:
                            editor.setText(texto)
                    return

        super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(gerar_estilo())
    janela = TelaSaida()
    janela.show()
    sys.exit(app.exec())