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
from util.fun_basicas import consulta_cep, LineEditComEnter

class CadFuncionarios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro Funcionários")
        
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
        nometela = QLabel("Cadastro Funcionários")
        nometela.setStyleSheet("color: orange; font-size:38px; font: bold;")
        

        tab = criar_tab_widget()
        tab.currentChanged.connect(self.ao_trocar_aba)
        self.tab = tab  # guarda o tab como atributo se precisar


        # ----------- ABA 1 (Consulta) ------------
        aba1 = QWidget()
        aba1.setStyleSheet('background-color: #cbcdce;')

        dados_cons = criar_label_padrao()
        dados_cons.setText('Dados à consultar')
        dados_cons.setStyleSheet('font: bold')
        dados_cons.setContentsMargins(2, 0, 0, 0)
        dados_cons.setFixedSize(dados_cons.sizeHint())

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

        lnedit_pesq = criar_lineedit_padrao()
        lnedit_pesq.setFixedWidth(810)

        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_opc.addWidget(comb_opc, alignment=Qt.AlignmentFlag.AlignLeft)

        vbox_mdl = QVBoxLayout()
        vbox_mdl.addWidget(label_mdl, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_mdl.addWidget(comb_mdl, alignment=Qt.AlignmentFlag.AlignLeft)

        hbox_pesq = QHBoxLayout()
        hbox_pesq.addWidget(label_pesq, alignment=Qt.AlignmentFlag.AlignLeft)
        hbox_pesq.addWidget(check_todos, alignment=Qt.AlignmentFlag.AlignRight)

        vbox_pesq = QVBoxLayout()
        vbox_pesq.addLayout(hbox_pesq)
        vbox_pesq.addWidget(lnedit_pesq, alignment=Qt.AlignmentFlag.AlignLeft)

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
        self.tabela_resultado.setMaximumHeight(350)
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
        layout_geral_aba1.addWidget(dados_cons)
        layout_geral_aba1.addLayout(hbox_linha1)
        layout_geral_aba1.addLayout(vbox_linha2)
        layout_geral_aba1.addWidget(self.tabela_resultado)
        layout_geral_aba1.addSpacing(73)
        layout_geral_aba1.addLayout(hbox_botoes_rodape)
        layout_geral_aba1.addStretch()

        aba1.setLayout(layout_geral_aba1)

        # ----------- ABA 2 (Cadastro) ------------
        aba2 = QWidget()
        aba2.setStyleSheet('background-color: #cbcdce;')


        dados_pess = criar_label_padrao()
        dados_pess.setText('Dados Pessoais')
        dados_pess.setStyleSheet('font: bold')
        dados_pess.setContentsMargins(2, 0, 0, 0)

        # linha 1 --- início ---

        #código funcionário
        cod_func = criar_label_padrao()
        cod_func.setText('Código')
        cod_func.setContentsMargins(2, 0, 0, 0)
        cod_func.setFixedSize(cod_func.sizeHint())

        edit_cod = criar_lineedit_padrao(LineEditComEnter)
        edit_cod.setFixedWidth(90)

        vbox_cod_fun = QVBoxLayout()
        vbox_cod_fun.addWidget(cod_func)
        vbox_cod_fun.addWidget(edit_cod)


        #nome funcionário
        nome_func = criar_label_padrao()
        nome_func.setText('Nome do Funcionário')
        nome_func.setContentsMargins(2, 0, 0, 0)
        nome_func.setFixedSize(nome_func.sizeHint())

        self.edit_nome_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_func.setFixedWidth (435)

        vbox_nome_func = QVBoxLayout()
        vbox_nome_func.addWidget(nome_func, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_nome_func.addWidget(self.edit_nome_func)

        #apelido funcionario
        apelido_fun = criar_label_padrao()
        apelido_fun.setText('Apelido')
        apelido_fun.setContentsMargins(2, 0, 0, 0)
        apelido_fun.setFixedSize(apelido_fun.sizeHint())

        edit_apelido = criar_lineedit_padrao(LineEditComEnter)
        edit_apelido.setFixedWidth(200)

        vbox_apelido_func = QVBoxLayout()
        vbox_apelido_func.addWidget(apelido_fun, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_apelido_func.addWidget(edit_apelido)

        #cpf do funcionario
        cpf_func = criar_label_padrao()
        cpf_func.setText('CPF')
        cpf_func.setContentsMargins(2, 0, 0, 0)
        cpf_func.setFixedSize(cpf_func.sizeHint())

        edit_cpf_func = criar_lineedit_padrao(LineEditComEnter)
        edit_cpf_func.setFixedWidth(110)
        edit_cpf_func.setInputMask('000.000.000-00;_')

        vbox_cpf_func = QVBoxLayout()
        vbox_cpf_func.addWidget(cpf_func, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_cpf_func.addWidget(edit_cpf_func)

        #RG 
        rg_func = criar_label_padrao()
        rg_func.setText('RG')
        rg_func.setContentsMargins(2, 0, 0, 0)
        rg_func.setFixedSize(rg_func.sizeHint())

        edit_rg_func = criar_lineedit_padrao(LineEditComEnter)
        edit_rg_func.setFixedWidth(200)

        vbox_rg_func = QVBoxLayout()
        vbox_rg_func.addWidget(rg_func)
        vbox_rg_func.addWidget(edit_rg_func)

        #data de nascimento

        dt_nasc_func = criar_label_padrao()
        dt_nasc_func.setText('Nascimento')
        dt_nasc_func.setFixedSize(dt_nasc_func.sizeHint())

        edit_dt_nasc_func = criar_lineedit_padrao(LineEditComEnter)
        edit_dt_nasc_func.setFixedWidth(100)
        edit_dt_nasc_func.setInputMask('00/00/0000;_')


        vbox_dt_nasc_func = QVBoxLayout()
        vbox_dt_nasc_func.addWidget(dt_nasc_func)
        vbox_dt_nasc_func.addWidget(edit_dt_nasc_func)

        #sexo funcionário

        sexo_func = criar_label_padrao()
        sexo_func.setText('Sexo')
        sexo_func.setContentsMargins(2, 0, 0, 0)
        sexo_func.setFixedSize(sexo_func.sizeHint())

        comb_sexo_func = criar_combobox_padrao()
        comb_sexo_func.setFixedWidth(100)
        comb_sexo_func.addItem('Selecione')
        comb_sexo_func.addItem('Masculino')
        comb_sexo_func.addItem('Feminino')
        comb_sexo_func.model().item(0).setEnabled(False)

        vbox_sexo_func = QVBoxLayout()
        vbox_sexo_func.addWidget(sexo_func)
        vbox_sexo_func.addWidget(comb_sexo_func)

        #layout linha 1
        cad_linha1 = QHBoxLayout()
        cad_linha1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha1.addLayout(vbox_cod_fun)
        cad_linha1.addLayout(vbox_nome_func)
        cad_linha1.addLayout(vbox_apelido_func)
        cad_linha1.addLayout(vbox_cpf_func)
        cad_linha1.addLayout(vbox_rg_func)
        cad_linha1.addLayout(vbox_dt_nasc_func)
        cad_linha1.addLayout(vbox_sexo_func)

        # linha 1 --- fim ---

        # linha 2 --- início ---

        #endereço funcionário 
        end_func = criar_label_padrao()
        end_func.setText('Endereço')
        end_func.setContentsMargins(2, 0, 0, 0)
        end_func.setFixedSize(end_func.sizeHint())

        self.edit_end_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_end_func.setFixedWidth(390)

        vbox_end_func = QVBoxLayout()
        vbox_end_func.addWidget(end_func)
        vbox_end_func.addWidget(self.edit_end_func)


        #bairro funcionário
        bairro_func = criar_label_padrao()
        bairro_func.setText('Bairro')
        bairro_func.setContentsMargins(2, 0, 0, 0)
        bairro_func.setFixedSize(bairro_func.sizeHint())

        self.edit_bairro_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bairro_func.setFixedWidth(210)

        vbox_bairro_func = QVBoxLayout()
        vbox_bairro_func.addWidget(bairro_func)
        vbox_bairro_func.addWidget(self.edit_bairro_func)

        #cep funcionário
        cep_func = criar_label_padrao()
        cep_func.setText('CEP')
        cep_func.setContentsMargins(2, 0, 0, 0)
        cep_func.setFixedSize(cep_func.sizeHint())

        self.edit_cep_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cep_func.setFixedWidth(90)
        self.edit_cep_func.setInputMask('00.000-000;_')
        self.edit_cep_func.editingFinished.connect(self.buscar_cep)

        vbox_cep_func = QVBoxLayout()
        vbox_cep_func.addWidget(cep_func)
        vbox_cep_func.addWidget(self.edit_cep_func)

        #cidade funcionário
        cid_func = criar_label_padrao()
        cid_func.setText('Cidade')
        cid_func.setContentsMargins(2, 0, 0, 0)
        cid_func.setFixedSize(cid_func.sizeHint())

        self.edit_cid_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cid_func.setFixedWidth(225)

        vbox_cid_func = QVBoxLayout()
        vbox_cid_func.addWidget(cid_func)
        vbox_cid_func.addWidget(self.edit_cid_func)

        #estado funcionario
        est_func = criar_label_padrao()
        est_func.setText('UF')
        est_func.setContentsMargins(2, 0, 0, 0)
        est_func.setFixedSize(est_func.sizeHint())

        self.edit_est_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_est_func.setFixedWidth(60)

        vbox_est_func = QVBoxLayout()
        vbox_est_func.addWidget(est_func)
        vbox_est_func.addWidget(self.edit_est_func)

        #WhatsApp
        zap_func = criar_label_padrao()
        zap_func.setText('WhatsApp')
        zap_func.setContentsMargins(2, 0, 0, 0)
        zap_func.setFixedSize(zap_func.sizeHint())

        edit_zap_func = criar_lineedit_padrao(LineEditComEnter)
        edit_zap_func.setFixedWidth(130)
        edit_zap_func.setInputMask('(00)00000-0000;_')

        vbox_zap_func = QVBoxLayout()
        vbox_zap_func.addWidget(zap_func)
        vbox_zap_func.addWidget(edit_zap_func)


        #Telefone
        tel_func = criar_label_padrao()
        tel_func.setText('Telefone')
        tel_func.setContentsMargins(2, 0, 0, 0)
        tel_func.setFixedSize(zap_func.sizeHint())

        edit_tel_func = criar_lineedit_padrao(LineEditComEnter)
        edit_tel_func.setFixedWidth(130)
        edit_tel_func.setInputMask('(00)00000-0000;_')

        vbox_tel_func = QVBoxLayout()
        vbox_tel_func.addWidget(tel_func)
        vbox_tel_func.addWidget(edit_tel_func)

        #layout linha 2
        cad_linha2 = QHBoxLayout()
        cad_linha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha2.addLayout(vbox_cep_func)
        cad_linha2.addLayout(vbox_end_func)
        cad_linha2.addLayout(vbox_bairro_func)
        cad_linha2.addLayout(vbox_cid_func)
        cad_linha2.addLayout(vbox_est_func)
        cad_linha2.addLayout(vbox_zap_func)
        cad_linha2.addLayout(vbox_tel_func)
       
        # linha 2 --- fim ----

        # linha 3 --- início

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

        #Cidade nascimento

        nacion_func = criar_label_padrao()
        nacion_func.setText('Cidade Nascimento')
        nacion_func.setContentsMargins(2, 0, 0, 0)
        nacion_func.setFixedSize(nacion_func.sizeHint())

        edit_nacion_func = criar_lineedit_padrao(LineEditComEnter)
        edit_nacion_func.setFixedWidth(200)
        
        vbox_nacion_func = QVBoxLayout()
        vbox_nacion_func.addWidget(nacion_func)
        vbox_nacion_func.addWidget(edit_nacion_func)

        #Pais nascimento
        
        natur_func = criar_label_padrao()
        natur_func.setText('País Nascimento')
        natur_func.setContentsMargins(2, 0, 0, 0)
        natur_func.setFixedSize(natur_func.sizeHint())

        edit_natur_func = criar_lineedit_padrao(LineEditComEnter)
        edit_natur_func.setFixedWidth(200)

        vbox_natur_func = QVBoxLayout()
        vbox_natur_func.addWidget(natur_func)
        vbox_natur_func.addWidget(edit_natur_func)

        #e-mail
        email_func = criar_label_padrao()
        email_func.setText('e-mail')
        email_func.setContentsMargins(2, 0 , 0, 0)
        email_func.setFixedSize(email_func.sizeHint())

        edit_email_func = criar_lineedit_padrao(LineEditComEnter)
        edit_email_func.setFixedWidth(305)

        vbox_email_fun = QVBoxLayout()
        vbox_email_fun.addWidget(email_func)
        vbox_email_fun.addWidget(edit_email_func)

        #layout linha 3
        cad_linha3 = QHBoxLayout()
        cad_linha3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha3.addLayout(vbox_nome_mae)
        cad_linha3.addLayout(vbox_nome_pai)
        cad_linha3.addLayout(vbox_nacion_func)
        cad_linha3.addLayout(vbox_natur_func)
        cad_linha3.addLayout(vbox_email_fun)

        # linha 3 --- fim ---


        # dados profissionais


        dados_prof = criar_label_padrao()
        dados_prof.setText('Dados Profissionais')
        dados_prof.setStyleSheet('font: bold')
        dados_prof.setContentsMargins(2, 0, 0, 0)

        # linha 4 --- inicio ---

        # data admissão
        dt_admis = criar_label_padrao()
        dt_admis.setText('Admissão')
        dt_admis.setContentsMargins(2, 0, 0, 0)
        dt_admis.setFixedSize(dt_admis.sizeHint())

        edit_admis = criar_lineedit_padrao(LineEditComEnter)
        edit_admis.setFixedWidth(100)
        edit_admis.setInputMask('00/00/0000;_')

        vbox_admis = QVBoxLayout()
        vbox_admis.addWidget(dt_admis)
        vbox_admis.addWidget(edit_admis)


        # salario
        sal_fun = criar_label_padrao()
        sal_fun.setText('Salário')
        sal_fun.setContentsMargins(2, 0, 0, 0)
        sal_fun.setFixedSize(sal_fun.sizeHint())

        edit_sal_fun = criar_lineedit_padrao(LineEditComEnter)
        edit_sal_fun.setFixedWidth(100)

        vbox_sal_fun = QVBoxLayout()
        vbox_sal_fun.addWidget(sal_fun)
        vbox_sal_fun.addWidget(edit_sal_fun)

        # cargo
        cargo_fun = criar_label_padrao()
        cargo_fun.setText('Cargo')
        cargo_fun.setContentsMargins(2, 0, 0, 0)
        cargo_fun.setFixedSize(cargo_fun.sizeHint())

        comb_cargo_fun = criar_combobox_padrao()
        comb_cargo_fun.setFixedWidth(200)
        comb_cargo_fun.addItem('Selecione')
        comb_cargo_fun.model().item(0).setEnabled(False)

        vbox_cargo_fun = QVBoxLayout()
        vbox_cargo_fun.addWidget(cargo_fun)
        vbox_cargo_fun.addWidget(comb_cargo_fun)

        #carteira trabalho

        cart_trab = criar_label_padrao()
        cart_trab.setText('Carteira Trabalho')
        cart_trab.setContentsMargins(2, 0, 0, 0)
        cart_trab.setFixedSize(cart_trab.sizeHint())

        edit_cart_trab = criar_lineedit_padrao(LineEditComEnter)
        edit_cart_trab.setFixedWidth(200)

        vbox_cart_trab = QVBoxLayout()
        vbox_cart_trab.addWidget(cart_trab)
        vbox_cart_trab.addWidget(edit_cart_trab)

        #Pis/Pasep

        pis_func = criar_label_padrao()
        pis_func.setText('PIS / PASEP')
        pis_func.setContentsMargins(2, 0, 0, 0)
        pis_func.setFixedSize(pis_func.sizeHint())


        edit_pis_func = criar_lineedit_padrao(LineEditComEnter)
        edit_pis_func.setFixedWidth(250)

        vbox_pis_func = QVBoxLayout()
        vbox_pis_func.addWidget(pis_func)
        vbox_pis_func.addWidget(edit_pis_func)



        # layout linha 4
        cad_linha4 = QHBoxLayout()
        cad_linha4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha4.addLayout(vbox_admis)
        cad_linha4.addLayout(vbox_sal_fun)
        cad_linha4.addLayout(vbox_cargo_fun)
        cad_linha4.addLayout(vbox_cart_trab)
        cad_linha4.addLayout(vbox_pis_func) 

        # linha 4 --- fim ---

        # linha 5 --- início ---

        # data demissão

        dt_demis = criar_label_padrao()
        dt_demis.setText('Demissão')
        dt_demis.setContentsMargins(2, 0, 0, 0)
        dt_demis.setFixedSize(dt_demis.sizeHint())

        edit_demis = criar_lineedit_padrao(LineEditComEnter)
        edit_demis.setFixedWidth(100)
        edit_demis.setInputMask('00/00/0000;_')

        vbox_demis_func = QVBoxLayout()
        vbox_demis_func.addWidget(dt_demis)
        vbox_demis_func.addWidget(edit_demis)

        # motivo demissão

        mot_demis = criar_label_padrao()
        mot_demis.setText('Motivo demissão')
        mot_demis.setContentsMargins(2, 0, 0, 0)
        mot_demis.setFixedSize(mot_demis.sizeHint())

        edit_mot_demis = criar_lineedit_padrao(LineEditComEnter)
        edit_mot_demis.setFixedWidth(770)

        vbox_mot_demis = QVBoxLayout()
        vbox_mot_demis.addWidget(mot_demis)
        vbox_mot_demis.addWidget(edit_mot_demis)


        #layout linha 5
        cad_linha5 = QHBoxLayout()
        cad_linha5.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha5.addLayout(vbox_demis_func)
        cad_linha5.addLayout(vbox_mot_demis)
        
        # linha 5 --- fim ---

        # linha 6 --- inicio ---


        # informações adicionais 

        inf_add_func = criar_label_padrao()
        inf_add_func.setText('Informações adicionais')
        inf_add_func.setContentsMargins(2, 0, 0, 0)
        inf_add_func.setFixedSize(inf_add_func.sizeHint())

        text_inf_add_func = QTextEdit()
        text_inf_add_func.setFixedSize(875, 70)
        text_inf_add_func.setStyleSheet('background-color: white; font-size: 14px')

        vbox_inf_add_func = QVBoxLayout()
        vbox_inf_add_func.addWidget(inf_add_func)
        vbox_inf_add_func.addWidget(text_inf_add_func)
 

        cad_linha6 = QHBoxLayout()
        cad_linha6.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha6.addLayout(vbox_inf_add_func)
        
        vbox_linhas = QVBoxLayout()
        vbox_linhas.addLayout(cad_linha4)
        vbox_linhas.addLayout(cad_linha5)
        vbox_linhas.addLayout(cad_linha6)


        # Foto do funcionário
        self.lbl_foto = QLabel("Foto")
        self.lbl_foto.setFixedSize(150, 200)
        self.lbl_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_foto.setStyleSheet("""
            background-color: white;
            border: 1px solid #999;
            font-size: 12px;
            color: gray;
        """)



        hbox_linha_foto = QHBoxLayout()
        hbox_linha_foto.addLayout(vbox_linhas)
        hbox_linha_foto.addStretch()  # antes da foto
        hbox_linha_foto.addWidget(self.lbl_foto, alignment=Qt.AlignmentFlag.AlignTop)
        hbox_linha_foto.addSpacing(80)


        botao_novo_fun = criar_botao()
        botao_novo_fun.setText('F5 - Novo')

        botao_canc_fun = criar_botao()
        botao_canc_fun.setText('Cancelar')

        botao_excl_fun = criar_botao()
        botao_excl_fun.setText('Excluir')

        hbox_botoes_aba2 = QHBoxLayout()
        hbox_botoes_aba2.setAlignment(Qt.AlignmentFlag.AlignCenter )
        hbox_botoes_aba2.addWidget(botao_novo_fun)
        hbox_botoes_aba2.addSpacing(5)
        hbox_botoes_aba2.addWidget(botao_canc_fun)
        hbox_botoes_aba2.addSpacing(5)
        hbox_botoes_aba2.addWidget(botao_excl_fun)
        hbox_botoes_aba2.addStretch()

        #layout geral apresentação na tela aba2

        layout_geral_aba2 = QVBoxLayout()
        layout_geral_aba2.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba2.addWidget(dados_pess)
        layout_geral_aba2.addLayout(cad_linha1)
        layout_geral_aba2.addLayout(cad_linha2)
        layout_geral_aba2.addLayout(cad_linha3)
        layout_geral_aba2.addWidget(dados_prof)
        layout_geral_aba2.addLayout(hbox_linha_foto)
        layout_geral_aba2.addSpacing(95)
        layout_geral_aba2.addLayout(hbox_botoes_aba2)
        layout_geral_aba2.addStretch()


        aba2.setLayout(layout_geral_aba2)

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
        vbox.setContentsMargins(110, 20, 110, 0)

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

    def buscar_cep(self):
        cep = self.edit_cep_func.text()
        dados = consulta_cep(cep)

        if dados is None:
            QMessageBox.warning(self, "CEP inválido", "CEP não encontrado ou mal formatado.")
        elif dados:
            self.edit_end_func.setText(dados.get('logradouro', '').upper())
            self.edit_bairro_func.setText(dados.get('bairro', '').upper())
            self.edit_cid_func.setText(dados.get('localidade', '').upper())
            self.edit_est_func.setText(dados.get('uf', '').upper())
        # Se dados == {}, significa sem internet → não faz nada


    def ao_trocar_aba(self, index):
    # Aba 2 é a de Cadastro
        if index == 1:
            self.edit_nome_func.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = CadFuncionarios()
    janela.show()
    sys.exit(app.exec())
