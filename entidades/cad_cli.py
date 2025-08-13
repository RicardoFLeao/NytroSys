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
from util.fun_basicas import LineEditComEnter, consulta_cep

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
        tab.currentChanged.connect(self.ao_trocar_aba)
        self.tab = tab  # gua

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

        edit_label_pesq = criar_lineedit_padrao()
        edit_label_pesq.setMinimumWidth(810)

        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc)
        vbox_opc.addWidget(comb_opc)

        vbox_mdl = QVBoxLayout()
        vbox_mdl.addWidget(label_mdl)
        vbox_mdl.addWidget(comb_mdl)

        hbox_pesq = QHBoxLayout()
        hbox_pesq.addWidget(label_pesq)
        hbox_pesq.addWidget(check_todos, alignment=Qt.AlignmentFlag.AlignRight)

        vbox_pesq = QVBoxLayout()
        vbox_pesq.addLayout(hbox_pesq)
        vbox_pesq.addWidget(edit_label_pesq)

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
        layout_geral_aba1.addSpacing(10)
        layout_geral_aba1.addLayout(hbox_botoes_rodape)
        layout_geral_aba1.addSpacing(10)

        aba1.setLayout(layout_geral_aba1)

        # ----------- ABA 2 (Cadastro) ------------
        aba2 = QWidget()
        aba2.setStyleSheet('background-color: #cbcdce;')

        #table cadastro de clientes

        table_cliente = criar_tab_widget()
        # criação aba dados 

        aba_dados = QWidget()
        # dados linha 1 --- inicio ---

        cod_cli = criar_label_padrao()
        cod_cli.setText('Código')
        cod_cli.setContentsMargins(2, 0, 0, 0)
        cod_cli.setFixedSize(cod_cli.sizeHint())

        edit_cod_cli = criar_lineedit_padrao()
        edit_cod_cli.setFixedWidth(90)

        vbox_cod_cli = QVBoxLayout()
        vbox_cod_cli.addWidget(cod_cli)
        vbox_cod_cli.addWidget(edit_cod_cli)

        # Razão social 
        raz_social = criar_label_padrao()
        raz_social.setText('Razão Social/Nome')
        raz_social.setContentsMargins(2, 0, 0, 0)
        raz_social.setFixedSize(raz_social.sizeHint())

        # check física / jurídica
        
        self.check_jur = QCheckBox('Jurídica')
        self.check_jur.stateChanged.connect(self.atualiza_form)
        self.check_fis = QCheckBox('Física')
        self.check_fis.stateChanged.connect(self.atualiza_form)

        self.grupo_tipo_pessoa = QButtonGroup(self)
        self.grupo_tipo_pessoa.setExclusive(True)  # Permite só um marcado
        self.grupo_tipo_pessoa.addButton(self.check_jur)
        self.grupo_tipo_pessoa.addButton(self.check_fis)

        hbox_check = QHBoxLayout()
        hbox_check.addWidget(self.check_jur, alignment=Qt.AlignmentFlag.AlignRight)
        hbox_check.addWidget(self.check_fis, alignment=Qt.AlignmentFlag.AlignRight)

        hbox_label_raz_social = QHBoxLayout()
        hbox_label_raz_social.addWidget(raz_social)
        hbox_label_raz_social.addLayout(hbox_check)
        hbox_label_raz_social.setContentsMargins(0, 0, 10, 0)

        self.edit_raz_social = criar_lineedit_padrao(LineEditComEnter)
        self.edit_raz_social.setMinimumWidth(435)

        vbox_raz_social = QVBoxLayout()
        vbox_raz_social.addLayout(hbox_label_raz_social)
        vbox_raz_social.addWidget(self.edit_raz_social)

        # Nome fantasia 
        fant_cli = criar_label_padrao()
        fant_cli.setText('Nome Fantasia/Apelido')
        fant_cli.setContentsMargins(2, 0, 0, 0)
        fant_cli.setFixedSize(fant_cli.sizeHint())

        self.edit_fant_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_fant_cli.setMinimumWidth(390)
        self.edit_fant_cli.setContentsMargins(0,1,0,0)

        vbox_fant_cli = QVBoxLayout()
        vbox_fant_cli.addWidget(fant_cli, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_fant_cli.addWidget(self.edit_fant_cli)

        #contato 

        cont_cli = criar_label_padrao()
        cont_cli.setText('Nome Contato')
        cont_cli.setContentsMargins(2, 0, 0, 0)
        cont_cli.setFixedSize(cont_cli.sizeHint())

        self.edit_cont_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cont_cli.setMinimumWidth(180)

        vbox_cont_cli = QVBoxLayout()
        vbox_cont_cli.addWidget(cont_cli)
        vbox_cont_cli.addWidget(self.edit_cont_cli)

        #WhatsApp
        zap_cli = criar_label_padrao()
        zap_cli.setText('WhatsApp')
        zap_cli.setContentsMargins(2, 0, 0, 0)
        zap_cli.setFixedSize(zap_cli.sizeHint())

        self.edit_zap_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_zap_cli.setFixedWidth(130)
        self.edit_zap_cli.setInputMask('(00)00000-0000;_')

        vbox_zap_cli = QVBoxLayout()
        vbox_zap_cli.addWidget(zap_cli)
        vbox_zap_cli.addWidget(self.edit_zap_cli)
        

        # layout linha 1 
        dados_cli_linha1 = QHBoxLayout()
        dados_cli_linha1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dados_cli_linha1.addLayout(vbox_cod_cli)
        dados_cli_linha1.addLayout(vbox_raz_social)
        dados_cli_linha1.addLayout(vbox_fant_cli)
        dados_cli_linha1.addLayout(vbox_cont_cli)
        dados_cli_linha1.addLayout(vbox_zap_cli)

        # dados linha 1 --- fim ---

        # dados linha 2 --- início ---

        #cep client
        cep_cli = criar_label_padrao()
        cep_cli.setText('CEP')
        cep_cli.setContentsMargins(2, 0, 0, 0)
        cep_cli.setFixedSize(cep_cli.sizeHint())

        self.edit_cep_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cep_cli.setFixedWidth(90)
        self.edit_cep_cli.setInputMask('00.000-000;_')
        self.edit_cep_cli.editingFinished.connect(self.buscar_cep)

        vbox_cep_cli = QVBoxLayout()
        vbox_cep_cli.addWidget(cep_cli)
        vbox_cep_cli.addWidget(self.edit_cep_cli)
        
        #endereço cliente
        end_cli = criar_label_padrao()
        end_cli.setText('Endereço')
        end_cli.setContentsMargins(2, 0, 0, 0)
        end_cli.setFixedSize(end_cli.sizeHint())

        self.edit_end_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_end_cli.setMinimumWidth(335)

        vbox_end_cli = QVBoxLayout()
        vbox_end_cli.addWidget(end_cli)
        vbox_end_cli.addWidget(self.edit_end_cli)

        #número
        num_cli = criar_label_padrao()
        num_cli.setText('Número')
        num_cli.setContentsMargins(2, 0, 0, 0)
        num_cli.setFixedSize(num_cli.sizeHint())

        edit_num_cli = criar_lineedit_padrao(LineEditComEnter)
        edit_num_cli.setFixedWidth(80)

        vbox_num_cli = QVBoxLayout()
        vbox_num_cli.addWidget(num_cli)
        vbox_num_cli.addWidget(edit_num_cli)

        #bairro funcionário
        bairro_cli = criar_label_padrao()
        bairro_cli.setText('Bairro')
        bairro_cli.setContentsMargins(2, 0, 0, 0)
        bairro_cli.setFixedSize(bairro_cli.sizeHint())

        self.edit_bairro_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bairro_cli.setMinimumWidth(205)

        vbox_bairro_cli = QVBoxLayout()
        vbox_bairro_cli.addWidget(bairro_cli)
        vbox_bairro_cli.addWidget(self.edit_bairro_cli)

        #cidade fornecedor
        cid_cli = criar_label_padrao()
        cid_cli.setText('Cidade')
        cid_cli.setContentsMargins(2, 0, 0, 0)
        cid_cli.setFixedSize(cid_cli.sizeHint())

        self.edit_cid_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cid_cli.setMinimumWidth(220)

        vbox_cid_cli = QVBoxLayout()
        vbox_cid_cli.addWidget(cid_cli)
        vbox_cid_cli.addWidget(self.edit_cid_cli)

        #estado fornecedor
        est_cli = criar_label_padrao()
        est_cli.setText('UF')
        est_cli.setContentsMargins(2, 0, 0, 0)
        est_cli.setFixedSize(est_cli.sizeHint())

        self.edit_est_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_est_cli.setFixedWidth(60)

        vbox_est_cli = QVBoxLayout()
        vbox_est_cli.addWidget(est_cli)
        vbox_est_cli.addWidget(self.edit_est_cli)

        #e-mail fornecedor
        email_cli = criar_label_padrao()
        email_cli.setText('e-mail')
        email_cli.setContentsMargins(2, 0 , 0, 0)
        email_cli.setFixedSize(email_cli.sizeHint())

        self.edit_email_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_email_cli.setFixedWidth(310)

        vbox_email_cli = QVBoxLayout()
        vbox_email_cli.addWidget(email_cli)
        vbox_email_cli.addWidget(self.edit_email_cli)

        #layout linha 2
        dados_cli_linha2 = QHBoxLayout()
        dados_cli_linha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dados_cli_linha2.addLayout(vbox_cep_cli)
        dados_cli_linha2.addLayout(vbox_end_cli)
        dados_cli_linha2.addLayout(vbox_num_cli)
        dados_cli_linha2.addLayout(vbox_bairro_cli)
        dados_cli_linha2.addLayout(vbox_cid_cli)
        dados_cli_linha2.addLayout(vbox_est_cli)
        dados_cli_linha2.addLayout(vbox_email_cli)

        # dados linha 2 --- fim ---

        # dados linha 3 --- início ---
        # telefone
        tel_cli = criar_label_padrao()
        tel_cli.setText('Telefone')
        tel_cli.setContentsMargins(2, 0, 0, 0)
        tel_cli.setFixedSize(tel_cli.sizeHint())

        self.edit_tel_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_cli.setFixedWidth(130)
        self.edit_tel_cli.setInputMask('(00)00000-0000;_')

        vbox_tel_cli = QVBoxLayout()
        vbox_tel_cli.addWidget(tel_cli)
        vbox_tel_cli.addWidget(self.edit_tel_cli)

        #CNPJ / CPF
        self.cnpj_cli = criar_label_padrao()
        self.edit_cnpj_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cnpj_cli.setFixedWidth(150)


        vbox_cnpj_cli = QVBoxLayout()
        vbox_cnpj_cli.addWidget(self.cnpj_cli)
        vbox_cnpj_cli.addWidget(self.edit_cnpj_cli)

        # Insc. Estadual
        self.insc_cli = criar_label_padrao()
        self.edit_insc_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_insc_cli.setFixedWidth(150)
        
        vbox_insc_cli = QVBoxLayout()
        vbox_insc_cli.addWidget(self.insc_cli)
        vbox_insc_cli.addWidget(self.edit_insc_cli)

        # Insc. Municipal
        insc_mun_cli = criar_label_padrao()
        insc_mun_cli.setText('Insc. Municipal')
        insc_mun_cli.setContentsMargins(2, 0, 0, 0)
        insc_mun_cli.setFixedSize(insc_mun_cli.sizeHint())

        self.edit_insc_mun_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_insc_mun_cli.setFixedWidth(150)
        
        vbox_insc_mun_cli = QVBoxLayout()
        vbox_insc_mun_cli.addWidget(insc_mun_cli)
        vbox_insc_mun_cli.addWidget(self.edit_insc_mun_cli)

        #data de nascimento
        self.dt_nasc_cli = criar_label_padrao()

        edit_dt_nasc_cli = criar_lineedit_padrao(LineEditComEnter)
        edit_dt_nasc_cli.setFixedWidth(100)
        edit_dt_nasc_cli.setInputMask('00/00/0000;_')

        vbox_dt_nasc_cli = QVBoxLayout()
        vbox_dt_nasc_cli.addWidget(self.dt_nasc_cli)
        vbox_dt_nasc_cli.addWidget(edit_dt_nasc_cli)

        #sexo funcionário
        sexo_cli = criar_label_padrao()
        sexo_cli.setText('Sexo')
        sexo_cli.setContentsMargins(2, 0, 0, 0)
        sexo_cli.setFixedSize(sexo_cli.sizeHint())

        comb_sexo_cli = criar_combobox_padrao()
        comb_sexo_cli.setFixedWidth(100)
        comb_sexo_cli.addItem('Selecione')
        comb_sexo_cli.addItem('Masculino')
        comb_sexo_cli.addItem('Feminino')
        comb_sexo_cli.model().item(0).setEnabled(False)

        vbox_sexo_cli = QVBoxLayout()
        vbox_sexo_cli.addWidget(sexo_cli)
        vbox_sexo_cli.addWidget(comb_sexo_cli)

        #Cidade nascimento

        nacion_cli = criar_label_padrao()
        nacion_cli.setText('Cidade Nascimento')
        nacion_cli.setContentsMargins(2, 0, 0, 0)
        nacion_cli.setFixedSize(nacion_cli.sizeHint())

        edit_nacion_cli = criar_lineedit_padrao(LineEditComEnter)
        edit_nacion_cli.setMinimumWidth(215)
        
        vbox_nacion_cli = QVBoxLayout()
        vbox_nacion_cli.addWidget(nacion_cli)
        vbox_nacion_cli.addWidget(edit_nacion_cli)

        #Pais nascimento
        
        natur_cli = criar_label_padrao()
        natur_cli.setText('País Nascimento')
        natur_cli.setContentsMargins(2, 0, 0, 0)
        natur_cli.setFixedSize(natur_cli.sizeHint())

        edit_natur_cli = criar_lineedit_padrao(LineEditComEnter)
        edit_natur_cli.setMinimumWidth(212)

        vbox_natur_cli = QVBoxLayout()
        vbox_natur_cli.addWidget(natur_cli)
        vbox_natur_cli.addWidget(edit_natur_cli)

        #layout linha 3
        dados_cli_linha3 = QHBoxLayout()
        dados_cli_linha3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dados_cli_linha3.addLayout(vbox_tel_cli)
        dados_cli_linha3.addLayout(vbox_cnpj_cli)
        dados_cli_linha3.addLayout(vbox_insc_cli)
        dados_cli_linha3.addLayout(vbox_insc_mun_cli)
        dados_cli_linha3.addLayout(vbox_dt_nasc_cli)
        dados_cli_linha3.addLayout(vbox_sexo_cli)
        dados_cli_linha3.addLayout(vbox_nacion_cli)
        dados_cli_linha3.addLayout(vbox_natur_cli)

        # dados linha 3 --- fim ---

        # dados linha 4 --- início ---

        #nome da mae
        nome_mae = criar_label_padrao()
        nome_mae.setText('Nome Mãe')
        nome_mae.setContentsMargins(2, 0, 0, 0)
        nome_mae.setFixedSize(nome_mae.sizeHint())

        edit_nome_mae = criar_lineedit_padrao(LineEditComEnter)
        edit_nome_mae.setFixedWidth(270)

        vbox_nome_mae = QVBoxLayout()
        vbox_nome_mae.addWidget(nome_mae)
        vbox_nome_mae.addWidget(edit_nome_mae)

        #nome do pai
        nome_pai = criar_label_padrao()
        nome_pai.setText('Nome Pai')
        nome_pai.setContentsMargins(2, 0, 0, 0)
        nome_pai.setFixedSize(nome_pai.sizeHint())

        edit_nome_pai = criar_lineedit_padrao(LineEditComEnter)
        edit_nome_pai.setFixedWidth(270)

        vbox_nome_pai = QVBoxLayout()
        vbox_nome_pai.addWidget(nome_pai)
        vbox_nome_pai.addWidget(edit_nome_pai)

        #layout linha 4
        dados_cli_linha4 = QHBoxLayout()
        dados_cli_linha4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dados_cli_linha4.addLayout(vbox_nome_mae)
        dados_cli_linha4.addLayout(vbox_nome_pai)

        # dados linha 4 --- fim ---

        # dados linha 5 --- início ---
        
        # informações adicionais 

        inf_add_cli = criar_label_padrao()
        inf_add_cli.setText('Informações adicionais')
        inf_add_cli.setContentsMargins(2, 0, 0, 0)
        inf_add_cli.setFixedSize(inf_add_cli.sizeHint())

        text_inf_add_cli = QTextEdit()
        text_inf_add_cli.setMinimumWidth(875)
        text_inf_add_cli.setMinimumHeight(70)
        text_inf_add_cli.setStyleSheet('background-color: white; font-size: 14px')

        vbox_inf_add_cli = QVBoxLayout()
        vbox_inf_add_cli.addWidget(inf_add_cli)
        vbox_inf_add_cli.addWidget(text_inf_add_cli)


        # layout linha 5
        dados_cli_linha5 = QHBoxLayout()
        dados_cli_linha5.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dados_cli_linha5.addLayout(vbox_inf_add_cli)
 
        # dados linha 5 --- fim ---

        # botoes aba 2
        botao_novo_fun = criar_botao()
        botao_novo_fun.setText('F5 - Novo')

        botao_canc_fun = criar_botao()
        botao_canc_fun.setText('Cancelar')

        botao_excl_fun = criar_botao()
        botao_excl_fun.setText('Excluir')

        hbox_botoes_dados = QHBoxLayout()
        hbox_botoes_dados.setAlignment(Qt.AlignmentFlag.AlignCenter )
        hbox_botoes_dados.addWidget(botao_novo_fun)
        hbox_botoes_dados.addSpacing(5)
        hbox_botoes_dados.addWidget(botao_canc_fun)
        hbox_botoes_dados.addSpacing(5)
        hbox_botoes_dados.addWidget(botao_excl_fun)
        hbox_botoes_dados.addStretch()

        #layout geral aba dados
        vbox_geral_aba_dados = QVBoxLayout()
        vbox_geral_aba_dados.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        vbox_geral_aba_dados.addLayout(dados_cli_linha1)
        vbox_geral_aba_dados.addLayout(dados_cli_linha2)
        vbox_geral_aba_dados.addLayout(dados_cli_linha3)
        vbox_geral_aba_dados.addLayout(dados_cli_linha4)
        vbox_geral_aba_dados.addLayout(dados_cli_linha5)
        vbox_geral_aba_dados.addSpacing(10)
        vbox_geral_aba_dados.addLayout(hbox_botoes_dados)
        vbox_geral_aba_dados.addSpacing(10)


        # adiciona layout na tela
        aba_dados.setLayout(vbox_geral_aba_dados)

        # criação aba referencia
        aba_ref = QWidget()

        #Referência linha 1 
        dad_prof = criar_label_padrao()
        dad_prof.setText('Dados Profissionais')
        dad_prof.setStyleSheet('font: bold;')
        dad_prof.setContentsMargins(2, 0, 0, 0)
        dad_prof.setFixedSize(dad_prof.sizeHint())

        vbox_dad_prof = QVBoxLayout()
        vbox_dad_prof.addWidget(dad_prof, alignment=Qt.AlignmentFlag.AlignLeft)

        hbox_ref_linha1 = QHBoxLayout()
        hbox_ref_linha1.addLayout(vbox_dad_prof)

        #Referência linha 2

        #local de trabalho
        loc_trab = criar_label_padrao()
        loc_trab.setText('Local Trabalho')
        loc_trab.setContentsMargins(2, 0, 0, 0)
        loc_trab.setFixedSize(loc_trab.sizeHint())

        edit_loc_trab = criar_lineedit_padrao(LineEditComEnter)
        edit_loc_trab.setMinimumWidth(180)

        vbox_loc_trab = QVBoxLayout()
        vbox_loc_trab.addWidget(loc_trab)
        vbox_loc_trab.addWidget(edit_loc_trab)

        #cargo
        carg_trab = criar_label_padrao()
        carg_trab.setText('Cargo')
        carg_trab.setContentsMargins(2, 0, 0, 0)
        carg_trab.setFixedSize(carg_trab.sizeHint())

        edit_carg_trab = criar_lineedit_padrao(LineEditComEnter)
        edit_carg_trab.setMinimumWidth(180)

        vbox_carg_trab = QVBoxLayout()
        vbox_carg_trab.addWidget(carg_trab)
        vbox_carg_trab.addWidget(edit_carg_trab)

        #tempo serviço
        temp_serv = criar_label_padrao()
        temp_serv.setText('Tempo Serv.')
        temp_serv.setContentsMargins(2, 0, 0, 0)
        temp_serv.setFixedSize(temp_serv.sizeHint())

        edit_temp_serv = criar_lineedit_padrao(LineEditComEnter)
        edit_temp_serv.setFixedWidth(160)

        vbox_temp_serv = QVBoxLayout()
        vbox_temp_serv.addWidget(temp_serv)
        vbox_temp_serv.addWidget(edit_temp_serv)

        #salário 
        salario = criar_label_padrao()
        salario.setText('Salário')
        salario.setContentsMargins(2, 0, 0, 0)
        salario.setFixedSize(salario.sizeHint())

        edit_salario = criar_lineedit_padrao(LineEditComEnter)
        edit_salario.setFixedWidth(100)

        vbox_salario = QVBoxLayout()
        vbox_salario.addWidget(salario)
        vbox_salario.addWidget(edit_salario)

        #telefone trabalho

        tel_trab = criar_label_padrao()
        tel_trab.setText('Telefone')
        tel_trab.setContentsMargins(2, 0, 0, 0)
        tel_trab.setFixedSize(tel_trab.sizeHint())

        edit_tel_trab = criar_lineedit_padrao(LineEditComEnter)
        edit_tel_trab.setFixedWidth(130)
        edit_tel_trab.setInputMask('(00)00000-0000;_')

        vbox_tel_trab = QVBoxLayout()
        vbox_tel_trab.addWidget(tel_trab)
        vbox_tel_trab.addWidget(edit_tel_trab)

        #layout referencias linha 2
        hbox_ref_linha2 = QHBoxLayout()
        hbox_ref_linha2.addLayout(vbox_loc_trab)
        hbox_ref_linha2.addLayout(vbox_carg_trab)
        hbox_ref_linha2.addLayout(vbox_temp_serv)
        hbox_ref_linha2.addLayout(vbox_salario)
        hbox_ref_linha2.addLayout(vbox_tel_trab)

        #referencias linha 3

        
        #cep trabalho
        cep_trab = criar_label_padrao()
        cep_trab.setText('CEP')
        cep_trab.setContentsMargins(2, 0, 0, 0)
        cep_trab.setFixedSize(cep_trab.sizeHint())

        self.edit_cep_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cep_trab.setFixedWidth(90)
        self.edit_cep_trab.setInputMask('00.000-000;_')
        self.edit_cep_trab.editingFinished.connect(self.buscar_cep)

        vbox_cep_trab = QVBoxLayout()
        vbox_cep_trab.addWidget(cep_trab)
        vbox_cep_trab.addWidget(self.edit_cep_trab)
        
        #endereço fornecedor 
        end_trab = criar_label_padrao()
        end_trab.setText('Endereço')
        end_trab.setContentsMargins(2, 0, 0, 0)
        end_trab.setFixedSize(end_trab.sizeHint())

        self.edit_end_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_end_trab.setMinimumWidth(335)

        vbox_end_trab = QVBoxLayout()
        vbox_end_trab.addWidget(end_trab)
        vbox_end_trab.addWidget(self.edit_end_trab)

        #número
        num_trab = criar_label_padrao()
        num_trab.setText('Número')
        num_trab.setContentsMargins(2, 0, 0, 0)
        num_trab.setFixedSize(num_trab.sizeHint())

        edit_num_trab = criar_lineedit_padrao(LineEditComEnter)
        edit_num_trab.setFixedWidth(80)

        vbox_num_trab = QVBoxLayout()
        vbox_num_trab.addWidget(num_trab)
        vbox_num_trab.addWidget(edit_num_trab)

        #bairro funcionário
        bairro_trab = criar_label_padrao()
        bairro_trab.setText('Bairro')
        bairro_trab.setContentsMargins(2, 0, 0, 0)
        bairro_trab.setFixedSize(bairro_trab.sizeHint())

        self.edit_bairro_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bairro_trab.setMinimumWidth(205)

        vbox_bairro_trab = QVBoxLayout()
        vbox_bairro_trab.addWidget(bairro_trab)
        vbox_bairro_trab.addWidget(self.edit_bairro_trab)

        #cidade fornecedor
        cid_trab = criar_label_padrao()
        cid_trab.setText('Cidade')
        cid_trab.setContentsMargins(2, 0, 0, 0)
        cid_trab.setFixedSize(cid_trab.sizeHint())

        self.edit_cid_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cid_trab.setMinimumWidth(220)

        vbox_cid_trab = QVBoxLayout()
        vbox_cid_trab.addWidget(cid_trab)
        vbox_cid_trab.addWidget(self.edit_cid_trab)

        #estado fornecetrab
        est_trab = criar_label_padrao()
        est_trab.setText('UF')
        est_trab.setContentsMargins(2, 0, 0, 0)
        est_trab.setFixedSize(est_trab.sizeHint())

        self.edit_est_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_est_trab.setFixedWidth(60)

        vbox_est_trab = QVBoxLayout()
        vbox_est_trab.addWidget(est_trab)
        vbox_est_trab.addWidget(self.edit_est_trab)

        #layout linha 3

        hbox_ref_linha3 = QHBoxLayout()
        hbox_ref_linha3.addLayout(vbox_cep_trab)
        hbox_ref_linha3.addLayout(vbox_end_trab)
        hbox_ref_linha3.addLayout(vbox_num_trab)
        hbox_ref_linha3.addLayout(vbox_bairro_trab)
        hbox_ref_linha3.addLayout(vbox_cid_trab)
        hbox_ref_linha3.addLayout(vbox_est_trab)

        # layout geral aba referencias
        vbox_geral_aba_ref = QVBoxLayout()
        vbox_geral_aba_ref.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        vbox_geral_aba_ref.addLayout(hbox_ref_linha1)
        vbox_geral_aba_ref.addLayout(hbox_ref_linha2)
        vbox_geral_aba_ref.addLayout(hbox_ref_linha3)


        aba_ref.setLayout(vbox_geral_aba_ref)

        # --------------------------------------------------

        table_cliente.addTab(aba_dados, "Dados")
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

        #adiciona layout 2 na tela
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
        vbox.setContentsMargins(20, 20, 20, 20)

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


    def atualiza_form(self):
        if self.check_jur.isChecked():
            self.cnpj_cli.setText('CNPJ')
            self.cnpj_cli.setContentsMargins(2, 0, 0, 0)
            self.cnpj_cli.setFixedSize(self.cnpj_cli.sizeHint())
            self.edit_cnpj_cli.setInputMask('00.000.000/0000-00;_')
            self.insc_cli.setText('Insc. Estadual')
            self.insc_cli.setContentsMargins(2, 0, 0, 0)
            self.insc_cli.setFixedSize(self.insc_cli.sizeHint())
            self.dt_nasc_cli.setText('Abertura')
            self.dt_nasc_cli.setContentsMargins(2, 0, 0, 0)
            self.dt_nasc_cli.setFixedSize(self.dt_nasc_cli.sizeHint())

        elif self.check_fis.isChecked():
            self.cnpj_cli.setText('CPF')
            self.cnpj_cli.setContentsMargins(2, 0, 0, 0)
            self.cnpj_cli.setFixedSize(self.cnpj_cli.sizeHint())
            self.edit_cnpj_cli.setInputMask('000.000.000-00;_')
            self.insc_cli.setText('RG')
            self.insc_cli.setContentsMargins(2, 0, 0, 0)
            self.insc_cli.setFixedSize(self.insc_cli.sizeHint())
            self.dt_nasc_cli.setText('Nascimento')
            self.dt_nasc_cli.setContentsMargins(2, 0, 0, 0)
            self.dt_nasc_cli.setFixedSize(self.dt_nasc_cli.sizeHint())


    def buscar_cep(self):
        # Descobre quem disparou o sinal
        origem = self.sender()
        if origem is None:
            return

        # Lê o CEP da origem e normaliza (somente dígitos)
        cep = ''.join(ch for ch in origem.text() if ch.isdigit())

        dados = consulta_cep(cep)

        # Seleciona widgets de destino conforme a origem
        if origem is self.edit_cep_cli:
            destino_end   = self.edit_end_cli
            destino_bairro= self.edit_bairro_cli
            destino_cidade= self.edit_cid_cli
            destino_uf    = self.edit_est_cli
        elif origem is self.edit_cep_trab:
            destino_end   = self.edit_end_trab
            destino_bairro= self.edit_bairro_trab
            destino_cidade= self.edit_cid_trab
            destino_uf    = self.edit_est_trab
        else:
            return

        if dados is None:
            QMessageBox.warning(self, "CEP inválido", "CEP não encontrado ou mal formatado.")
            # limpa os destinos e volta o foco
            destino_end.clear()
            destino_bairro.clear()
            destino_cidade.clear()
            destino_uf.clear()
            origem.setFocus()
            return

        if dados:  # veio resposta da API
            destino_end.setText(dados.get('logradouro', '').upper())
            destino_bairro.setText(dados.get('bairro', '').upper())
            destino_cidade.setText(dados.get('localidade', '').upper())
            destino_uf.setText(dados.get('uf', '').upper())
        # se dados == {}, você já tratou como "sem internet": não altera nada



    def ao_trocar_aba(self, index):
    # Aba 2 é a de Cadastro
        if index == 1:
            self.edit_raz_social.setFocus()
            self.check_jur.setChecked(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = CadCliente()
    janela.show()
    sys.exit(app.exec())
