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
from entidades.funcionario.funcionario_service import FuncionarioService
from entidades.funcionario.dialog_senha_funcionario import DialogSenhaFuncionario


class CadFuncionarios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro Funcionários")
        self.service = FuncionarioService()
        self.status_atual = "A"

        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagens', 'icone.png'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"[ERRO] Icone não encontrado: {icon_path}")

        self.componentes()
        self.showMaximized()

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)
        QShortcut(QKeySequence('F8'), self).activated.connect(self.acao_buscar_funcionario)
        QShortcut(QKeySequence('F5'), self).activated.connect(self.novo_funcionario)

    def componentes(self):
        nometela = QLabel("Cadastro de Funcionários")
        nometela.setStyleSheet("color: orange; font-size:38px; font: bold;")

        tab = criar_tab_widget()
        tab.currentChanged.connect(self.ao_trocar_aba)
        self.tab = tab

        aba1 = QWidget()
        aba1.setStyleSheet('background-color: #cbcdce;')

        dados_cons = criar_label_padrao()
        dados_cons.setText('Dados a consultar')
        dados_cons.setStyleSheet('font: bold')

        label_opc = criar_label_padrao()
        label_opc.setText('Opcões')

        self.comb_opc = criar_combobox_padrao()
        self.comb_opc.addItems(["Código", "Nome", "CPF", "Cargo"])
        self.comb_opc.setCurrentText("Nome")
        self.comb_opc.setFixedWidth(220)

        label_mdl = criar_label_padrao()
        label_mdl.setText('Modelo')

        self.comb_mdl = criar_combobox_padrao()
        self.comb_mdl.addItem('Iniciar com...')
        self.comb_mdl.setFixedWidth(220)

        label_pesq = criar_label_padrao()
        label_pesq.setText('Dados a pesquisar')

        self.check_todos = QCheckBox("Todos")

        self.lnedit_pesq = criar_lineedit_padrao()
        self.lnedit_pesq.setMinimumWidth(810)
        self.lnedit_pesq.textChanged.connect(self.acao_buscar_funcionario)

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
        vbox_pesq.addWidget(self.lnedit_pesq)

        hbox_linha1 = QHBoxLayout()
        hbox_linha1.addLayout(vbox_opc)
        hbox_linha1.addLayout(vbox_mdl)
        hbox_linha1.addLayout(vbox_pesq)

        label_ativo = criar_label_padrao()
        label_ativo.setText('Status')

        self.combo_ativo = criar_combobox_padrao()
        self.combo_ativo.addItems(["Ativos", "Excluídos", "Todos"])
        self.combo_ativo.setFixedWidth(220)

        self.btn_pesq = criar_botao()
        self.btn_pesq.setText("F8 - Pesquisa")
        self.btn_pesq.clicked.connect(self.acao_buscar_funcionario)

        hbox_linha2 = QHBoxLayout()
        hbox_linha2.addWidget(self.combo_ativo, alignment=Qt.AlignmentFlag.AlignLeft)
        hbox_linha2.addWidget(self.btn_pesq)

        vbox_linha2 = QVBoxLayout()
        vbox_linha2.addWidget(label_ativo, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_linha2.addLayout(hbox_linha2)

        self.tabela_resultado = QTableWidget()
        self.tabela_resultado.setColumnCount(6)
        self.tabela_resultado.setHorizontalHeaderLabels(["Código", "Nome", "Cargo","WhatsApp","E-mail", "Status"])
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
        self.tabela_resultado.setMinimumHeight(180)
        self.tabela_resultado.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabela_resultado.verticalHeader().setVisible(False)
        self.tabela_resultado.itemDoubleClicked.connect(self.abrir_funcionario_selecionado)

        self.tabela_resultado.setColumnWidth(0, 70)    # Código
        self.tabela_resultado.setColumnWidth(1, 360)   # Nome 
        self.tabela_resultado.setColumnWidth(2, 170)   # CPF 
        self.tabela_resultado.setColumnWidth(3, 140)   # WhatsApp
        self.tabela_resultado.setColumnWidth(4, 220)   # E-mail
        self.tabela_resultado.setColumnWidth(5, 100)   # Status

        self.botao_novo = criar_botao()
        self.botao_novo.setText('F5 - Novo')
        self.botao_novo.clicked.connect(self.novo_funcionario)

        self.botao_relat = criar_botao()
        self.botao_relat.setText('Relatorios')

        hbox_botoes_rodape = QHBoxLayout()
        hbox_botoes_rodape.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox_botoes_rodape.addWidget(self.botao_novo)
        hbox_botoes_rodape.addSpacing(5)
        hbox_botoes_rodape.addWidget(self.botao_relat)
        hbox_botoes_rodape.addStretch()

        layout_geral_aba1 = QVBoxLayout()
        layout_geral_aba1.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba1.addWidget(dados_cons)
        layout_geral_aba1.addLayout(hbox_linha1)
        layout_geral_aba1.addLayout(vbox_linha2)
        layout_geral_aba1.addWidget(self.tabela_resultado)
        layout_geral_aba1.addSpacing(10)
        layout_geral_aba1.addLayout(hbox_botoes_rodape)
        layout_geral_aba1.addSpacing(10)
        aba1.setLayout(layout_geral_aba1)

        aba2 = QWidget()
        aba2.setStyleSheet('background-color: #cbcdce;')

        dados_pess = criar_label_padrao()
        dados_pess.setText('Dados Pessoais')
        dados_pess.setStyleSheet('font: bold')

        cod_func = criar_label_padrao()
        cod_func.setText('Código')
        self.edit_cod = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cod.setFixedWidth(90)
        self.edit_cod.setReadOnly(True)
        vbox_cod_fun = QVBoxLayout()
        vbox_cod_fun.addWidget(cod_func)
        vbox_cod_fun.addWidget(self.edit_cod)

        nome_func = criar_label_padrao()
        nome_func.setText('Nome do Funcionario')
        self.edit_nome_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_func.setMinimumWidth(435)
        vbox_nome_func = QVBoxLayout()
        vbox_nome_func.addWidget(nome_func)
        vbox_nome_func.addWidget(self.edit_nome_func)

        apelido_fun = criar_label_padrao()
        apelido_fun.setText('Apelido')
        self.edit_apelido = criar_lineedit_padrao(LineEditComEnter)
        self.edit_apelido.setMinimumWidth(200)
        self.edit_apelido.setMaximumWidth(300)
        vbox_apelido_func = QVBoxLayout()
        vbox_apelido_func.addWidget(apelido_fun)
        vbox_apelido_func.addWidget(self.edit_apelido)

        cpf_func = criar_label_padrao()
        cpf_func.setText('CPF')
        self.edit_cpf_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cpf_func.setFixedWidth(110)
        self.edit_cpf_func.setInputMask('000.000.000-00;_')
        vbox_cpf_func = QVBoxLayout()
        vbox_cpf_func.addWidget(cpf_func, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_cpf_func.addWidget(self.edit_cpf_func)

        rg_func = criar_label_padrao()
        rg_func.setText('RG')
        self.edit_rg_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_rg_func.setFixedWidth(200)
        vbox_rg_func = QVBoxLayout()
        vbox_rg_func.addWidget(rg_func)
        vbox_rg_func.addWidget(self.edit_rg_func)

        dt_nasc_func = criar_label_padrao()
        dt_nasc_func.setText('Nascimento')
        self.edit_dt_nasc_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_dt_nasc_func.setFixedWidth(100)
        self.edit_dt_nasc_func.setInputMask('00/00/0000;_')
        vbox_dt_nasc_func = QVBoxLayout()
        vbox_dt_nasc_func.addWidget(dt_nasc_func)
        vbox_dt_nasc_func.addWidget(self.edit_dt_nasc_func)

        sexo_func = criar_label_padrao()
        sexo_func.setText('Sexo')
        self.comb_sexo_func = criar_combobox_padrao()
        self.comb_sexo_func.setFixedWidth(100)
        self.comb_sexo_func.addItems(['Selecione', 'Masculino', 'Feminino'])
        self.comb_sexo_func.model().item(0).setEnabled(False)
        vbox_sexo_func = QVBoxLayout()
        vbox_sexo_func.addWidget(sexo_func)
        vbox_sexo_func.addWidget(self.comb_sexo_func)

        cad_linha1 = QHBoxLayout()
        cad_linha1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha1.addLayout(vbox_cod_fun)
        cad_linha1.addLayout(vbox_nome_func)
        cad_linha1.addLayout(vbox_apelido_func)
        cad_linha1.addLayout(vbox_cpf_func)
        cad_linha1.addLayout(vbox_rg_func)
        cad_linha1.addLayout(vbox_dt_nasc_func)
        cad_linha1.addLayout(vbox_sexo_func)

        end_func = criar_label_padrao()
        end_func.setText('Endereco')
        self.edit_end_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_end_func.setMinimumWidth(35)
        self.edit_end_func.setMaximumWidth(450)
        vbox_end_func = QVBoxLayout()
        vbox_end_func.addWidget(end_func)
        vbox_end_func.addWidget(self.edit_end_func)

        num_func = criar_label_padrao()
        num_func.setText('Numero')
        self.edit_num_fun = criar_lineedit_padrao(LineEditComEnter)
        self.edit_num_fun.setFixedWidth(80)
        vbox_num_func = QVBoxLayout()
        vbox_num_func.addWidget(num_func)
        vbox_num_func.addWidget(self.edit_num_fun)

        bairro_func = criar_label_padrao()
        bairro_func.setText('Bairro')
        self.edit_bairro_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bairro_func.setMinimumWidth(210)
        vbox_bairro_func = QVBoxLayout()
        vbox_bairro_func.addWidget(bairro_func)
        vbox_bairro_func.addWidget(self.edit_bairro_func)

        cep_func = criar_label_padrao()
        cep_func.setText('CEP')
        self.edit_cep_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cep_func.setFixedWidth(90)
        self.edit_cep_func.setInputMask('00.000-000;_')
        self.edit_cep_func.editingFinished.connect(self.buscar_cep)
        vbox_cep_func = QVBoxLayout()
        vbox_cep_func.addWidget(cep_func)
        vbox_cep_func.addWidget(self.edit_cep_func)

        cid_func = criar_label_padrao()
        cid_func.setText('Cidade')
        self.edit_cid_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cid_func.setMinimumWidth(225)
        vbox_cid_func = QVBoxLayout()
        vbox_cid_func.addWidget(cid_func)
        vbox_cid_func.addWidget(self.edit_cid_func)

        est_func = criar_label_padrao()
        est_func.setText('UF')
        self.edit_est_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_est_func.setFixedWidth(60)
        vbox_est_func = QVBoxLayout()
        vbox_est_func.addWidget(est_func)
        vbox_est_func.addWidget(self.edit_est_func)

        zap_func = criar_label_padrao()
        zap_func.setText('WhatsApp')
        self.edit_zap_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_zap_func.setFixedWidth(130)
        self.edit_zap_func.setInputMask('(00)00000-0000;_')
        vbox_zap_func = QVBoxLayout()
        vbox_zap_func.addWidget(zap_func)
        vbox_zap_func.addWidget(self.edit_zap_func)

        tel_func = criar_label_padrao()
        tel_func.setText('Telefone')
        self.edit_tel_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_func.setFixedWidth(130)
        self.edit_tel_func.setInputMask('(00)00000-0000;_')
        vbox_tel_func = QVBoxLayout()
        vbox_tel_func.addWidget(tel_func)
        vbox_tel_func.addWidget(self.edit_tel_func)

        cad_linha2 = QHBoxLayout()
        cad_linha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha2.addLayout(vbox_cep_func)
        cad_linha2.addLayout(vbox_end_func)
        cad_linha2.addLayout(vbox_num_func)
        cad_linha2.addLayout(vbox_bairro_func)
        cad_linha2.addLayout(vbox_cid_func)
        cad_linha2.addLayout(vbox_est_func)
        cad_linha2.addLayout(vbox_zap_func)
        cad_linha2.addLayout(vbox_tel_func)

        nome_mae = criar_label_padrao()
        nome_mae.setText('Nome Mãe')
        self.edit_nome_mae = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_mae.setMinimumWidth(270)
        vbox_nome_mae = QVBoxLayout()
        vbox_nome_mae.addWidget(nome_mae)
        vbox_nome_mae.addWidget(self.edit_nome_mae)

        nome_pai = criar_label_padrao()
        nome_pai.setText('Nome Pai')
        self.edit_nome_pai = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_pai.setMinimumWidth(270)
        vbox_nome_pai = QVBoxLayout()
        vbox_nome_pai.addWidget(nome_pai)
        vbox_nome_pai.addWidget(self.edit_nome_pai)

        nacion_func = criar_label_padrao()
        nacion_func.setText('Cidade Nascimento')
        self.edit_nacion_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nacion_func.setMinimumWidth(200)
        vbox_nacion_func = QVBoxLayout()
        vbox_nacion_func.addWidget(nacion_func)
        vbox_nacion_func.addWidget(self.edit_nacion_func)

        natur_func = criar_label_padrao()
        natur_func.setText('Pais Nascimento')
        self.edit_natur_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_natur_func.setFixedWidth(200)
        vbox_natur_func = QVBoxLayout()
        vbox_natur_func.addWidget(natur_func)
        vbox_natur_func.addWidget(self.edit_natur_func)

        email_func = criar_label_padrao()
        email_func.setText('E-mail')
        self.edit_email_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_email_func.setFixedWidth(305)
        vbox_email_fun = QVBoxLayout()
        vbox_email_fun.addWidget(email_func)
        vbox_email_fun.addWidget(self.edit_email_func)

        cad_linha3 = QHBoxLayout()
        cad_linha3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha3.addLayout(vbox_nome_mae)
        cad_linha3.addLayout(vbox_nome_pai)
        cad_linha3.addLayout(vbox_nacion_func)
        cad_linha3.addLayout(vbox_natur_func)
        cad_linha3.addLayout(vbox_email_fun)

        dados_prof = criar_label_padrao()
        dados_prof.setText('Dados Profissionais')
        dados_prof.setStyleSheet('font: bold')

        dt_admis = criar_label_padrao()
        dt_admis.setText('Admissão')
        self.edit_admis = criar_lineedit_padrao(LineEditComEnter)
        self.edit_admis.setFixedWidth(100)
        self.edit_admis.setInputMask('00/00/0000;_')
        vbox_admis = QVBoxLayout()
        vbox_admis.addWidget(dt_admis)
        vbox_admis.addWidget(self.edit_admis)

        sal_fun = criar_label_padrao()
        sal_fun.setText('Salário')
        self.edit_sal_fun = criar_lineedit_padrao(LineEditComEnter)
        self.edit_sal_fun.setFixedWidth(100)
        vbox_sal_fun = QVBoxLayout()
        vbox_sal_fun.addWidget(sal_fun)
        vbox_sal_fun.addWidget(self.edit_sal_fun)

        cargo_fun = criar_label_padrao()
        cargo_fun.setText('Cargo')
        self.comb_cargo_fun = criar_combobox_padrao()
        self.comb_cargo_fun.setFixedWidth(200)
        self.comb_cargo_fun.addItems(['Selecione', 'ANALISTA', 'GERENTE', 'SUPERVISOR', 'VENDEDOR', 'CAIXA'])
        self.comb_cargo_fun.model().item(0).setEnabled(False)
        vbox_cargo_fun = QVBoxLayout()
        vbox_cargo_fun.addWidget(cargo_fun)
        vbox_cargo_fun.addWidget(self.comb_cargo_fun)

        cart_trab = criar_label_padrao()
        cart_trab.setText('Carteira Trabalho')
        self.edit_cart_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cart_trab.setMinimumWidth(245)
        vbox_cart_trab = QVBoxLayout()
        vbox_cart_trab.addWidget(cart_trab)
        vbox_cart_trab.addWidget(self.edit_cart_trab)

        pis_func = criar_label_padrao()
        pis_func.setText('PIS / PASEP')
        self.edit_pis_func = criar_lineedit_padrao(LineEditComEnter)
        self.edit_pis_func.setMinimumWidth(290)
        vbox_pis_func = QVBoxLayout()
        vbox_pis_func.addWidget(pis_func)
        vbox_pis_func.addWidget(self.edit_pis_func)

        cad_linha4 = QHBoxLayout()
        cad_linha4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha4.addLayout(vbox_admis)
        cad_linha4.addLayout(vbox_sal_fun)
        cad_linha4.addLayout(vbox_cargo_fun)
        cad_linha4.addLayout(vbox_cart_trab)
        cad_linha4.addLayout(vbox_pis_func)

        dt_demis = criar_label_padrao()
        dt_demis.setText('Demissão')
        self.edit_demis = criar_lineedit_padrao(LineEditComEnter)
        self.edit_demis.setFixedWidth(100)
        self.edit_demis.setInputMask('00/00/0000;_')
        vbox_demis_func = QVBoxLayout()
        vbox_demis_func.addWidget(dt_demis)
        vbox_demis_func.addWidget(self.edit_demis)

        mot_demis = criar_label_padrao()
        mot_demis.setText('Motivo demissão')
        self.edit_mot_demis = criar_lineedit_padrao(LineEditComEnter)
        self.edit_mot_demis.setMinimumWidth(855)
        vbox_mot_demis = QVBoxLayout()
        vbox_mot_demis.addWidget(mot_demis)
        vbox_mot_demis.addWidget(self.edit_mot_demis)

        cad_linha5 = QHBoxLayout()
        cad_linha5.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha5.addLayout(vbox_demis_func)
        cad_linha5.addLayout(vbox_mot_demis)

        inf_add_func = criar_label_padrao()
        inf_add_func.setText('Informacões adicionais')
        self.text_inf_add_func = QTextEdit()
        self.text_inf_add_func.setMinimumWidth(750)
        self.text_inf_add_func.setMinimumHeight(50)
        self.text_inf_add_func.setStyleSheet('background-color: white; font-size: 14px')
        vbox_inf_add_func = QVBoxLayout()
        vbox_inf_add_func.addWidget(inf_add_func)
        vbox_inf_add_func.addWidget(self.text_inf_add_func)

        cad_linha6 = QHBoxLayout()
        cad_linha6.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha6.addLayout(vbox_inf_add_func)

        vbox_linhas = QVBoxLayout()
        vbox_linhas.addLayout(cad_linha4)
        vbox_linhas.addLayout(cad_linha5)
        vbox_linhas.addLayout(cad_linha6)

        self.lbl_foto = QLabel("Foto")
        self.lbl_foto.setFixedSize(150, 200)
        self.lbl_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_foto.setStyleSheet("""
            background-color: white;
            border: 1px solid #999;
            font-size: 12px;
            color: gray;
        """)

        self.btn_cad_senha = criar_botao()
        self.btn_cad_senha.setText('Cadastrar Senha')
        self.btn_cad_senha.clicked.connect(self.abrir_dialog_senha)
        
        vbox_foto = QVBoxLayout()
        vbox_foto.addWidget(self.lbl_foto)
        vbox_foto.addWidget(self.btn_cad_senha, Qt.AlignmentFlag.AlignVCenter, Qt.AlignmentFlag.AlignHCenter)

        hbox_linha_foto = QHBoxLayout()
        hbox_linha_foto.addLayout(vbox_linhas)
        hbox_linha_foto.addSpacing(80)
        hbox_linha_foto.addLayout(vbox_foto)
        hbox_linha_foto.addSpacing(80)

        self.botao_novo_fun = criar_botao()
        self.botao_novo_fun.setText('F5 - Novo')
        self.botao_novo_fun.clicked.connect(self.novo_funcionario)

        self.botao_canc_fun = criar_botao()
        self.botao_canc_fun.setText('Cancelar')
        self.botao_canc_fun.clicked.connect(self.cancelar)

        self.botao_excl_fun = criar_botao()
        self.botao_excl_fun.setText('Excluir / Ativar')
        self.botao_excl_fun.clicked.connect(self.alterar_status_funcionario)


        hbox_botoes_aba2 = QHBoxLayout()
        hbox_botoes_aba2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox_botoes_aba2.addWidget(self.botao_novo_fun)
        hbox_botoes_aba2.addSpacing(5)
        hbox_botoes_aba2.addWidget(self.botao_canc_fun)
        hbox_botoes_aba2.addSpacing(5)
        hbox_botoes_aba2.addWidget(self.botao_excl_fun)
        hbox_botoes_aba2.addStretch()

        layout_geral_aba2 = QVBoxLayout()
        layout_geral_aba2.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba2.addWidget(dados_pess)
        layout_geral_aba2.addLayout(cad_linha1)
        layout_geral_aba2.addLayout(cad_linha2)
        layout_geral_aba2.addLayout(cad_linha3)
        layout_geral_aba2.addWidget(dados_prof)
        layout_geral_aba2.addLayout(hbox_linha_foto)
        layout_geral_aba2.addSpacing(10)
        layout_geral_aba2.addLayout(hbox_botoes_aba2)
        layout_geral_aba2.addSpacing(10)
        aba2.setLayout(layout_geral_aba2)

        tab.addTab(aba1, "Consulta")
        tab.addTab(aba2, "Cadastro")

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

        vbox = QVBoxLayout()
        vbox.addWidget(nometela, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(tab)
        vbox.addLayout(hbox_botoes)
        vbox.setContentsMargins(20, 20, 20, 20)
        self.setLayout(vbox)

    def salvar(self):
        dados = self.coletar_dados_formulario()
        if dados["codigo"]:
            resultado = self.service.atualizar_funcionario(dados)
        else:
            resultado = self.service.salvar_funcionario(dados)

        if resultado["sucesso"]:
            QMessageBox.information(self, "Sucesso", resultado["mensagem"])
            self.limpar_campos()
            self.tab.setCurrentIndex(0)
            self.acao_buscar_funcionario()
            return

        QMessageBox.warning(self, "Aviso", resultado["mensagem"])
        if "Nome" in resultado["mensagem"]:
            self.edit_nome_func.setFocus()
        elif "CPF" in resultado["mensagem"] or "cadastrado" in resultado["mensagem"]:
            self.edit_cpf_func.setFocus()
            self.edit_cpf_func.selectAll()

    def coletar_dados_formulario(self):
        return {
            "codigo": self.edit_cod.text().strip(),
            "nome": self.edit_nome_func.text().strip(),
            "apelido": self.edit_apelido.text().strip(),
            "cpf": self.edit_cpf_func.text().strip(),
            "rg": self.edit_rg_func.text().strip(),
            "data_nascimento": self.edit_dt_nasc_func.text().strip(),
            "sexo": self.comb_sexo_func.currentText() if self.comb_sexo_func.currentText() != 'Selecione' else "",
            "cep": self.edit_cep_func.text().strip(),
            "endereco": self.edit_end_func.text().strip(),
            "numero": self.edit_num_fun.text().strip(),
            "bairro": self.edit_bairro_func.text().strip(),
            "cidade": self.edit_cid_func.text().strip(),
            "estado": self.edit_est_func.text().strip(),
            "whatsapp": self.edit_zap_func.text().strip(),
            "telefone": self.edit_tel_func.text().strip(),
            "nome_mae": self.edit_nome_mae.text().strip(),
            "nome_pai": self.edit_nome_pai.text().strip(),
            "cidade_nascimento": self.edit_nacion_func.text().strip(),
            "pais_nascimento": self.edit_natur_func.text().strip(),
            "email": self.edit_email_func.text().strip(),
            "data_admissao": self.edit_admis.text().strip(),
            "salario": self.edit_sal_fun.text().strip(),
            "cargo": self.comb_cargo_fun.currentText() if self.comb_cargo_fun.currentText() != 'Selecione' else "",
            "carteira_trabalho": self.edit_cart_trab.text().strip(),
            "pis_pasep": self.edit_pis_func.text().strip(),
            "data_demissao": self.edit_demis.text().strip(),
            "motivo_demissao": self.edit_mot_demis.text().strip(),
            "info_adicional": self.text_inf_add_func.toPlainText().strip(),
            "status": self.status_atual,
        }

    def limpar_campos(self):
        self.status_atual = "A"
        for campo in (
            self.edit_cod, self.edit_nome_func, self.edit_apelido, self.edit_cpf_func, self.edit_rg_func,
            self.edit_dt_nasc_func, self.edit_cep_func, self.edit_end_func, self.edit_num_fun, self.edit_bairro_func,
            self.edit_cid_func, self.edit_est_func, self.edit_zap_func, self.edit_tel_func, self.edit_nome_mae,
            self.edit_nome_pai, self.edit_nacion_func, self.edit_natur_func, self.edit_email_func, self.edit_admis,
            self.edit_sal_fun, self.edit_cart_trab, self.edit_pis_func, self.edit_demis, self.edit_mot_demis,
        ):
            campo.clear()

        self.text_inf_add_func.clear()
        self.comb_sexo_func.setCurrentIndex(0)
        self.comb_cargo_fun.setCurrentIndex(0)
        self.edit_nome_func.setFocus()


    def acao_buscar_funcionario(self, *args):
        texto = self.lnedit_pesq.text().strip()
        opcao = self.comb_opc.currentText()
        status = self.combo_ativo.currentText()
        buscar_todos = self.check_todos.isChecked()

        if not texto and not buscar_todos:
            self.tabela_resultado.setRowCount(0)
            return

        resultados = self.service.buscar_funcionario(opcao, texto, status, buscar_todos)
        self.tabela_resultado.setRowCount(len(resultados))

        for linha, funcionario in enumerate(resultados):
            valores = [
                funcionario.get("codigo", ""),
                funcionario.get("nome", ""),
                funcionario.get("cargo", ""),
                funcionario.get("whatsapp", ""),
                funcionario.get("email", ""),
                funcionario.get("status", ""),
            ]

            for coluna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor) if valor is not None else "")

                if coluna == 5:
                    if valor == "A":
                        item.setText("Ativo")
                    elif valor == "E":
                        item.setText("Excluído")
                        item.setForeground(Qt.GlobalColor.red)

                self.tabela_resultado.setItem(linha, coluna, item)


    def abrir_funcionario_selecionado(self):
        linha = self.tabela_resultado.currentRow()
        if linha == -1:
            return

        codigo_item = self.tabela_resultado.item(linha, 0)
        if codigo_item is None:
            return

        funcionario = self.service.buscar_por_codigo(codigo_item.text())
        if not funcionario:
            return

        self.carregar_funcionario_no_formulario(funcionario)
        self.tab.setCurrentIndex(1)

    def carregar_funcionario_no_formulario(self, funcionario):
        self.edit_cod.setText(funcionario.get("codigo") or "")
        self.edit_nome_func.setText(funcionario.get("nome") or "")
        self.edit_apelido.setText(funcionario.get("apelido") or "")
        self.edit_cpf_func.setText(funcionario.get("cpf") or "")
        self.edit_rg_func.setText(funcionario.get("rg") or "")
        self.edit_cep_func.setText(funcionario.get("cep") or "")
        self.edit_end_func.setText(funcionario.get("endereco") or "")
        self.edit_num_fun.setText(funcionario.get("numero") or "")
        self.edit_bairro_func.setText(funcionario.get("bairro") or "")
        self.edit_cid_func.setText(funcionario.get("cidade") or "")
        self.edit_est_func.setText(funcionario.get("estado") or "")
        self.edit_zap_func.setText(funcionario.get("whatsapp") or "")
        self.edit_tel_func.setText(funcionario.get("telefone") or "")
        self.edit_nome_mae.setText(funcionario.get("nome_mae") or "")
        self.edit_nome_pai.setText(funcionario.get("nome_pai") or "")
        self.edit_nacion_func.setText(funcionario.get("cidade_nascimento") or "")
        self.edit_natur_func.setText(funcionario.get("pais_nascimento") or "")
        self.edit_email_func.setText(funcionario.get("email") or "")
        self.edit_sal_fun.setText(str(funcionario.get("salario") or ""))
        self.edit_cart_trab.setText(funcionario.get("carteira_trabalho") or "")
        self.edit_pis_func.setText(funcionario.get("pis_pasep") or "")
        self.edit_mot_demis.setText(funcionario.get("motivo_demissao") or "")
        self.text_inf_add_func.setPlainText(funcionario.get("info_adicional") or "")
        self.status_atual = funcionario.get("status") or "A"

        for widget, valor in ((self.edit_dt_nasc_func, funcionario.get("data_nascimento")), (self.edit_admis, funcionario.get("data_admissao")), (self.edit_demis, funcionario.get("data_demissao"))):
            if valor:
                texto = str(valor)
                if "-" in texto:
                    ano, mes, dia = texto.split("-")
                    widget.setText(f"{dia}/{mes}/{ano}")
                else:
                    widget.setText(texto)
            else:
                widget.clear()

        sexo = funcionario.get("sexo") or ""
        indice_sexo = self.comb_sexo_func.findText(sexo)
        self.comb_sexo_func.setCurrentIndex(indice_sexo if indice_sexo >= 0 else 0)

        cargo = funcionario.get("cargo") or ""
        if cargo and self.comb_cargo_fun.findText(cargo) == -1:
            self.comb_cargo_fun.addItem(cargo)
        indice_cargo = self.comb_cargo_fun.findText(cargo)
        self.comb_cargo_fun.setCurrentIndex(indice_cargo if indice_cargo >= 0 else 0)

    def sair(self):
        from entidades.tela_ent import TelaEntidades
        self.janela = TelaEntidades()
        self.janela.show()
        self.close()

    def buscar_cep(self):
        cep = self.edit_cep_func.text()
        dados = consulta_cep(cep)

        if dados is None:
            QMessageBox.warning(self, "CEP invalido", "CEP nao encontrado ou mal formatado.")
        elif dados:
            self.edit_end_func.setText(dados.get('logradouro', '').upper())
            self.edit_bairro_func.setText(dados.get('bairro', '').upper())
            self.edit_cid_func.setText(dados.get('localidade', '').upper())
            self.edit_est_func.setText(dados.get('uf', '').upper())


    def ao_trocar_aba(self, index):
        if index == 1:
            self.edit_nome_func.setFocus()


    def alterar_status_funcionario(self):
        codigo = self.edit_cod.text().strip()
        if not codigo:
            QMessageBox.warning(self, "Aviso", "Nenhum funcionario selecionado.")
            return

        funcionario = self.service.buscar_por_codigo(codigo)
        if not funcionario:
            QMessageBox.warning(self, "Erro", "Funcionario nao encontrado.")
            return

        if funcionario.get("status") == "A":
            novo_status = "E"
            mensagem = "Deseja EXCLUIR este funcionario?"
            acao = "excluido"
        else:
            novo_status = "A"
            mensagem = "Deseja ATIVAR este funcionario?"
            acao = "ativado"

        msg = QMessageBox(self)
        msg.setWindowTitle("Confirmação")
        msg.setText(mensagem)

        btn_sim = msg.addButton("Sim", QMessageBox.ButtonRole.YesRole)
        btn_nao = msg.addButton("Não", QMessageBox.ButtonRole.NoRole)

        msg.setDefaultButton(btn_nao)
        msg.exec()

        if msg.clickedButton() != btn_sim:
            return

        resultado = self.service.alterar_status(codigo, novo_status)

        if resultado["sucesso"]:
            QMessageBox.information(self, "Sucesso", f"Funcionario {acao} com sucesso!")
            self.limpar_campos()
            self.tab.setCurrentIndex(0)
            self.acao_buscar_funcionario()
        else:
            QMessageBox.warning(self, "Erro", resultado["mensagem"])



    def novo_funcionario(self):
        self.limpar_campos()
        self.tab.setCurrentIndex(1)
        self.edit_nome_func.setFocus()

    def cancelar(self):
        self.limpar_campos()
        self.tab.setCurrentIndex(0)

    def abrir_dialog_senha(self):
        codigo = self.edit_cod.text().strip()

        if not codigo:
            QMessageBox.warning(
                self,
                "Aviso",
                "Usuário deve ser SALVO."
            )
            return

        dialog = DialogSenhaFuncionario(codigo)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = CadFuncionarios()
    janela.show()
    sys.exit(app.exec())
