from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence, QDoubleValidator, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.estilo import gerar_estilo
from util.padrao import (
    criar_botao,
    criar_tab_widget,
    criar_botao_sair,
    criar_botao_salvar,
    criar_label_padrao,
    criar_combobox_padrao,
    criar_lineedit_padrao)
from util.fun_basicas import(LineEditComEnter)
from util.fun_basicas import texto_para_float, formatar_preco
from bd import salvar_produto, listar_produtos, atualizar_produto, pesquisar_produtos_avancado, excluir_produto as excluir_produto_bd


class CadProd(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Produtos')
        self.setWindowIcon(QIcon('imagens/icone.png'))
        self.componentes()
        self.showMaximized()
        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)
        QShortcut(QKeySequence('F5'), self).activated.connect(self.limpar_campos)
        QShortcut(QKeySequence('F8'), self).activated.connect(self.preencher_tabela)

        self.setTabOrder(self.edit_preco_custo, self.edit_preco_venda)
        self.setTabOrder(self.edit_preco_venda, self.edit_preco_promocao)
        self.setTabOrder(self.edit_preco_promocao, self.edit_margem_lucro)
        self.setTabOrder(self.edit_margem_lucro, self.edit_desconto)

        
    def componentes(self):
        nometela = QLabel('Cadastro de Produtos')
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
        self.comb_opc.addItems(["Descrição", "Código", "Cód. Barras", "Referências"])
        self.comb_opc.setFixedWidth(220)

        label_mdl = criar_label_padrao()
        label_mdl.setText('Modelo')
        label_mdl.setContentsMargins(2, 0, 0, 0)
        label_mdl.setFixedSize(label_mdl.sizeHint())

        self.comb_mdl = criar_combobox_padrao()
        self.comb_mdl.addItem('Iniciar com...')
        self.comb_mdl.setFixedWidth(220)

        label_pesq = criar_label_padrao()
        label_pesq.setText('Dados a pesquisar')
        label_pesq.setContentsMargins(2, 0, 0, 0)
        label_pesq.setFixedSize(label_pesq.sizeHint())

        self.check_todos = QCheckBox("Todos")
        self.check_todos.toggled.connect(self.acao_check_todos)

        self.edit_label_pesq = criar_lineedit_padrao()
        self.edit_label_pesq.setMinimumWidth(810)
        self.edit_label_pesq.textChanged.connect(self.acao_digitar_pesquisa)

        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc)
        vbox_opc.addWidget(self.comb_opc)

        vbox_mdl = QVBoxLayout()
        vbox_mdl.addWidget(label_mdl)
        vbox_mdl.addWidget(self.comb_mdl)

        hbox_pesq = QHBoxLayout()
        hbox_pesq.addWidget(label_pesq)
        hbox_pesq.addWidget(self.check_todos, alignment=Qt.AlignmentFlag.AlignRight)

        vbox_pesq = QVBoxLayout()
        vbox_pesq.addLayout(hbox_pesq)
        vbox_pesq.addWidget(self.edit_label_pesq)

        hbox_linha1 = QHBoxLayout()
        hbox_linha1.addLayout(vbox_opc)
        hbox_linha1.addLayout(vbox_mdl)
        hbox_linha1.addLayout(vbox_pesq)

        label_ativo = criar_label_padrao()
        label_ativo.setText('Ativo')
        label_ativo.setContentsMargins(2, 0, 0, 0)
        label_ativo.setFixedSize(label_ativo.sizeHint())

        self.combo_ativo = criar_combobox_padrao()
        self.combo_ativo.addItems(["Todos", "Ativo", "Inativo"])
        self.combo_ativo.setFixedWidth(220)

        self.btn_pesq = criar_botao()
        self.btn_pesq.setText("F8 - Pesquisa")
        self.btn_pesq.clicked.connect(self.preencher_tabela)  # chama função ao clicar

        hbox_linha2 = QHBoxLayout()
        hbox_linha2.addWidget(self.combo_ativo, alignment=Qt.AlignmentFlag.AlignLeft)
        hbox_linha2.addWidget(self.btn_pesq)

        vbox_linha2 = QVBoxLayout()
        vbox_linha2.addWidget(label_ativo, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_linha2.addLayout(hbox_linha2)

        # ---------- TABELA DE RESULTADOS ----------
        self.tabela_resultado = QTableWidget()
        self.tabela_resultado.setColumnCount(4)
        self.tabela_resultado.setHorizontalHeaderLabels(["Código", "Descrição", "Quant.", "Preço"])
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
        self.tabela_resultado.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_resultado.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_resultado.setAlternatingRowColors(True)
        self.tabela_resultado.setMinimumHeight(300)
        self.tabela_resultado.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        

        header = self.tabela_resultado.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.tabela_resultado.cellDoubleClicked.connect(self.carregar_produto)


        #botões controle novo, relatório
        self.botao_novo = criar_botao()
        self.botao_novo.setText('F5 - Novo')
        self.botao_novo.clicked.connect(self.limpar_campos)

        self.botao_relat = criar_botao()
        self.botao_relat.setText('Relatórios')

        self.botao_excluir = criar_botao()
        self.botao_excluir.setText("Excluir")
        self.botao_excluir.clicked.connect(self.excluir_produto)

        hbox_botoes_rodape = QHBoxLayout()
        hbox_botoes_rodape.setAlignment(Qt.AlignmentFlag.AlignCenter )
        hbox_botoes_rodape.addWidget(self.botao_novo)
        hbox_botoes_rodape.addSpacing(5)
        hbox_botoes_rodape.addWidget(self.botao_relat)
        hbox_botoes_rodape.addStretch()
        hbox_botoes_rodape.addWidget(self.botao_excluir)
        # hbox_botoes_rodape.addSpacing()


        layout_geral_aba1 = QVBoxLayout()
        layout_geral_aba1.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba1.addLayout(hbox_linha1)
        layout_geral_aba1.addLayout(vbox_linha2)
        layout_geral_aba1.addWidget(self.tabela_resultado)
        layout_geral_aba1.addSpacing(10)
        layout_geral_aba1.addLayout(hbox_botoes_rodape)
        layout_geral_aba1.addSpacing(10)

        aba1.setLayout(layout_geral_aba1)

        # criação aba 2 cadastro
        aba2 = QWidget()
        aba2.setStyleSheet('background-color: #cbcdce;')

        codigos = QLabel('CODIFICAÇÃO')
        codigos.setStyleSheet('font: bold; color: orange; background-color: #031740; font-size: 12px')
        codigos.setContentsMargins(2, 0, 0, 0)
        codigos.setMinimumWidth(650)
        codigos.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # código produto
        cod_prod = criar_label_padrao()
        cod_prod.setText('Código')
        cod_prod.setContentsMargins(2, 0, 0, 0)
        cod_prod.setFixedSize(cod_prod.sizeHint())

        self.edit_cod = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cod.setFixedWidth(90)
        self.edit_cod.setReadOnly(True)

        vbox_cod = QVBoxLayout()
        vbox_cod.addWidget(cod_prod)
        vbox_cod.addWidget(self.edit_cod)

        #código barras
        cod_barras = criar_label_padrao()
        cod_barras.setText('Cód. Barras')
        cod_barras.setContentsMargins(2, 0, 0, 0)
        cod_barras.setFixedSize(cod_barras.sizeHint())

        regex = QRegularExpression(r"\d{0,13}")
        validador = QRegularExpressionValidator(regex)

        self.edit_cod_barras = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cod_barras.setMaxLength(13)
        self.edit_cod_barras.setValidator(validador)
        self.edit_cod_barras.setFixedWidth(150)

        vbox_barras = QVBoxLayout()
        vbox_barras.addWidget(cod_barras)
        vbox_barras.addWidget(self.edit_cod_barras)

        #código barras 2
        cod_barras2 = criar_label_padrao()
        cod_barras2.setText('Cód. Barras 2')
        cod_barras2.setContentsMargins(2, 0, 0, 0)
        cod_barras2.setFixedSize(cod_barras2.sizeHint())

        self.edit_cod_barras2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cod_barras2.setMaxLength(13)
        self.edit_cod_barras2.setValidator(validador)
        self.edit_cod_barras2.setFixedWidth(150)

        vbox_barras2 = QVBoxLayout()
        vbox_barras2.addWidget(cod_barras2)
        vbox_barras2.addWidget(self.edit_cod_barras2)

        # código fornecedor
        ref_forn = criar_label_padrao()
        ref_forn.setText('Referencia fornecedor')
        ref_forn.setContentsMargins(2, 0, 0, 0)
        ref_forn.setFixedSize(ref_forn.sizeHint())

        self.edit_ref_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_ref_forn.setFixedWidth(150)
        
        vbox_ref_forn = QVBoxLayout()
        vbox_ref_forn.addWidget(ref_forn)
        vbox_ref_forn.addWidget(self.edit_ref_forn)

        # código original 
        ref_orig = criar_label_padrao()
        ref_orig.setText('Referencia original')
        ref_orig.setContentsMargins(2, 0, 0, 0)
        ref_orig.setFixedSize(ref_orig.sizeHint())

        self.edit_ref_orig = criar_lineedit_padrao(LineEditComEnter)
        self.edit_ref_orig.setFixedWidth(150)
        
        vbox_ref_orig = QVBoxLayout()
        vbox_ref_orig.addWidget(ref_orig)
        vbox_ref_orig.addWidget(self.edit_ref_orig)

        # código similar
        ref_similar = criar_label_padrao()
        ref_similar.setText('Referencias similares')
        ref_similar.setContentsMargins(2, 0, 0, 0)
        ref_similar.setFixedSize(ref_similar.sizeHint())

        self.edit_ref_similar = criar_lineedit_padrao(LineEditComEnter)
        self.edit_ref_similar.setMinimumWidth(150)

        vbox_ref_similar = QVBoxLayout()
        vbox_ref_similar.addWidget(ref_similar)
        vbox_ref_similar.addWidget(self.edit_ref_similar)


        # Apresentação
        apres = QLabel('APRESENTAÇÃO')
        apres.setStyleSheet('font: bold; color: orange; background-color: #031740; font-size: 12px')
        apres.setContentsMargins(2, 0, 0, 0)
        apres.setMinimumWidth(650)
        apres.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # descrição
        desc = criar_label_padrao()
        desc.setText('Descrição')
        desc.setContentsMargins(2, 0, 0, 0)
        desc.setFixedSize(desc.sizeHint())

        self.edit_desc = criar_lineedit_padrao(LineEditComEnter)
        self.edit_desc.setFixedWidth(500)

        vbox_desc = QVBoxLayout()
        vbox_desc.addWidget(desc)
        vbox_desc.addWidget(self.edit_desc)

        # aplicação
        aplic = criar_label_padrao()
        aplic.setText('Aplicação')
        aplic.setContentsMargins(2, 0, 0, 0)
        aplic.setFixedSize(aplic.sizeHint())

        self.edit_aplic = criar_lineedit_padrao(LineEditComEnter)
        self.edit_aplic.setMinimumWidth(550)

        vbox_aplic = QVBoxLayout()
        vbox_aplic.addWidget(aplic)
        vbox_aplic.addWidget(self.edit_aplic)

        # criação da tab apresentação
        self.tab_apresentacao = criar_tab_widget()
        self.tab_apresentacao.setFixedHeight(108)

        self.tab_apresentacao.setStyleSheet("""
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

        # criação da aba fornecedor dentro da apresentação 
        aba_abastecimento = QWidget()

        # estoque mínimo 
        estoque_minimo = criar_label_padrao()
        estoque_minimo.setText('Est. Mín.')
        estoque_minimo.setContentsMargins(2, 0, 0, 0)
        estoque_minimo.setFixedSize(estoque_minimo.sizeHint())

        self.edit_estoque_minimo = criar_lineedit_padrao(LineEditComEnter)
        self.edit_estoque_minimo.setFixedWidth(100)

        vbox_estoque_minimo = QVBoxLayout()
        vbox_estoque_minimo.addWidget(estoque_minimo)
        vbox_estoque_minimo.addWidget(self.edit_estoque_minimo)

        # código fornecedor 
        cod_forn = criar_label_padrao()
        cod_forn.setText('Cod. Forn.')
        cod_forn.setContentsMargins(2, 0, 0, 0)
        cod_forn.setFixedSize(cod_forn.sizeHint())

        self.edit_cod_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cod_forn.setFixedWidth(90)

        vbox_cod_forn = QVBoxLayout()
        vbox_cod_forn.addWidget(cod_forn)
        vbox_cod_forn.addWidget(self.edit_cod_forn)

        # nome fornecedor
        nome_forn = criar_label_padrao()
        nome_forn.setText('Fornecedor')
        nome_forn.setContentsMargins(2, 0, 0, 0)
        nome_forn.setFixedSize(nome_forn.sizeHint())

        pesc_forn = criar_label_padrao()
        pesc_forn.setText('F8 - Pesquisa')
        pesc_forn.setContentsMargins(0, 0, 5, 0)
        pesc_forn.setFixedSize(pesc_forn.sizeHint())

        hbox_nome_forn = QHBoxLayout()
        hbox_nome_forn.addWidget(nome_forn, alignment=Qt.AlignmentFlag.AlignLeft)
        hbox_nome_forn.addWidget(pesc_forn, alignment=Qt.AlignmentFlag.AlignRight)

        self.edit_nome_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_forn.setFixedWidth(320)

        vbox_nome_forn = QVBoxLayout()
        vbox_nome_forn.addLayout(hbox_nome_forn)
        vbox_nome_forn.addWidget(self.edit_nome_forn)

        # repositor
        repositor = criar_label_padrao()
        repositor.setText('Repositor')
        repositor.setContentsMargins(2, 0, 0, 0)
        repositor.setFixedSize(repositor.sizeHint())

        pesc_repositor = criar_label_padrao()
        pesc_repositor.setText('F8 - Pesquisa')
        pesc_repositor.setContentsMargins(0, 0, 5, 0)
        pesc_repositor.setFixedSize(pesc_repositor.sizeHint())

        hbox_repositor = QHBoxLayout()
        hbox_repositor.addWidget(repositor, alignment= Qt.AlignmentFlag.AlignLeft)
        hbox_repositor.addWidget(pesc_repositor, alignment= Qt.AlignmentFlag.AlignRight)

        self.edit_repositor = criar_lineedit_padrao(LineEditComEnter)
        self.edit_repositor.setFixedWidth(250)

        vbox_repositor = QVBoxLayout()
        vbox_repositor.addLayout(hbox_repositor)
        vbox_repositor.addWidget(self.edit_repositor)


        hbox_aba_abastecimento = QHBoxLayout()
        hbox_aba_abastecimento.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_aba_abastecimento.addLayout(vbox_estoque_minimo)
        hbox_aba_abastecimento.addLayout(vbox_cod_forn)
        hbox_aba_abastecimento.addLayout(vbox_nome_forn)
        hbox_aba_abastecimento.addLayout(vbox_repositor)


        aba_abastecimento.setLayout(hbox_aba_abastecimento)

        # criação da aba unidade dentro da apresentação
        aba_unidade = QWidget()

        # unidade compra
        unidade = ["UN", "CX", "LT", "PCT", "GL", "TB"]
        
        un_compra = criar_label_padrao()
        un_compra.setText('Un. Compra')
        un_compra.setContentsMargins(2, 0, 0, 0)
        un_compra.setFixedSize(un_compra.sizeHint())

        self.comb_un_compra = criar_combobox_padrao()
        self.comb_un_compra.setFixedWidth(80)
        self.comb_un_compra.addItems(unidade)

        vbox_unid_compra = QVBoxLayout()
        vbox_unid_compra.addWidget(un_compra)
        vbox_unid_compra.addWidget(self.comb_un_compra)

        # quantidade compra
        quant_compra = criar_label_padrao()
        quant_compra.setText('Quant. Compra (Fator convers.)')
        quant_compra.setContentsMargins(2, 0, 0, 0)
        quant_compra.setFixedSize(quant_compra.sizeHint())

        self.edit_quant_compra = criar_lineedit_padrao(LineEditComEnter)
        self.edit_quant_compra.setFixedWidth(200)

        vbox_quant_compra = QVBoxLayout()
        vbox_quant_compra.addWidget(quant_compra)
        vbox_quant_compra.addWidget(self.edit_quant_compra)

        # unidade venda
        un_venda = criar_label_padrao()
        un_venda.setText('Un. Venda')
        un_venda.setContentsMargins(2, 0, 0, 0)
        un_venda.setFixedSize(un_venda.sizeHint())

        self.comb_un_venda = criar_combobox_padrao()
        self.comb_un_venda.setFixedWidth(80)
        self.comb_un_venda.addItems(unidade)

        vbox_unid_venda = QVBoxLayout()
        vbox_unid_venda.addWidget(un_venda)
        vbox_unid_venda.addWidget(self.comb_un_venda)

        # quantidade venda
        quant_venda = criar_label_padrao()
        quant_venda.setText('Quant. Venda')
        quant_venda.setContentsMargins(2, 0, 0, 0)
        quant_venda.setFixedSize(quant_venda.sizeHint())

        self.edit_quant_venda = criar_lineedit_padrao(LineEditComEnter)
        self.edit_quant_venda.setFixedWidth(100)

        vbox_quant_venda = QVBoxLayout()
        vbox_quant_venda.addWidget(quant_venda)
        vbox_quant_venda.addWidget(self.edit_quant_venda)


        #combo tipo inteiro / decimal
        label_tipo = criar_label_padrao()
        label_tipo.setText("Tipo Quantidade")
        label_tipo.setContentsMargins(2, 0, 0, 0)
        label_tipo.setFixedSize(label_tipo.sizeHint())

        self.combo_tipo_quant = criar_combobox_padrao()
        self.combo_tipo_quant.addItems(["Inteiro", "Decimal"])
        self.combo_tipo_quant.setFixedWidth(150)        

        vbox_tipo = QVBoxLayout()
        vbox_tipo.addWidget(label_tipo)
        vbox_tipo.addWidget(self.combo_tipo_quant)

        # hbox aba unidade
        hbox_aba_unidade = QHBoxLayout()
        hbox_aba_unidade.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_aba_unidade.addLayout(vbox_unid_compra)
        hbox_aba_unidade.addLayout(vbox_quant_compra)
        hbox_aba_unidade.addLayout(vbox_unid_venda)
        hbox_aba_unidade.addLayout(vbox_quant_venda)
        hbox_aba_unidade.addLayout(vbox_tipo)


        aba_unidade.setLayout(hbox_aba_unidade)

        # criação da aba localidade dentro da apresentação
        aba_localizacao = QWidget()

        # rua localização
        rua = criar_label_padrao()
        rua.setText('Rua')
        rua.setContentsMargins(2, 0, 0, 0)
        rua.setFixedSize(rua.sizeHint())

        self.edit_rua = criar_lineedit_padrao(LineEditComEnter)
        self.edit_rua.setFixedWidth(100)

        vbox_rua = QVBoxLayout()
        vbox_rua.addWidget(rua)
        vbox_rua.addWidget(self.edit_rua)
        
        # bloco localização
        bloco = criar_label_padrao()
        bloco.setText('Bloco')
        bloco.setContentsMargins(2, 0, 0, 0)
        bloco.setFixedSize(bloco.sizeHint())

        self.edit_bloco = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bloco.setFixedWidth(100)

        vbox_bloco = QVBoxLayout()
        vbox_bloco.addWidget(bloco)
        vbox_bloco.addWidget(self.edit_bloco)

        # Prateleira localização
        prateleira = criar_label_padrao()
        prateleira.setText('Prateleira')
        prateleira.setContentsMargins(2, 0, 0, 0)
        prateleira.setFixedSize(prateleira.sizeHint())

        self.edit_prateleira = criar_lineedit_padrao(LineEditComEnter)
        self.edit_prateleira.setFixedWidth(100)

        vbox_prateleira = QVBoxLayout()
        vbox_prateleira.addWidget(prateleira)
        vbox_prateleira.addWidget(self.edit_prateleira)

        # Gaveta localização
        gaveta = criar_label_padrao()
        gaveta.setText('Gaveta')
        gaveta.setContentsMargins(2, 0, 0, 0)
        gaveta.setFixedSize(gaveta.sizeHint())

        self.edit_gaveta = criar_lineedit_padrao(LineEditComEnter)
        self.edit_gaveta.setFixedWidth(100)

        vbox_gaveta = QVBoxLayout()
        vbox_gaveta.addWidget(gaveta)
        vbox_gaveta.addWidget(self.edit_gaveta)

        # horizontal layout aba localização
        hbox_aba_localizacao = QHBoxLayout()
        hbox_aba_localizacao.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_aba_localizacao.addLayout(vbox_rua)
        hbox_aba_localizacao.addLayout(vbox_bloco)
        hbox_aba_localizacao.addLayout(vbox_prateleira)
        hbox_aba_localizacao.addLayout(vbox_gaveta)

        aba_localizacao.setLayout(hbox_aba_localizacao) 

        self.tab_apresentacao.addTab(aba_abastecimento, 'Abastec.')
        self.tab_apresentacao.addTab(aba_unidade, 'Unidade')
        self.tab_apresentacao.addTab(aba_localizacao, 'Localização')

        # criação do horizontalbox linha 1 codigos e referencias
        hbox_cad_linha1 = QHBoxLayout()
        hbox_cad_linha1.addLayout(vbox_cod)
        hbox_cad_linha1.addLayout(vbox_barras)
        hbox_cad_linha1.addLayout(vbox_barras2)
        hbox_cad_linha1.addLayout(vbox_ref_forn)
        hbox_cad_linha1.addLayout(vbox_ref_orig)
        hbox_cad_linha1.addLayout(vbox_ref_similar)

        # criação do horizontalbox linha 2 descrição aplicação
        hbox_cad_linha2 = QHBoxLayout()
        hbox_cad_linha2.addLayout(vbox_desc)
        hbox_cad_linha2.addLayout(vbox_aplic)

        # label tritutários
        tributario = QLabel('TRIBUTÁRIOS')
        tributario.setStyleSheet('font: bold; color: orange; background-color: #031740; font-size: 12px')
        tributario.setContentsMargins(2, 0, 0, 0)
        tributario.setMinimumWidth(650)
        tributario.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # criação da tab tritutários
        self.tab_tributacao = criar_tab_widget()
        self.tab_tributacao.setFixedHeight(108)

        self.tab_tributacao.setStyleSheet("""
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

        #criação da aba classificação fiscal
        aba_class_fiscal = QWidget()

        #criação campo ncm
        ncm = criar_label_padrao()
        ncm.setText('Cód. NCM')
        ncm.setContentsMargins(2, 0, 0, 0)
        ncm.setFixedSize(ncm.sizeHint())

        self.edit_ncm = criar_lineedit_padrao(LineEditComEnter)
        self.edit_ncm.setFixedWidth(90)
        self.edit_ncm.setInputMask('0000.00.00;_')

        vbox_ncm = QVBoxLayout()
        vbox_ncm.addWidget(ncm)
        vbox_ncm.addWidget(self.edit_ncm)

        #criação campo EX TIPO
        ex_tipi = criar_label_padrao()
        ex_tipi.setText('EX/TIPI/NCM')
        ex_tipi.setContentsMargins(2, 0, 0, 0)
        ex_tipi.setFixedSize(ex_tipi.sizeHint())

        self.edit_ex_tipi = criar_lineedit_padrao(LineEditComEnter)
        self.edit_ex_tipi.setFixedWidth(90)

        vbox_ex_tipi = QVBoxLayout()
        vbox_ex_tipi.addWidget(ex_tipi)
        vbox_ex_tipi.addWidget(self.edit_ex_tipi)

        #criação campo CEST
        cest = criar_label_padrao()
        cest.setText('Cód. CEST')
        cest.setContentsMargins(2, 0, 0, 0)
        cest.setFixedSize(cest.sizeHint())

        self.edit_cest = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cest.setFixedWidth(90)
        self.edit_cest.setInputMask("00.000.00;_")

        vbox_cest = QVBoxLayout()
        vbox_cest.addWidget(cest)
        vbox_cest.addWidget(self.edit_cest)

        #criação campo NVE
        nve = criar_label_padrao()
        nve.setText('Cód. NVE')
        nve.setContentsMargins(2, 0, 0, 0)
        nve.setFixedSize(nve.sizeHint())

        self.edit_nve = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nve.setFixedWidth(90)

        vbox_nve = QVBoxLayout()
        vbox_nve.addWidget(nve)
        vbox_nve.addWidget(self.edit_nve)

        #criação do hbox da aba classificação fiscao / adicionamento na aba
        hbox_aba_class_fiscal = QHBoxLayout()
        hbox_aba_class_fiscal.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_aba_class_fiscal.addLayout(vbox_ncm)
        hbox_aba_class_fiscal.addLayout(vbox_ex_tipi)
        hbox_aba_class_fiscal.addLayout(vbox_cest)
        hbox_aba_class_fiscal.addLayout(vbox_nve)

        #adicinando o hbox na aba classificação fiscal 
        aba_class_fiscal.setLayout(hbox_aba_class_fiscal)

        # cria aba identificação fiscal 
        aba_ident_fiscal = QWidget()

        # #cria o campo GTIN/EAN comercial
        # gtin_ean_comercial = criar_label_padrao()
        # gtin_ean_comercial.setText('GTIN/EAN Comercial')
        # gtin_ean_comercial.setContentsMargins(2, 0, 0, 0)
        # gtin_ean_comercial.setFixedSize(gtin_ean_comercial.sizeHint())

        # self.edit_gtin_ean_com = criar_lineedit_padrao(LineEditComEnter)
        # self.edit_gtin_ean_com.setFixedWidth(150)

        # vbox_gtin_ean_com = QVBoxLayout()
        # vbox_gtin_ean_com.addWidget(gtin_ean_comercial)
        # vbox_gtin_ean_com.addWidget(self.edit_gtin_ean_com)

        # #cria o campo GTIN/EAN tributável
        # gtin_ean_tributavel = criar_label_padrao()
        # gtin_ean_tributavel.setText('GTIN/EAN Tributável')
        # gtin_ean_tributavel.setContentsMargins(2, 0, 0, 0)
        # gtin_ean_tributavel.setFixedSize(gtin_ean_tributavel.sizeHint())

        # self.edit_gtin_ean_trib = criar_lineedit_padrao(LineEditComEnter)
        # self.edit_gtin_ean_trib.setFixedWidth(150)

        # vbox_gtin_ean_trib = QVBoxLayout()
        # vbox_gtin_ean_trib.addWidget(gtin_ean_tributavel)
        # vbox_gtin_ean_trib.addWidget(self.edit_gtin_ean_trib)

        #cria o campo Unidade tributável
        uni_trib = criar_label_padrao()
        uni_trib.setText('Und. Trib.')
        uni_trib.setContentsMargins(2, 0, 0, 0)
        uni_trib.setFixedSize(uni_trib.sizeHint())

        self.combo_unid_trib = criar_combobox_padrao()
        self.combo_unid_trib.setFixedWidth(70)
        self.combo_unid_trib.addItems([
            "UN",
            "KG",
            "CX",
            "LT",
        ])

        vbox_uni_trib = QVBoxLayout()
        vbox_uni_trib.addWidget(uni_trib)
        vbox_uni_trib.addWidget(self.combo_unid_trib)

        #cria o campo Fator conversão tributária
        fat_conv_trib = criar_label_padrao()
        fat_conv_trib.setText('Fat. Conv. Tributária')
        fat_conv_trib.setContentsMargins(2, 0, 0, 0)
        fat_conv_trib.setFixedSize(fat_conv_trib.sizeHint())

        self.edit_fat_conv_trib = criar_lineedit_padrao(LineEditComEnter)
        self.edit_fat_conv_trib.setFixedWidth(150)

        vbox_fat_conv_trib= QVBoxLayout()
        vbox_fat_conv_trib.addWidget(fat_conv_trib)
        vbox_fat_conv_trib.addWidget(self.edit_fat_conv_trib)

        # cria o horizontal layout da aba identificação fiscal 
        hbox_aba_ident_fiscal= QHBoxLayout()
        hbox_aba_ident_fiscal.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # hbox_aba_ident_fiscal.addLayout(vbox_gtin_ean_com)
        # hbox_aba_ident_fiscal.addLayout(vbox_gtin_ean_trib)
        hbox_aba_ident_fiscal.addLayout(vbox_uni_trib)
        hbox_aba_ident_fiscal.addLayout(vbox_fat_conv_trib)

        #adiciona o layout na aba
        aba_ident_fiscal.setLayout(hbox_aba_ident_fiscal)

        #cria a aba regras especiais
        aba_reg_espec = QWidget()
        #cria o campo Origem da mercadoria
        orig_mercadoria = criar_label_padrao()
        orig_mercadoria.setText('Origem da Merc.')
        orig_mercadoria.setContentsMargins(2, 0, 0, 0)
        orig_mercadoria.setFixedSize(orig_mercadoria.sizeHint())

        self.combo_origem_merc = criar_combobox_padrao()
        self.combo_origem_merc.setFixedWidth(260)
        self.combo_origem_merc.addItems([
            "0 - Nacional",
            "1 - Estrangeira - Importação direta",
            "2 - Estrangeira - Adquirida no mercado interno",
            "3 - Nacional com conteúdo importado > 40%",
            "4 - Nacional produção conforme PPB",
            "5 - Nacional com conteúdo importado ≤ 40%",
            "6 - Estrangeira sem similar nacional",
            "7 - Estrangeira adquirida no mercado interno sem similar",
            "8 - Nacional com conteúdo importado > 70%"
        ])

        vbox_orig_mercadoria= QVBoxLayout()
        vbox_orig_mercadoria.addWidget(orig_mercadoria)
        vbox_orig_mercadoria.addWidget(self.combo_origem_merc)

        #cria o campo cBenef
        cbenef = criar_label_padrao()
        cbenef.setText('cBenef')
        cbenef.setContentsMargins(2, 0, 0, 0)
        cbenef.setFixedSize(cbenef.sizeHint())

        self.edit_cbenef = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cbenef.setFixedWidth(150)

        vbox_cbenef = QVBoxLayout()
        vbox_cbenef.addWidget(cbenef)
        vbox_cbenef.addWidget(self.edit_cbenef)

        #cria o campo Indicador de escala relevante
        ind_escala = criar_label_padrao()
        ind_escala.setText('Indic. Escala Relevante')
        ind_escala.setContentsMargins(2, 0, 0, 0)
        ind_escala.setFixedSize(ind_escala.sizeHint())

        self.combo_ind_escala_rel = criar_combobox_padrao()
        self.combo_ind_escala_rel.setFixedWidth(150)
        self.combo_ind_escala_rel.addItems(['','NÃO', 'SIM'])


        vbox_ind_escala = QVBoxLayout()
        vbox_ind_escala.addWidget(ind_escala)
        vbox_ind_escala.addWidget(self.combo_ind_escala_rel)

        #cria o campo CNPJ fabricante
        cnpj_fabricante = criar_label_padrao()
        cnpj_fabricante.setText('CNPJ fabricante')
        cnpj_fabricante.setContentsMargins(2, 0, 0, 0)
        cnpj_fabricante.setFixedSize(cnpj_fabricante.sizeHint())

        self.edit_cnpj_fabricante = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cnpj_fabricante.setFixedWidth(150)
        self.edit_cnpj_fabricante.setInputMask('00.000.000/0000-00;_')

        vbox_cnpj_fabricante = QVBoxLayout()
        vbox_cnpj_fabricante.addWidget(cnpj_fabricante)
        vbox_cnpj_fabricante.addWidget(self.edit_cnpj_fabricante)

        #cria o campo ANP
        anp = criar_label_padrao()
        anp.setText('Código ANP')
        anp.setContentsMargins(2, 0, 0, 0)
        anp.setFixedSize(anp.sizeHint())
        
        self.edit_anp = criar_lineedit_padrao(LineEditComEnter)
        self.edit_anp.setFixedWidth(150)

        vbox_anp = QVBoxLayout()
        vbox_anp.addWidget(anp)
        vbox_anp.addWidget(self.edit_anp)

        #cria horizontal box aba registros especiais
        hbox_aba_reg_espec = QHBoxLayout()
        hbox_aba_reg_espec.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_aba_reg_espec.addLayout(vbox_orig_mercadoria)
        hbox_aba_reg_espec.addLayout(vbox_cbenef)
        hbox_aba_reg_espec.addLayout(vbox_ind_escala)
        hbox_aba_reg_espec.addLayout(vbox_cnpj_fabricante)
        hbox_aba_reg_espec.addLayout(vbox_anp)

        aba_reg_espec.setLayout(hbox_aba_reg_espec)

        #cria a aba tributação padrão
        aba_trib_padrao = QWidget()

        #cria o campo CST ICMS/CSOSN
        cst_icms_csosn = criar_label_padrao()
        cst_icms_csosn.setText('CST ICMS/CSOSN')
        cst_icms_csosn.setContentsMargins(2, 0, 0, 0)
        cst_icms_csosn.setFixedSize(cst_icms_csosn.sizeHint())

        self.combo_cst_icms_csosn = criar_combobox_padrao()
        self.combo_cst_icms_csosn.setFixedWidth(260)
        self.combo_cst_icms_csosn.addItems([
            "102 - Tributada sem crédito",
            "500 - ICMS ST",
            "00 - Tributada integral",
            "20 - Redução de base",
            "40 - Isenta",
            "60 - ICMS ST"
        ])

        vbox_cst_icms_csosn = QVBoxLayout()
        vbox_cst_icms_csosn.addWidget(cst_icms_csosn)
        vbox_cst_icms_csosn.addWidget(self.combo_cst_icms_csosn)

        #cria o campo CST PIS
        cst_pis = criar_label_padrao()
        cst_pis.setText('CST PIS')
        cst_pis.setContentsMargins(2, 0, 0, 0)
        cst_pis.setFixedSize(cst_pis.sizeHint())

        self.combo_cst_pis = criar_combobox_padrao()
        self.combo_cst_pis.setFixedWidth(220)
        self.combo_cst_pis.addItems([
            "",
            "01 - Operação tributável",
            "04 - Monofásica",
            "06 - Alíquota zero",
            "07 - Isenta",
            "08 - Sem incidência",
            "09 - Suspensão",
            "49 - Outras operações de saída",
            "99 - Outras operações"
        ])

        vbox_cst_pis = QVBoxLayout()
        vbox_cst_pis.addWidget(cst_pis)
        vbox_cst_pis.addWidget(self.combo_cst_pis)

        #cria o campo CST COFINS
        cst_cofins = criar_label_padrao()
        cst_cofins.setText('CST COFINS')
        cst_cofins.setContentsMargins(2, 0, 0, 0)
        cst_cofins.setFixedSize(cst_cofins.sizeHint())

        self.combo_cst_cofins = criar_combobox_padrao()
        self.combo_cst_cofins.setFixedWidth(220)
        self.combo_cst_cofins.addItems([
            "",
            "01 - Operação tributável",
            "04 - Monofásica",
            "06 - Alíquota zero",
            "07 - Isenta",
            "08 - Sem incidência",
            "09 - Suspensão",
            "49 - Outras operações de saída",
            "99 - Outras operações"
        ])

        vbox_cst_cofins = QVBoxLayout()
        vbox_cst_cofins.addWidget(cst_cofins)
        vbox_cst_cofins.addWidget(self.combo_cst_cofins)

        #cria o campo CST IPI
        cst_ipi = criar_label_padrao()
        cst_ipi.setText('CST IPI')
        cst_ipi.setContentsMargins(2, 0, 0, 0)
        cst_ipi.setFixedSize(cst_ipi.sizeHint())

        self.combo_cst_ipi = criar_combobox_padrao()
        self.combo_cst_ipi.setFixedWidth(220)
        self.combo_cst_ipi.addItems([
            "",
            "00 - Entrada com crédito",
            "02 - Isento",
            "49 - Outras entradas",
            "50 - Saída tributada",
            "53 - Saída não tributada",
            "99 - Outras saídas"
        ])

        vbox_cst_ipi = QVBoxLayout()
        vbox_cst_ipi.addWidget(cst_ipi)
        vbox_cst_ipi.addWidget(self.combo_cst_ipi)

        #cria o campo Alíquota IPI
        aliq_ipi = criar_label_padrao()
        aliq_ipi.setText('Alíquota IPI')
        aliq_ipi.setContentsMargins(2, 0, 0, 0)
        aliq_ipi.setFixedSize(aliq_ipi.sizeHint())

        self.edit_aliq_ipi = criar_lineedit_padrao(LineEditComEnter)
        self.edit_aliq_ipi.setFixedWidth(150)

        vbox_aliq_ipi = QVBoxLayout()
        vbox_aliq_ipi.addWidget(aliq_ipi)
        vbox_aliq_ipi.addWidget(self.edit_aliq_ipi)
        
        #cria o horizontal layout da aba tributação padrao
        hbox_aba_trib_padrao = QHBoxLayout()
        hbox_aba_trib_padrao.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_aba_trib_padrao.addLayout(vbox_cst_icms_csosn)
        hbox_aba_trib_padrao.addLayout(vbox_cst_pis)
        hbox_aba_trib_padrao.addLayout(vbox_cst_cofins)
        hbox_aba_trib_padrao.addLayout(vbox_cst_ipi)
        hbox_aba_trib_padrao.addLayout(vbox_aliq_ipi)

        #adiciona o horizontal layout aba tributação padrado na tela
        aba_trib_padrao.setLayout(hbox_aba_trib_padrao)

        # adiciona as abas fiscais na na tab
        self.tab_tributacao.addTab(aba_class_fiscal, 'Class. Fiscal')
        self.tab_tributacao.addTab(aba_ident_fiscal, 'Ident. Fiscal/Comerc.')
        self.tab_tributacao.addTab(aba_reg_espec, 'Regras Especiais')
        self.tab_tributacao.addTab(aba_trib_padrao, 'Tributação Padrão')


        # label preço
        preco = QLabel('PREÇOS')
        preco.setStyleSheet('font: bold; color: orange; background-color: #031740; font-size: 12px')
        preco.setContentsMargins(2, 0, 0, 0)
        preco.setMinimumWidth(650)
        preco.setAlignment(Qt.AlignmentFlag.AlignCenter)


        #cria campo preço custo
        preco_custo = criar_label_padrao()
        preco_custo.setText('Preço Custo')
        preco_custo.setContentsMargins(2, 0, 0, 0)
        preco_custo.setFixedSize(preco_custo.sizeHint())

        self.edit_preco_custo = criar_lineedit_padrao(LineEditComEnter)
        # self.edit_preco_custo.setValidator(validador_preco())
        self.edit_preco_custo.setFixedWidth(120)
        self.edit_preco_custo.editingFinished.connect(self.atualizar_calculo_preco)
        self.edit_preco_custo.editingFinished.connect(lambda: self.formatar_preco_campo(self.edit_preco_custo))
       
        #cria campo media custo
        media_custo = criar_label_padrao()
        media_custo.setText('Média Custo')
        media_custo.setContentsMargins(2, 0, 0, 0)
        media_custo.setFixedSize(media_custo.sizeHint())

        self.edit_media_custo = criar_lineedit_padrao(LineEditComEnter)
        self.edit_media_custo.setFixedWidth(120)
        self.edit_media_custo.setReadOnly(True)

        #cria um vertical box dos campos preço custo / media custo
        vbox_preco_custo = QVBoxLayout()
        vbox_preco_custo.addWidget(preco_custo)
        vbox_preco_custo.addWidget(self.edit_preco_custo)
        vbox_preco_custo.addWidget(media_custo)
        vbox_preco_custo.addWidget(self.edit_media_custo)
        
        #cria campo preço venda
        preco_venda = criar_label_padrao()
        preco_venda.setText('Preço Venda')
        preco_venda.setContentsMargins(2, 0, 0, 0)
        preco_venda.setFixedSize(preco_venda.sizeHint())

        self.edit_preco_venda = criar_lineedit_padrao(LineEditComEnter)
        # self.edit_preco_venda.setValidator(validador_preco())
        self.edit_preco_venda.setFixedWidth(120)
        self.edit_preco_venda.editingFinished.connect(self.calcular_margem_lucro)
        self.edit_preco_venda.editingFinished.connect(lambda: self.formatar_preco_campo(self.edit_preco_venda))
       
        #cria campo margem lucro
        margem_lucro = criar_label_padrao()
        margem_lucro.setText('Margem lucro %')
        margem_lucro.setContentsMargins(2, 0, 0, 0)
        margem_lucro.setFixedSize(margem_lucro.sizeHint())

        self.edit_margem_lucro = criar_lineedit_padrao(LineEditComEnter)
        self.edit_margem_lucro.setFixedWidth(120)
        self.edit_margem_lucro.setValidator(self.validador_percentual())
        self.edit_margem_lucro.textChanged.connect(self.calcular_preco_venda)
       
        #cria vertical box dos campos preco venda / margem lucro
        vbox_preco_venda = QVBoxLayout()
        vbox_preco_venda.addWidget(preco_venda)
        vbox_preco_venda.addWidget(self.edit_preco_venda)
        vbox_preco_venda.addWidget(margem_lucro)
        vbox_preco_venda.addWidget(self.edit_margem_lucro)

        #cria campo preço promoção
        preco_promocao = criar_label_padrao()
        preco_promocao.setText('Preço Promocional')
        preco_promocao.setContentsMargins(2, 0, 0, 0)
        preco_promocao.setFixedSize(preco_promocao.sizeHint())

        self.edit_preco_promocao = criar_lineedit_padrao(LineEditComEnter)
        # self.edit_preco_promocao.setValidator(validador_preco())
        self.edit_preco_promocao.setFixedWidth(120)
        self.edit_preco_promocao.editingFinished.connect(lambda: self.formatar_preco_campo(self.edit_preco_promocao))

        #cria campo % desconto
        desconto = criar_label_padrao()
        desconto.setText('% de desconto')
        desconto.setContentsMargins(2, 0, 0, 0)
        desconto.setFixedSize(desconto.sizeHint())

        self.edit_desconto = criar_lineedit_padrao()
        self.edit_desconto.setFixedWidth(120)
        self.edit_desconto.setValidator(self.validador_percentual())
        
        #cria o vertical layout dos campos preco promocional / % de desconto
        vbox_desconto_preco = QVBoxLayout()
        vbox_desconto_preco.addWidget(preco_promocao)
        vbox_desconto_preco.addWidget(self.edit_preco_promocao)
        vbox_desconto_preco.addWidget(desconto)
        vbox_desconto_preco.addWidget(self.edit_desconto)

        #cria o horizontal layout dos preços
        hbox_linha_preco = QHBoxLayout()
        hbox_linha_preco.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_linha_preco.addLayout(vbox_preco_custo)
        hbox_linha_preco.addLayout(vbox_preco_venda)
        hbox_linha_preco.addLayout(vbox_desconto_preco)


        layout_geral_aba2 = QVBoxLayout()
        layout_geral_aba2.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba2.addWidget(codigos)
        layout_geral_aba2.addLayout(hbox_cad_linha1)
        layout_geral_aba2.addWidget(apres)
        layout_geral_aba2.addLayout(hbox_cad_linha2)
        layout_geral_aba2.addWidget(self.tab_apresentacao)
        layout_geral_aba2.addWidget(tributario)
        layout_geral_aba2.addWidget(self.tab_tributacao)
        layout_geral_aba2.addWidget(preco)
        layout_geral_aba2.addLayout(hbox_linha_preco)
        layout_geral_aba2.addStretch()

        aba2.setLayout(layout_geral_aba2)

        self.tab.addTab(aba1, "Consulta")
        self.tab.addTab(aba2, "Cadastro")

        # Botões parte inferior da tela
        self.btn_sair = criar_botao_sair()
        self.btn_sair.clicked.connect(self.sair)

        self.btn_salvar = criar_botao_salvar()
        self.btn_salvar.clicked.connect(self.salvar)

        hbox_botoes = QHBoxLayout()
        hbox_botoes.addStretch()
        hbox_botoes.addWidget(self.btn_sair)
        hbox_botoes.addSpacing(40)
        hbox_botoes.addWidget(self.btn_salvar)
        hbox_botoes.addStretch()

        # layout proncipal
        vbox = QVBoxLayout()
        vbox.addWidget(nometela, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        vbox.addWidget(self.tab)
        vbox.addLayout(hbox_botoes)
        vbox.setContentsMargins(20, 20, 20, 20)

        self.setLayout(vbox)


    def carregar_produto(self, linha, coluna):
        codigo = self.tabela_resultado.item(linha, 0).text()

        if not codigo or codigo == "None":
            return

        from bd import buscar_produto_por_codigo
        produto = buscar_produto_por_codigo(codigo)

        if not produto:
            QMessageBox.warning(self, "Aviso", "Produto não encontrado.")
            return

        # Preenchendo campos
        self.edit_cod.setText(str(produto["codigo"]))
        self.edit_cod_barras.setText(produto["cod_barras"])
        self.edit_cod_barras2.setText(produto["cod_barras_2"])
        self.edit_desc.setText(produto["descricao"])
        self.edit_ref_forn.setText(produto["ref_fornecedor"])
        self.edit_ref_orig.setText(produto["ref_original"])
        self.edit_ref_similar.setText(produto["ref_similar"])
        self.edit_aplic.setText(produto["aplicacao"])

        self.edit_estoque_minimo.setText(str(produto["estoque_minimo"] or ""))
        self.edit_cod_forn.setText(str(produto["cod_fornecedor"] or ""))
        self.edit_nome_forn.setText(str(produto["nome_fornecedor"] or ""))
        self.edit_repositor.setText(str(produto["repositor"] or ""))

        self.edit_preco_custo.setText(str(produto["preco_custo"]))
        self.edit_preco_venda.setText(str(produto["preco_venda"]))
        self.edit_preco_promocao.setText(str(produto["preco_promocao"]))
        self.edit_margem_lucro.setText(str(produto["margem_lucro"]))
        self.edit_desconto.setText(str(produto["desconto"]))
        self.combo_tipo_quant.setCurrentText(produto["tipo_quantidade"])

        # Vai pra aba cadastro
        self.tab.setCurrentIndex(1)

    def preencher_tabela(self, texto=None):
        texto_pesquisa = self.edit_label_pesq.text().strip().upper()
        opcao = self.comb_opc.currentText()

        self.tabela_resultado.setRowCount(0)

        if self.check_todos.isChecked():
            dados = listar_produtos()
        else:
            if not texto_pesquisa:
                return
            dados = pesquisar_produtos_avancado(opcao, texto_pesquisa)

        if not dados:
            return

        self.tabela_resultado.setRowCount(len(dados))

        for linha, dados_linha in enumerate(dados):
            for coluna, valor in enumerate(dados_linha):
                if coluna == 3:
                    valor = f"{float(valor):.2f}".replace(".", ",")
                else:
                    valor = str(valor)

                self.tabela_resultado.setItem(linha, coluna, QTableWidgetItem(valor))
                    
    def formatar_preco_campo(self, campo):
        try:
            valor = texto_para_float(campo.text())
            campo.setText(formatar_preco(valor))
        except ValueError:
            pass


    def calcular_preco_venda(self):
        try:
            preco_custo = texto_para_float(self.edit_preco_custo.text())
            margem = texto_para_float(self.edit_margem_lucro.text())

            if preco_custo <= 0:
                return

            preco_venda = preco_custo + (preco_custo * margem / 100)
            self.edit_preco_venda.setText(formatar_preco(preco_venda))
        except ValueError:
            pass


    def calcular_margem_lucro(self):
        try:
            preco_custo = texto_para_float(self.edit_preco_custo.text())
            preco_venda = texto_para_float(self.edit_preco_venda.text())

            if preco_custo <= 0:
                return

            margem = ((preco_venda - preco_custo) / preco_custo) * 100
            self.edit_margem_lucro.setText(formatar_preco(margem))

        except ValueError:
            pass


    def atualizar_calculo_preco(self):
        if self.edit_margem_lucro.text().strip():
            self.calcular_preco_venda()
        elif self.edit_preco_venda.text().strip():
            self.calcular_margem_lucro()

    def salvar(self):
        descricao = self.edit_desc.text().strip().upper()
        tipo_quant = self.combo_tipo_quant.currentText()

        if not descricao:
            QMessageBox.warning(self, "Aviso", "Descrição é obrigatória.")
            self.edit_desc.setFocus()
            return

        dados = {
            "codigo": self.edit_cod.text().strip(),
            "cod_barras": self.edit_cod_barras.text().strip(),
            "cod_barras2": self.edit_cod_barras2.text().strip(),
            "descricao": self.edit_desc.text().strip().upper(),
            "ref_forn": self.edit_ref_forn.text().strip().upper(),
            "ref_orig": self.edit_ref_orig.text().strip().upper(),
            "ref_similar": self.edit_ref_similar.text().strip().upper(),
            "aplicacao": self.edit_aplic.text().strip().upper(),

            "estoque_minimo": self.edit_estoque_minimo.text().strip(),
            "cod_fornecedor": self.edit_cod_forn.text().strip(),
            "nome_fornecedor": self.edit_nome_forn.text().strip().upper(),
            "repositor": self.edit_repositor.text().strip().upper(),

            "preco_custo": self.edit_preco_custo.text().strip(),
            "preco_venda": self.edit_preco_venda.text().strip(),
            "preco_promocao": self.edit_preco_promocao.text().strip(),
            "margem_lucro": self.edit_margem_lucro.text().strip(),
            "desconto": self.edit_desconto.text().strip(),
            "tipo_quantidade": tipo_quant,
        }

        if dados["codigo"]:
            sucesso = atualizar_produto(dados)
            mensagem = "Produto atualizado com sucesso!"
        else:
            sucesso = salvar_produto(dados)
            mensagem = "Produto salvo com sucesso!"

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.limpar_campos()
            self.preencher_tabela()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao salvar produto.")
                    
    def sair(self):
        from telaMain import telaPrincipal
        self.janela = telaPrincipal()
        self.janela.show()
        self.close()

    def validador_percentual(self):
        return QDoubleValidator(0.0, 100.0, 2)

    def limpar_campos(self):
        self.tab.setCurrentIndex(1)

        self.edit_cod.clear()
        self.edit_cod_barras.clear()
        self.edit_cod_barras2.clear()
        self.edit_ref_forn.clear()
        self.edit_ref_orig.clear()
        self.edit_ref_similar.clear()
        self.edit_desc.clear()
        self.edit_aplic.clear()
        self.edit_preco_custo.clear()
        self.edit_preco_venda.clear()
        self.edit_margem_lucro.clear()
        self.edit_preco_promocao.clear()
        self.edit_desconto.clear()

        self.edit_desc.setFocus()

    def excluir_produto(self):
        linha = self.tabela_resultado.currentRow()

        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um produto na tabela para excluir.")
            return

        item_codigo = self.tabela_resultado.item(linha, 0)
        item_descricao = self.tabela_resultado.item(linha, 1)

        if item_codigo is None:
            QMessageBox.warning(self, "Aviso", "Não foi possível identificar o produto.")
            return

        codigo = item_codigo.text().strip()
        descricao = item_descricao.text().strip() if item_descricao else ""

        msg = QMessageBox(self)
        msg.setWindowTitle("Confirmar exclusão")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText(
            f"Deseja excluir o produto?\n\n"
            f"Código: {codigo}\n"
            f"Descrição: {descricao}"
        )

        btn_sim = msg.addButton("Sim", QMessageBox.ButtonRole.YesRole)
        btn_nao = msg.addButton("Não", QMessageBox.ButtonRole.NoRole)

        msg.setDefaultButton(btn_nao)

        msg.exec()

        if msg.clickedButton() != btn_sim:
            return

        sucesso = excluir_produto_bd(codigo)

        if sucesso:
            QMessageBox.information(self, "Sucesso", "Produto excluído com sucesso!")
            self.preencher_tabela()
            
            if self.edit_cod.text().strip() == codigo:
                self.limpar_campos()

        else:
            QMessageBox.critical(self, "Erro", "Erro ao excluir produto.")


    def acao_check_todos(self, marcado):
        if marcado:
            self.edit_label_pesq.clear()
            self.preencher_tabela()

    def acao_digitar_pesquisa(self, texto):
        if texto.strip():
            if self.check_todos.isChecked():
                self.check_todos.blockSignals(True)
                self.check_todos.setChecked(False)
                self.check_todos.blockSignals(False)

        self.preencher_tabela()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = CadProd()
    janela.show()
    sys.exit(app.exec())
