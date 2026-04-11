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
from util.fun_basicas import consulta_cep, LineEditComEnter, validar_cnpj, validar_cpf

class CadFornecedor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro Fornecedores")
        
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
        nometela = QLabel("Cadastro de Fornecedores")
        nometela.setStyleSheet("color: orange; font-size:38px; font: bold")

        tab = criar_tab_widget()
        tab.currentChanged.connect(self.ao_trocar_aba)
        self.tab = tab  # guarda o tab como atributo se precisar

        # ----------- ABA 1 (Consulta) ------------
        aba1 = QWidget()
        aba1.setStyleSheet('background-color: #cbcdce;')

        label_opc = criar_label_padrao()
        label_opc.setText('Opções')
        label_opc.setContentsMargins(2, 0, 0, 0)
        label_opc.setFixedSize(label_opc.sizeHint())

        self.comb_opc = criar_combobox_padrao()
        self.comb_opc.addItem("Nome/Razão Sócial")
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

        self.lnedit_pesq = criar_lineedit_padrao()
        self.lnedit_pesq.setMinimumWidth(810)

        vbox_opc = QVBoxLayout()
        vbox_opc.addWidget(label_opc)
        vbox_opc.addWidget(self.comb_opc)

        vbox_mdl = QVBoxLayout()
        vbox_mdl.addWidget(label_mdl)
        vbox_mdl.addWidget(self.comb_mdl)

        hbox_pesq = QHBoxLayout()
        hbox_pesq.addWidget(label_pesq)
        hbox_pesq.addWidget(self.check_todos)

        vbox_pesq = QVBoxLayout()
        vbox_pesq.addLayout(hbox_pesq)
        vbox_pesq.addWidget(self.lnedit_pesq)

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
        self.tabela_resultado.setHorizontalHeaderLabels(["Código", "Nome / Razão Sócial", "Contato", "Status"])
        self.tabela_resultado.setStyleSheet("background-color: white; font-size: 13px")
        self.tabela_resultado.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_resultado.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_resultado.setAlternatingRowColors(True)
        self.tabela_resultado.setMinimumHeight(300)
        

        #botões controle novo, relatório

        self.botao_novo = criar_botao()
        self.botao_novo.setText('F5 - Novo')

        self.botao_relat = criar_botao()
        self.botao_relat.setText('Relatórios')

        hbox_botoes_rodape = QHBoxLayout()
        hbox_botoes_rodape.setAlignment(Qt.AlignmentFlag.AlignCenter )
        hbox_botoes_rodape.addWidget(self.botao_novo)
        hbox_botoes_rodape.addSpacing(5)
        hbox_botoes_rodape.addWidget(self.botao_relat)
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

        # linha 1 --- inicio ---

        # código fornecedor
        cod_for = criar_label_padrao()
        cod_for.setText('Código')
        cod_for.setContentsMargins(2, 0, 0, 0)
        cod_for.setFixedSize(cod_for.sizeHint())

        self.edit_cod_for = criar_lineedit_padrao()
        self.edit_cod_for.setFixedWidth(90)
        self.edit_cod_for.setReadOnly(True)

        vbox_cod_for = QVBoxLayout()
        vbox_cod_for.addWidget(cod_for)
        vbox_cod_for.addWidget(self.edit_cod_for)

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
        fant_forn = criar_label_padrao()
        fant_forn.setText('Nome Fantasia/Apelido')
        fant_forn.setContentsMargins(2, 0, 0, 0)
        fant_forn.setFixedSize(fant_forn.sizeHint())

        self.edit_fant_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_fant_forn.setMinimumWidth(400)
        self.edit_fant_forn.setContentsMargins(0,1,0,0)

        vbox_fant_forn = QVBoxLayout()
        vbox_fant_forn.addWidget(fant_forn, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_fant_forn.addWidget(self.edit_fant_forn)

        #contato 

        cont_forn = criar_label_padrao()
        cont_forn.setText('Nome Contato')
        cont_forn.setContentsMargins(2, 0, 0, 0)
        cont_forn.setFixedSize(cont_forn.sizeHint())

        self.edit_cont_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cont_forn.setMinimumWidth(180)

        vbox_cont_forn = QVBoxLayout()
        vbox_cont_forn.addWidget(cont_forn)
        vbox_cont_forn.addWidget(self.edit_cont_forn)

        #WhatsApp
        zap_forn = criar_label_padrao()
        zap_forn.setText('WhatsApp')
        zap_forn.setContentsMargins(2, 0, 0, 0)
        zap_forn.setFixedSize(zap_forn.sizeHint())

        self.edit_zap_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_zap_forn.setFixedWidth(130)
        self.edit_zap_forn.setInputMask('(00)00000-0000;_')

        vbox_zap_forn = QVBoxLayout()
        vbox_zap_forn.addWidget(zap_forn)
        vbox_zap_forn.addWidget(self.edit_zap_forn)

        # layout linha 1
        forn_linha1 = QHBoxLayout()
        forn_linha1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        forn_linha1.addLayout(vbox_cod_for)
        forn_linha1.addLayout(vbox_raz_social)
        forn_linha1.addLayout(vbox_fant_forn)
        forn_linha1.addLayout(vbox_cont_forn)
        forn_linha1.addLayout(vbox_zap_forn)

        # linha 1 --- fim ---

        # linha 2 --- inicio ---
        
        #cep fornecedor
        cep_forn = criar_label_padrao()
        cep_forn.setText('CEP')
        cep_forn.setContentsMargins(2, 0, 0, 0)
        cep_forn.setFixedSize(cep_forn.sizeHint())

        self.edit_cep_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cep_forn.setFixedWidth(90)
        self.edit_cep_forn.setInputMask('00.000-000;_')
        self.edit_cep_forn.editingFinished.connect(self.buscar_cep)

        vbox_cep_forn = QVBoxLayout()
        vbox_cep_forn.addWidget(cep_forn)
        vbox_cep_forn.addWidget(self.edit_cep_forn)
        
        #endereço fornecedor 
        end_forn = criar_label_padrao()
        end_forn.setText('Endereço')
        end_forn.setContentsMargins(2, 0, 0, 0)
        end_forn.setFixedSize(end_forn.sizeHint())

        self.edit_end_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_end_forn.setMinimumWidth(280)

        vbox_end_forn = QVBoxLayout()
        vbox_end_forn.addWidget(end_forn)
        vbox_end_forn.addWidget(self.edit_end_forn)

        #Número Funcionário

        num_for = criar_label_padrao()
        num_for.setText('Número')
        num_for.setContentsMargins(2, 0, 0, 0)
        num_for.setFixedSize(num_for.sizeHint())

        self.edit_num_for = criar_lineedit_padrao(LineEditComEnter)
        self.edit_num_for.setFixedWidth(80)

        vbox_num_for = QVBoxLayout()
        vbox_num_for.addWidget(num_for)
        vbox_num_for.addWidget(self.edit_num_for)

        #bairro funcionário
        bairro_forn = criar_label_padrao()
        bairro_forn.setText('Bairro')
        bairro_forn.setContentsMargins(2, 0, 0, 0)
        bairro_forn.setFixedSize(bairro_forn.sizeHint())

        self.edit_bairro_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bairro_forn.setMinimumWidth(205)

        vbox_bairro_forn = QVBoxLayout()
        vbox_bairro_forn.addWidget(bairro_forn)
        vbox_bairro_forn.addWidget(self.edit_bairro_forn)

        #cidade fornecedor
        cid_forn = criar_label_padrao()
        cid_forn.setText('Cidade')
        cid_forn.setContentsMargins(2, 0, 0, 0)
        cid_forn.setFixedSize(cid_forn.sizeHint())

        self.edit_cid_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cid_forn.setMinimumWidth(220)

        vbox_cid_forn = QVBoxLayout()
        vbox_cid_forn.addWidget(cid_forn)
        vbox_cid_forn.addWidget(self.edit_cid_forn)

        #estado fornecedor
        est_forn = criar_label_padrao()
        est_forn.setText('UF')
        est_forn.setContentsMargins(2, 0, 0, 0)
        est_forn.setFixedSize(est_forn.sizeHint())

        self.edit_est_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_est_forn.setFixedWidth(60)

        vbox_est_forn = QVBoxLayout()
        vbox_est_forn.addWidget(est_forn)
        vbox_est_forn.addWidget(self.edit_est_forn)

        #e-mail fornecedor
        email_forn = criar_label_padrao()
        email_forn.setText('e-mail')
        email_forn.setContentsMargins(2, 0 , 0, 0)
        email_forn.setFixedSize(email_forn.sizeHint())

        self.edit_email_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_email_forn.setFixedWidth(305)

        vbox_email_forn = QVBoxLayout()
        vbox_email_forn.addWidget(email_forn)
        vbox_email_forn.addWidget(self.edit_email_forn)

        #layout linha 2
        forn_linha2 = QHBoxLayout()
        forn_linha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        forn_linha2.addLayout(vbox_cep_forn)
        forn_linha2.addLayout(vbox_end_forn)
        forn_linha2.addLayout(vbox_num_for)
        forn_linha2.addLayout(vbox_bairro_forn)
        forn_linha2.addLayout(vbox_cid_forn)
        forn_linha2.addLayout(vbox_est_forn)
        forn_linha2.addLayout(vbox_email_forn)

        # linha 2 --- fim ---

        # linha 3 --- início ---

        # telefone
        tel_forn = criar_label_padrao()
        tel_forn.setText('Telefone')
        tel_forn.setContentsMargins(2, 0, 0, 0)
        tel_forn.setFixedSize(tel_forn.sizeHint())

        self.edit_tel_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_forn.setFixedWidth(130)
        self.edit_tel_forn.setInputMask('(00)00000-0000;_')

        vbox_tel_forn = QVBoxLayout()
        vbox_tel_forn.addWidget(tel_forn)
        vbox_tel_forn.addWidget(self.edit_tel_forn)

        #CNPJ / CPF
        self.cnpj_forn = criar_label_padrao()
        self.edit_cnpj_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cnpj_forn.setFixedWidth(150)
        self.edit_cnpj_forn.editingFinished.connect(self.validar_documento)


        vbox_cnpj_forn = QVBoxLayout()
        vbox_cnpj_forn.addWidget(self.cnpj_forn)
        vbox_cnpj_forn.addWidget(self.edit_cnpj_forn)

        # Insc. Estadual
        self.insc_forn = criar_label_padrao()
        self.edit_insc_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_insc_forn.setFixedWidth(150)
        
        vbox_insc_forn = QVBoxLayout()
        vbox_insc_forn.addWidget(self.insc_forn)
        vbox_insc_forn.addWidget(self.edit_insc_forn)

        # Insc. Municipal
        insc_mun_forn = criar_label_padrao()
        insc_mun_forn.setText('Insc. Municipal')
        insc_mun_forn.setContentsMargins(2, 0, 0, 0)
        insc_mun_forn.setFixedSize(insc_mun_forn.sizeHint())

        self.edit_insc_mun_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_insc_mun_forn.setFixedWidth(150)
        
        vbox_insc_mun_forn = QVBoxLayout()
        vbox_insc_mun_forn.addWidget(insc_mun_forn)
        vbox_insc_mun_forn.addWidget(self.edit_insc_mun_forn)

        #data de nascimento
        self.dt_nasc_forn = criar_label_padrao()

        self.edit_dt_nasc_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_dt_nasc_forn.setFixedWidth(100)
        self.edit_dt_nasc_forn.setInputMask('00/00/0000;_')

        vbox_dt_nasc_forn = QVBoxLayout()
        vbox_dt_nasc_forn.addWidget(self.dt_nasc_forn)
        vbox_dt_nasc_forn.addWidget(self.edit_dt_nasc_forn)

        #sexo funcionário
        sexo_forn = criar_label_padrao()
        sexo_forn.setText('Sexo')
        sexo_forn.setContentsMargins(2, 0, 0, 0)
        sexo_forn.setFixedSize(sexo_forn.sizeHint())

        self.comb_sexo_forn = criar_combobox_padrao()
        self.comb_sexo_forn.setFixedWidth(100)
        self.comb_sexo_forn.addItem('Selecione')
        self.comb_sexo_forn.addItem('Masculino')
        self.comb_sexo_forn.addItem('Feminino')
        self.comb_sexo_forn.model().item(0).setEnabled(False)

        vbox_sexo_forn = QVBoxLayout()
        vbox_sexo_forn.addWidget(sexo_forn)
        vbox_sexo_forn.addWidget(self.comb_sexo_forn)

        #layout linha 3
        forn_linha3 = QHBoxLayout()
        forn_linha3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        forn_linha3.addLayout(vbox_tel_forn)
        forn_linha3.addLayout(vbox_cnpj_forn)
        forn_linha3.addLayout(vbox_insc_forn)
        forn_linha3.addLayout(vbox_insc_mun_forn)
        forn_linha3.addLayout(vbox_dt_nasc_forn)
        forn_linha3.addLayout(vbox_sexo_forn)

        # linha 3 --- fim ---

        # linha 4 --- início ---

        inf_add_forn = criar_label_padrao()
        inf_add_forn.setText('Informações adicionais')
        inf_add_forn.setContentsMargins(2, 0, 0, 0)
        inf_add_forn.setFixedSize(inf_add_forn.sizeHint())

        self.text_inf_add_forn = QTextEdit()
        self.text_inf_add_forn.setMinimumWidth(875)
        self.text_inf_add_forn.setMinimumHeight(70)
        self.text_inf_add_forn.setStyleSheet('background-color: white; font-size: 14px')

        vbox_inf_add_forn = QVBoxLayout()
        vbox_inf_add_forn.addWidget(inf_add_forn)
        vbox_inf_add_forn.addWidget(self.text_inf_add_forn)
 
        forn_linha4 = QHBoxLayout()
        forn_linha4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        forn_linha4.addLayout(vbox_inf_add_forn)
        
        # linha 4 --- fim ---
        
        # botoes aba 2
        self.botao_novo_fornecedor = criar_botao()
        self.botao_novo_fornecedor.setText('F5 - Novo')

        self.botao_canc_fornecedor = criar_botao()
        self.botao_canc_fornecedor.setText('Cancelar')

        self.botao_excl_fornecedor = criar_botao()
        self.botao_excl_fornecedor.setText('Excluir')

        hbox_botoes_aba2 = QHBoxLayout()
        hbox_botoes_aba2.setAlignment(Qt.AlignmentFlag.AlignCenter )
        hbox_botoes_aba2.addWidget(self.botao_novo_fornecedor)
        hbox_botoes_aba2.addSpacing(5)
        hbox_botoes_aba2.addWidget(self.botao_canc_fornecedor)
        hbox_botoes_aba2.addSpacing(5)
        hbox_botoes_aba2.addWidget(self.botao_excl_fornecedor)
        hbox_botoes_aba2.addStretch()

        # layout geral aba 2
        layout_geral_aba2 = QVBoxLayout()
        layout_geral_aba2.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba2.addLayout(forn_linha1)
        layout_geral_aba2.addLayout(forn_linha2)
        layout_geral_aba2.addLayout(forn_linha3)
        layout_geral_aba2.addLayout(forn_linha4)
        layout_geral_aba2.addSpacing(10)
        layout_geral_aba2.addLayout(hbox_botoes_aba2)
        layout_geral_aba2.addSpacing(10)


        aba2.setLayout(layout_geral_aba2)

        # ----------- Tabs ----------
        tab.addTab(aba1, "Consulta")
        tab.addTab(aba2, "Cadastro")

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

        # ----------- Layout Principal ----------
        vbox = QVBoxLayout()
        vbox.addWidget(nometela, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(tab)
        vbox.addLayout(hbox_botoes)
        vbox.setContentsMargins(20, 20, 20, 20)

        self.setLayout(vbox)



    def salvar(self):
        razao_social = self.edit_raz_social.text().strip().upper()
        cpf_cnpj = self.edit_cnpj_forn.text().strip()

        if not razao_social:
            QMessageBox.warning(self, "Aviso", "Razão social / nome é obrigatório.")
            self.edit_raz_social.setFocus()
            return

        if self.check_jur.isChecked():
            tipo_pessoa = "J"
        elif self.check_fis.isChecked():
            tipo_pessoa = "F"
        else:
            QMessageBox.warning(self, "Aviso", "Selecione Jurídica ou Física.")
            return

        numeros_doc = "".join(filter(str.isdigit, cpf_cnpj))

        if numeros_doc:
            if tipo_pessoa == "J":
                if len(numeros_doc) != 14:
                    QMessageBox.warning(self, "Aviso", "CNPJ inválido.")
                    self.edit_cnpj_forn.setFocus()
                    self.edit_cnpj_forn.selectAll()
                    return

                # troque validar_cnpj pela sua função
                if not validar_cnpj(numeros_doc):
                    QMessageBox.warning(self, "Aviso", "CNPJ inválido.")
                    self.edit_cnpj_forn.setFocus()
                    self.edit_cnpj_forn.selectAll()
                    return

            elif tipo_pessoa == "F":
                if len(numeros_doc) != 11:
                    QMessageBox.warning(self, "Aviso", "CPF inválido.")
                    self.edit_cnpj_forn.setFocus()
                    self.edit_cnpj_forn.selectAll()
                    return

                # troque validar_cpf pela sua função
                if not validar_cpf(numeros_doc):
                    QMessageBox.warning(self, "Aviso", "CPF inválido.")
                    self.edit_cnpj_forn.setFocus()
                    self.edit_cnpj_forn.selectAll()
                    return

        ativo = "S" if self.combo_ativo.currentText() != "Inativo" else "N"

        dados = {
            "codigo": self.edit_cod_for.text().strip(),
            "tipo_pessoa": tipo_pessoa,
            "razao_social": self.edit_raz_social.text().strip().upper(),
            "nome_fantasia": self.edit_fant_forn.text().strip().upper(),
            "contato": self.edit_cont_forn.text().strip().upper(),
            "whatsapp": self.edit_zap_forn.text().strip(),
            "telefone": self.edit_tel_forn.text().strip(),
            "email": self.edit_email_forn.text().strip().lower(),
            "cep": self.edit_cep_forn.text().strip(),
            "endereco": self.edit_end_forn.text().strip().upper(),
            "numero": self.edit_num_for.text().strip(),
            "bairro": self.edit_bairro_forn.text().strip().upper(),
            "cidade": self.edit_cid_forn.text().strip().upper(),
            "uf": self.edit_est_forn.text().strip().upper(),
            "cpf_cnpj": cpf_cnpj,
            "inscricao_estadual": self.edit_insc_forn.text().strip().upper(),
            "inscricao_municipal": self.edit_insc_mun_forn.text().strip().upper(),
            "data_referencia": self.edit_dt_nasc_forn.text().strip(),
            "sexo": self.comb_sexo_forn.currentText() if self.comb_sexo_forn.currentText() != "Selecione" else "",
            "info_adicional": self.text_inf_add_forn.toPlainText().strip().upper(),
            "ativo": ativo
        }

        from bd import salvar_fornecedor
        resultado = salvar_fornecedor(dados)

        if resultado == "existe":
            QMessageBox.warning(self, "Aviso", "Fornecedor já cadastrado.")
            self.edit_cnpj_forn.setFocus()
            self.edit_cnpj_forn.selectAll()

        elif resultado:
            QMessageBox.information(self, "Sucesso", "Fornecedor salvo com sucesso!")
            self.limpar_campos()

        else:
            QMessageBox.critical(self, "Erro", "Erro ao salvar fornecedor.")

    def limpar_campos(self):
        self.edit_cod_for.clear()
        self.edit_raz_social.clear()
        self.edit_fant_forn.clear()
        self.edit_cont_forn.clear()
        self.edit_zap_forn.clear()
        self.edit_tel_forn.clear()
        self.edit_email_forn.clear()

        self.edit_cep_forn.clear()
        self.edit_end_forn.clear()
        self.edit_num_for.clear()
        self.edit_bairro_forn.clear()
        self.edit_cid_forn.clear()
        self.edit_est_forn.clear()

        self.edit_cnpj_forn.clear()
        self.edit_insc_forn.clear()
        self.edit_insc_mun_forn.clear()
        self.edit_dt_nasc_forn.clear()

        self.text_inf_add_forn.clear()

        self.comb_sexo_forn.setCurrentIndex(0)

        self.check_jur.setChecked(False)
        self.check_fis.setChecked(False)

        self.edit_raz_social.setFocus()

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
        cep = self.edit_cep_forn.text()
        dados = consulta_cep(cep)

        if dados is None:
            QMessageBox.warning(self, "CEP inválido", "CEP não encontrado ou mal formatado.")
        elif dados:
            self.edit_end_forn.setText(dados.get('logradouro', '').upper())
            self.edit_bairro_forn.setText(dados.get('bairro', '').upper())
            self.edit_cid_forn.setText(dados.get('localidade', '').upper())
            self.edit_est_forn.setText(dados.get('uf', '').upper())
        # Se dados == {}, significa sem internet → não faz nada


    def ao_trocar_aba(self, index):
    # Aba 2 é a de Cadastro
        if index == 1:
            self.edit_raz_social.setFocus()
            self.check_jur.setChecked(True)

        
    def atualiza_form(self):
        if self.check_jur.isChecked():
            self.cnpj_forn.setText('CNPJ')
            self.cnpj_forn.setContentsMargins(2, 0, 0, 0)
            self.cnpj_forn.setFixedSize(self.cnpj_forn.sizeHint())
            self.edit_cnpj_forn.setInputMask('00.000.000/0000-00;_')
            self.insc_forn.setText('Insc. Estadual')
            self.insc_forn.setContentsMargins(2, 0, 0, 0)
            self.insc_forn.setFixedSize(self.insc_forn.sizeHint())
            self.dt_nasc_forn.setText('Abertura')
            self.dt_nasc_forn.setContentsMargins(2, 0, 0, 0)
            self.dt_nasc_forn.setFixedSize(self.dt_nasc_forn.sizeHint())

        elif self.check_fis.isChecked():
            self.cnpj_forn.setText('CPF')
            self.cnpj_forn.setContentsMargins(2, 0, 0, 0)
            self.cnpj_forn.setFixedSize(self.cnpj_forn.sizeHint())
            self.edit_cnpj_forn.setInputMask('000.000.000-00;_')
            self.insc_forn.setText('RG')
            self.insc_forn.setContentsMargins(2, 0, 0, 0)
            self.insc_forn.setFixedSize(self.insc_forn.sizeHint())
            self.dt_nasc_forn.setText('Nascimento')
            self.dt_nasc_forn.setContentsMargins(2, 0, 0, 0)
            self.dt_nasc_forn.setFixedSize(self.dt_nasc_forn.sizeHint())

    def validar_documento(self):
        from util.fun_basicas import validar_cpf, validar_cnpj

        doc = self.edit_cnpj_forn.text().strip()
        numeros = ''.join(filter(str.isdigit, doc))

        if not numeros:
            return  # campo vazio passa

        if self.check_jur.isChecked():
            if len(numeros) != 14 or not validar_cnpj(numeros):
                QMessageBox.warning(self, "Aviso", "CNPJ inválido.")
                self.edit_cnpj_forn.setFocus()
                self.edit_cnpj_forn.selectAll()
                return

        elif self.check_fis.isChecked():
            if len(numeros) != 11 or not validar_cpf(numeros):
                QMessageBox.warning(self, "Aviso", "CPF inválido.")
                self.edit_cnpj_forn.setFocus()
                self.edit_cnpj_forn.selectAll()
                return

        else:
            QMessageBox.warning(self, "Aviso", "Selecione Jurídica ou Física.")
            self.check_jur.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = CadFornecedor()
    janela.show()
    sys.exit(app.exec())
