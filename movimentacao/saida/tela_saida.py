import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..')))

from util.padrao import criar_label_padrao, criar_lineedit_padrao
from util.fun_basicas import LineEditComEnter
from util.estilo import gerar_estilo
from PyQt6.QtGui import QShortcut, QKeySequence, QIcon
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QHBoxLayout, QLineEdit,
    QTableWidget, QHeaderView, QAbstractItemView
)

from movimentacao.saida.funcao_venda import (
    abrir_pesquisa_produto,
    abrir_pesquisa_ao_digitar,
    receber_produto_pesquisa,
    ir_para_unitario,
    criar_item,
    limpar_info_produto,
    adicionar_produto_tabela,
    ir_para_tabela_quantidade,
    event_filter_tabela,
    tratar_edicao_tabela,
    destacar_linha_atual,
    texto_para_float,
    formatar_valor,
    atualizar_info_produto_tabela,
    atualizar_totais,
    renumerar_itens_tabela,
    novo
)


class TelaSaida(QWidget):
    def __init__(self, tela_origem=None):
        super().__init__()
        self.tela_origem = tela_origem
        self.setWindowTitle('Saída')
        self.setWindowIcon(QIcon('imagens/icone.png'))
        self.produto_atual = None

        self.componentes()
        self.showMaximized()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)

        self.edit_busca_produto.textEdited.connect(self.abrir_pesquisa_ao_digitar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_data_hora)
        self.timer.start(1000)

        self.atalho_f8_produto = QShortcut(
            QKeySequence('F8'), self.edit_busca_produto)
        self.atalho_f8_produto.setContext(Qt.ShortcutContext.WidgetShortcut)
        self.atalho_f8_produto.activated.connect(
            lambda: self.abrir_pesquisa_produto(self.edit_busca_produto.text())
        )

        self.atalho_f8_quantidade = QShortcut(
            QKeySequence('F8'), self.edit_quantidade_item
        )
        self.atalho_f8_quantidade.setContext(Qt.ShortcutContext.WidgetShortcut)
        self.atalho_f8_quantidade.activated.connect(
            lambda: self.abrir_pesquisa_produto(self.edit_busca_produto.text())
        )

        self.atalho_f8_tabela = QShortcut(QKeySequence('F8'), self.tabela)
        self.atalho_f8_tabela.setContext(Qt.ShortcutContext.WidgetShortcut)
        self.atalho_f8_tabela.activated.connect(
            lambda: self.abrir_pesquisa_produto(self.edit_busca_produto.text())
        )

        self.atalho_f8_vendedor = QShortcut(
            QKeySequence('F8'), self.edit_vendedor
        )
        self.atalho_f8_vendedor.setContext(Qt.ShortcutContext.WidgetShortcut)
        self.atalho_f8_vendedor.activated.connect(self.abrir_pesquisa_vendedor)

        self.atalho_f8_cod_vendedor = QShortcut(
            QKeySequence('F8'), self.cod_vendedor
        )
        self.atalho_f8_cod_vendedor.setContext(Qt.ShortcutContext.WidgetShortcut)
        self.atalho_f8_cod_vendedor.activated.connect(
            self.abrir_pesquisa_vendedor
        )

        QShortcut(QKeySequence('Ctrl+D'), self).activated.connect(
            self.focar_desconto
        )

        self.tabela.installEventFilter(self)

        self.edit_quantidade_item.returnPressed.connect(self.ir_para_unitario)
        self.edit_unitario_item.returnPressed.connect(
            self.adicionar_produto_tabela
        )
        self.edit_busca_produto.returnPressed.connect(
            self.ir_para_tabela_quantidade
        )

        self.tabela.itemChanged.connect(self.tratar_edicao_tabela)
        self.tabela.currentCellChanged.connect(self.destacar_linha_atual)
        self.tabela.currentCellChanged.connect(
            self.atualizar_info_produto_tabela
        )

        self.edit_desconto.textChanged.connect(self.atualizar_totais)

        QShortcut(QKeySequence('F5'), self).activated.connect(self.novo)
        QShortcut(QKeySequence('F3'), self).activated.connect(
            self.focar_cod_vendedor
        )
        QShortcut(QKeySequence('F6'), self).activated.connect(
            self.focar_cod_cliente
        )

        QShortcut(QKeySequence('F12'), self).activated.connect(self.abrir_tela_pagamento)

        self.edit_busca_produto.setFocus()

        self.cod_vendedor.returnPressed.connect(self.buscar_vendedor_por_codigo)

        # -------- CLIENTE --------
        self.cod_cliente.returnPressed.connect(self.buscar_cliente_por_codigo)
        self.cod_cliente.returnPressed.connect(self.ir_para_nome_cliente)

        self.atalho_enter_cliente = QShortcut(
            QKeySequence('Return'), self.edit_cliente
        )
        self.atalho_enter_cliente.setContext(
            Qt.ShortcutContext.WidgetShortcut
        )
        self.atalho_enter_cliente.activated.connect(
            self.tratar_enter_cliente
        )

        self.atalho_enter2_cliente = QShortcut(
            QKeySequence('Enter'), self.edit_cliente
        )
        self.atalho_enter2_cliente.setContext(
            Qt.ShortcutContext.WidgetShortcut
        )
        self.atalho_enter2_cliente.activated.connect(
            self.tratar_enter_cliente
        )

        self.atalho_f8_cliente = QShortcut(
            QKeySequence('F8'), self.edit_cliente
        )
        self.atalho_f8_cliente.setContext(
            Qt.ShortcutContext.WidgetShortcut
        )
        self.atalho_f8_cliente.activated.connect(
            self.abrir_pesquisa_cliente
        )

        self.atalho_f8_cod_cliente = QShortcut(
            QKeySequence('F8'), self.cod_cliente
        )
        self.atalho_f8_cod_cliente.setContext(
            Qt.ShortcutContext.WidgetShortcut
        )
        self.atalho_f8_cod_cliente.activated.connect(
            self.abrir_pesquisa_cliente
        )

        self.carregar_proximo_numero_orcamento()

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
        self.botao_faturar = QPushButton("Consultar/Faturar")
        self.botao_consultas = QPushButton("Notas Fiscais - NFE")
        self.botao_relatorios = QPushButton("Relatórios")
        self.botao_sair = QPushButton("ESC - Sair")
        self.botao_sair.clicked.connect(self.sair)

        for botao in [self.botao_venda, self.botao_faturar, self.botao_consultas, self.botao_relatorios, self.botao_sair]:
            botao.setFixedSize(180, 60)
            botao.setStyleSheet("""
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
        layout_botoes.addWidget(self.botao_faturar)
        layout_botoes.addWidget(self.botao_consultas)
        layout_botoes.addWidget(self.botao_relatorios)
        layout_botoes.addStretch()
        layout_botoes.addWidget(self.botao_sair)

        layout_quadro = QVBoxLayout()
        layout_quadro.setContentsMargins(20, 10, 20, 10)
        layout_quadro.setSpacing(8)

        self.label_num = QLabel("Nº :")
        self.label_num.setStyleSheet(
            "font-size:14px; font-weight:bold; color:#031740;")

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


        self.label_tipo = QLabel("Orçamento")
        self.label_tipo.setStyleSheet("""
            QLabel {
                background: transparent;
                color: #031740;
                font-weight: bold;
                font-size: 20px;
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
        topo_dir.addWidget(self.label_tipo)
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
        self.cod_cliente.setPlaceholderText("F6")

        self.edit_cliente = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cliente.setMinimumWidth(500)
        self.edit_cliente.setPlaceholderText("F8 - Pesquisa clientes")

        self.label_cpf_cliente = criar_label_padrao()
        self.label_cpf_cliente.setText("CPF")
        self.label_cpf_cliente.setFixedSize(self.label_cpf_cliente.sizeHint())

        self.edit_cpf_cliente = criar_lineedit_padrao(LineEditComEnter)
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
        self.cod_vendedor.setPlaceholderText("F3")

        self.edit_vendedor = criar_lineedit_padrao(LineEditComEnter)
        self.edit_vendedor.setFixedWidth(150)
        self.edit_vendedor.setPlaceholderText("F8 - Pesquisa vendedor")

        self.label_desconto = criar_label_padrao()
        self.label_desconto.setText("Desconto:")
        self.label_desconto.setFixedSize(self.label_desconto.sizeHint())

        self.edit_desconto = criar_lineedit_padrao(LineEditComEnter)
        self.edit_desconto.setFixedWidth(70)
        self.edit_desconto.setPlaceholderText("Ctrl+D")

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
        bloco_esquerdo.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
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
        self.label_total_prod_titulo.setFixedSize(
            self.label_total_prod_titulo.sizeHint())

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
        self.label_busca_produto.setFixedSize(
            self.label_busca_produto.sizeHint())

        self.label_quantidade = criar_label_padrao()
        self.label_quantidade.setText("Quantidade")
        self.label_quantidade.setFixedSize(self.label_quantidade.sizeHint())

        self.label_unitario = criar_label_padrao()
        self.label_unitario.setText("Unitário")
        self.label_unitario.setFixedSize(self.label_unitario.sizeHint())

        self.edit_busca_produto = criar_lineedit_padrao()
        self.edit_busca_produto.setMinimumHeight(34)
        self.edit_busca_produto.setPlaceholderText(
            'Digite para buscar ou tecle F8')

        self.edit_quantidade_item = QLineEdit()
        self.edit_quantidade_item.setFixedSize(120, 34)
        self.edit_quantidade_item.setText("0,00")

        self.edit_unitario_item = criar_lineedit_padrao()
        self.edit_unitario_item.setFixedSize(120, 34)
        self.edit_unitario_item.setText("0,00")

        self.edit_quantidade_item.setStyleSheet(
            self.edit_unitario_item.styleSheet())

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
        self.tabela.setRowCount(0)
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
        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems)
        self.tabela.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)
        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
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
        linha_aplicacao.setSpacing(17)
        linha_aplicacao.addWidget(self.label_aplicacao)
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
        self.btn_novo.clicked.connect(self.novo)

        self.btn_gravar = criar_botao("F12 - Finalizar")
        self.btn_gravar.clicked.connect(self.abrir_tela_pagamento)

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

        self.label_foto = QLabel("Sem foto")
        self.label_foto.setFixedSize(180, 140)
        self.label_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_foto.setStyleSheet("""
            QLabel {
                background: white;
                border: 1px solid #cfd6dd;
            }
        """)

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
        if self.tela_origem:
            self.tela_origem.show()
        self.close()

    def abrir_pesquisa_produto(self, texto_inicial=""):
        return abrir_pesquisa_produto(self, texto_inicial)

    def abrir_pesquisa_ao_digitar(self, texto):
        return abrir_pesquisa_ao_digitar(self, texto)

    def receber_produto_pesquisa(self, produto):
        return receber_produto_pesquisa(self, produto)

    def ir_para_unitario(self):
        return ir_para_unitario(self)

    def criar_item(self, texto=""):
        return criar_item(self, texto)

    def limpar_info_produto(self):
        return limpar_info_produto(self)

    def adicionar_produto_tabela(self):
        return adicionar_produto_tabela(self)

    def ir_para_tabela_quantidade(self):
        return ir_para_tabela_quantidade(self)

    def eventFilter(self, obj, event):
        return event_filter_tabela(self, obj, event)

    def tratar_edicao_tabela(self, item):
        return tratar_edicao_tabela(self, item)

    def destacar_linha_atual(self, linha_atual, coluna_atual, linha_anterior, coluna_anterior):
        return destacar_linha_atual(
            self, linha_atual, coluna_atual, linha_anterior, coluna_anterior
        )

    def texto_para_float(self, texto):
        return texto_para_float(self, texto)

    def formatar_valor(self, valor):
        return formatar_valor(self, valor)

    def atualizar_info_produto_tabela(self, linha_atual, coluna_atual, linha_anterior, coluna_anterior):
        return atualizar_info_produto_tabela(
            self, linha_atual, coluna_atual, linha_anterior, coluna_anterior
        )

    def atualizar_totais(self):
        return atualizar_totais(self)

    def renumerar_itens_tabela(self):
        return renumerar_itens_tabela(self)

    def novo(self):
        if hasattr(self, "cliente_rapido"):
            del self.cliente_rapido

        return novo(self)


    def focar_desconto(self):
        self.edit_desconto.setFocus()
        self.edit_desconto.selectAll()

    def abrir_pesquisa_vendedor(self):
        from consulta.tela_pesq_funcionario import TelaPesqFuncionario
        self.tela_pesq_vendedor = TelaPesqFuncionario(self)
        self.tela_pesq_vendedor.exec()

    def selecionar_vendedor(self, codigo, nome):
        self.cod_vendedor.setText(codigo)
        self.edit_vendedor.setText(nome)
        self.edit_busca_produto.setFocus()

    def focar_cod_vendedor(self):
        self.cod_vendedor.setFocus()
        self.cod_vendedor.selectAll()

    def buscar_vendedor_por_codigo(self):
        codigo = self.cod_vendedor.text().strip()

        if not codigo:
            self.edit_vendedor.setFocus()
            self.edit_vendedor.selectAll()
            return

        from entidades.funcionario.funcionario_service import FuncionarioService
        from PyQt6.QtWidgets import QMessageBox

        service = FuncionarioService()
        vendedor = service.buscar_por_codigo(codigo)

        if not vendedor:
            QMessageBox.warning(self, "Aviso", "Vendedor não encontrado.")
            self.cod_vendedor.setFocus()
            self.cod_vendedor.selectAll()
            return

        nome_vendedor = (
            vendedor.get("apelido")
            or vendedor.get("nome")
            or vendedor.get("nome_funcionario")
            or ""
        )

        self.edit_vendedor.setText(nome_vendedor)
        self.edit_busca_produto.setFocus()
        self.edit_busca_produto.selectAll()

    def abrir_pesquisa_cliente(self):
        from consulta.tela_pesq_cliente import TelaPesqCliente
        self.tela_pesq_cliente = TelaPesqCliente(self)
        self.tela_pesq_cliente.exec()

    def selecionar_cliente(self, codigo, nome, cpf):
        self.cod_cliente.setText(codigo)
        self.edit_cliente.setText(nome)
        self.edit_cpf_cliente.setText(cpf)

        self.edit_cliente.setReadOnly(True)
        self.edit_cpf_cliente.setReadOnly(True)

        self.edit_cpf_cliente.setFocus()
        self.edit_cpf_cliente.selectAll()

    def focar_cod_cliente(self):
        self.cod_cliente.setFocus()
        self.cod_cliente.selectAll()

    def ir_para_nome_cliente(self):
        if self.cod_cliente.text().strip():
            if self.edit_cliente.text().strip():
                self.cod_vendedor.setFocus()
                self.cod_vendedor.selectAll()
                return

        self.edit_cliente.setFocus()
        self.edit_cliente.selectAll()


    def limpar_cliente(self):
        self.cod_cliente.clear()
        self.edit_cliente.clear()
        self.edit_cpf_cliente.clear()

        self.edit_cliente.setReadOnly(False)
        self.edit_cpf_cliente.setReadOnly(False)

        self.edit_cliente.setFocus()

    def buscar_cliente_por_codigo(self):
        codigo = self.cod_cliente.text().strip()

        if not codigo:
            return

        if codigo == "0":
            self.limpar_cliente()
            return

        from entidades.cliente.cliente_service import ClienteService
        from PyQt6.QtWidgets import QMessageBox

        service = ClienteService()
        cliente = service.buscar_por_codigo(codigo)

        if not cliente:
            QMessageBox.warning(self, "Aviso", "Cliente não encontrado.")
            self.cod_cliente.setFocus()
            self.cod_cliente.selectAll()
            return

        nome = (
            cliente.get("nome")
            or cliente.get("nome_fantasia")
            or cliente.get("razao_social")
            or ""
        )
        cpf = cliente.get("cpf_cnpj", "")

        self.edit_cliente.setText(nome)
        self.edit_cpf_cliente.setText(cpf)
        self.edit_cliente.setReadOnly(True)
        self.edit_cpf_cliente.setReadOnly(True)

    def abrir_cliente_rapido(self, texto):
        texto = texto.strip()

        if not texto:
            return

        if self.cod_cliente.text().strip():
            return

        from consulta.tela_cliente_rapido import TelaClienteRapido

        dados_iniciais = getattr(self, "cliente_rapido", None)

        self.tela_cliente_rapido = TelaClienteRapido(
            self,
            nome_inicial=texto,
            dados_iniciais=dados_iniciais
        )
        self.tela_cliente_rapido.exec()

    def receber_cliente_rapido(self, dados):
        self.cliente_rapido = {
            "nome": dados.get("nome", "").strip(),
            "cpf": dados.get("cpf", "").strip(),
            "telefone": dados.get("telefone", "").strip(),
            "cep": dados.get("cep", "").strip(),
            "endereco": dados.get("endereco", "").strip(),
            "numero": dados.get("numero", "").strip(),
            "bairro": dados.get("bairro", "").strip(),
            "cidade": dados.get("cidade", "").strip(),
            "uf": dados.get("uf", "").strip(),
        }

        self.cod_cliente.clear()
        self.edit_cliente.setText(self.cliente_rapido["nome"])
        self.edit_cpf_cliente.setText(self.cliente_rapido["cpf"])

        self.edit_cliente.setReadOnly(False)
        self.edit_cpf_cliente.setReadOnly(False)

        self.cod_vendedor.setFocus()
        self.cod_vendedor.selectAll()

    def tratar_enter_cliente(self):
        texto = self.edit_cliente.text().strip()

        if texto:
            self.abrir_cliente_rapido(texto)
            return

        self.cod_vendedor.setFocus()
        self.cod_vendedor.selectAll()


    def salvar_orcamento(self):
        self.abrir_tela_pagamento()


        
    def salvar_itens_orcamento(self, cursor, id_orcamento):
        from movimentacao.saida.funcao_venda import salvar_itens_orcamento
        return salvar_itens_orcamento(self, cursor, id_orcamento)

    def carregar_proximo_numero_orcamento(self):
        from movimentacao.saida.funcao_venda import carregar_proximo_numero_orcamento
        return carregar_proximo_numero_orcamento(self)


    def abrir_tela_pagamento(self):
        from movimentacao.tela_pagamento import TelaPagamento

        self.tela_pagamento = TelaPagamento(self)
        self.tela_pagamento.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(gerar_estilo())
    janela = TelaSaida()
    janela.show()
    sys.exit(app.exec())