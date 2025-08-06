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
        nometela = QLabel("Cadastro Fornecedores")
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
        layout_geral_aba1.addLayout(hbox_linha1)
        layout_geral_aba1.addLayout(vbox_linha2)
        layout_geral_aba1.addWidget(self.tabela_resultado)
        layout_geral_aba1.addStretch()
        layout_geral_aba1.addLayout(hbox_botoes_rodape)
        layout_geral_aba1.addStretch()

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

        edit_cod_for = criar_lineedit_padrao()
        edit_cod_for.setFixedWidth(90)

        vbox_cod_for = QVBoxLayout()
        vbox_cod_for.addWidget(cod_for)
        vbox_cod_for.addWidget(edit_cod_for)

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
        hbox_label_raz_social.addStretch()
        hbox_label_raz_social.addLayout(hbox_check)
        hbox_label_raz_social.setContentsMargins(0, 0, 17, 0)

        self.edit_raz_social = criar_lineedit_padrao(LineEditComEnter)
        self.edit_raz_social.setFixedWidth (435)
        self.edit_raz_social.setFocus()

        vbox_raz_social = QVBoxLayout()
        vbox_raz_social.addLayout(hbox_label_raz_social)
        vbox_raz_social.addWidget(self.edit_raz_social)

        # Nome fantasia 
        fant_forn = criar_label_padrao()
        fant_forn.setText('Nome Fantasia/Apelido')
        fant_forn.setContentsMargins(2, 0, 0, 0)
        fant_forn.setFixedSize(fant_forn.sizeHint())

        self.edit_fant_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_fant_forn.setFixedWidth(400)

        vbox_fant_forn = QVBoxLayout()
        vbox_fant_forn.addWidget(fant_forn, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_fant_forn.addWidget(self.edit_fant_forn)

        #contato 

        cont_forn = criar_label_padrao()
        cont_forn.setText('Contato')
        cont_forn.setContentsMargins(2, 0, 0, 0)
        cont_forn.setFixedSize(fant_forn.sizeHint())

        self.edit_cont_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cont_forn.setFixedWidth(180)

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
        self.edit_end_forn.setFixedWidth(350)

        vbox_end_forn = QVBoxLayout()
        vbox_end_forn.addWidget(end_forn)
        vbox_end_forn.addWidget(self.edit_end_forn)

        #bairro funcionário
        bairro_forn = criar_label_padrao()
        bairro_forn.setText('Bairro')
        bairro_forn.setContentsMargins(2, 0, 0, 0)
        bairro_forn.setFixedSize(bairro_forn.sizeHint())

        self.edit_bairro_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bairro_forn.setFixedWidth(205)

        vbox_bairro_forn = QVBoxLayout()
        vbox_bairro_forn.addWidget(bairro_forn)
        vbox_bairro_forn.addWidget(self.edit_bairro_forn)

        #cidade fornecedor
        cid_forn = criar_label_padrao()
        cid_forn.setText('Cidade')
        cid_forn.setContentsMargins(2, 0, 0, 0)
        cid_forn.setFixedSize(cid_forn.sizeHint())

        self.edit_cid_forn = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cid_forn.setFixedWidth(220)

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

        #layout linha 3
        forn_linha3 = QHBoxLayout()
        forn_linha3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        forn_linha3.addLayout(vbox_tel_forn)
        forn_linha3.addLayout(vbox_cnpj_forn)
        forn_linha3.addLayout(vbox_insc_forn)
        forn_linha3.addLayout(vbox_insc_mun_forn)

        # linha 3 --- fim ---

        # linha 4 --- início ---

        inf_add_forn = criar_label_padrao()
        inf_add_forn.setText('Informações adicionais')
        inf_add_forn.setContentsMargins(2, 0, 0, 0)
        inf_add_forn.setFixedSize(inf_add_forn.sizeHint())

        text_inf_add_forn = QTextEdit()
        text_inf_add_forn.setFixedSize(875, 70)
        text_inf_add_forn.setStyleSheet('background-color: white; font-size: 14px')

        vbox_inf_add_forn = QVBoxLayout()
        vbox_inf_add_forn.addWidget(inf_add_forn)
        vbox_inf_add_forn.addWidget(text_inf_add_forn)
 
        forn_linha4 = QHBoxLayout()
        forn_linha4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        forn_linha4.addLayout(vbox_inf_add_forn)
        
        # linha 4 --- fim ---

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

        # layout geral aba 2
        layout_geral_aba2 = QVBoxLayout()
        layout_geral_aba2.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba2.addLayout(forn_linha1)
        layout_geral_aba2.addLayout(forn_linha2)
        layout_geral_aba2.addLayout(forn_linha3)
        layout_geral_aba2.addLayout(forn_linha4)
        layout_geral_aba2.addStretch()
        layout_geral_aba2.addLayout(hbox_botoes_aba2)
        layout_geral_aba2.addSpacing(30)


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
        vbox.setContentsMargins(110, 50, 110, 50)

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

        elif self.check_fis.isChecked():
            self.cnpj_forn.setText('CPF')
            self.cnpj_forn.setContentsMargins(2, 0, 0, 0)
            self.cnpj_forn.setFixedSize(self.cnpj_forn.sizeHint())
            self.edit_cnpj_forn.setInputMask('000.000.000-00;_')
            self.insc_forn.setText('RG')
            self.insc_forn.setContentsMargins(2, 0, 0, 0)
            self.insc_forn.setFixedSize(self.insc_forn.sizeHint())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = CadFornecedor()
    janela.show()
    sys.exit(app.exec())
