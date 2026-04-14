import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from entidades.cliente.cliente_service import ClienteService
from util.estilo import gerar_estilo
from util.fun_basicas import LineEditComEnter, consulta_cep
from util.padrao import (
    criar_botao,
    criar_botao_sair,
    criar_botao_salvar,
    criar_combobox_padrao,
    criar_label_padrao,
    criar_lineedit_padrao,
    criar_tab_widget,
)


class CadCliente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro Clientes")
        self.service = ClienteService()
        self.status_atual = "A"

        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "imagens", "icone.png")
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"[ERRO] Icone nao encontrado: {icon_path}")

        self.componentes()
        self.showMaximized()

        QShortcut(QKeySequence("Esc"), self).activated.connect(self.sair)
        QShortcut(QKeySequence("F8"), self).activated.connect(self.acao_buscar_cliente)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.novo_cliente)

    def componentes(self):
        nometela = QLabel("Cadastro de Clientes")
        nometela.setStyleSheet("color: orange; font-size:38px; font: bold")

        self.tab = criar_tab_widget()
        self.tab.currentChanged.connect(self.ao_trocar_aba)

        # ----------- ABA 1 (Consulta) ------------
        aba1 = QWidget()
        aba1.setStyleSheet('background-color: #cbcdce;')

        label_opc = criar_label_padrao()
        label_opc.setText('Opções')
        label_opc.setContentsMargins(2, 0, 0, 0)
        label_opc.setFixedSize(label_opc.sizeHint())

        opcoes_consulta = ['Código', 'Nome / Razão Social', 'CPF / CNPJ', 'WhatsApp', 'Email']
        self.comb_opc = criar_combobox_padrao()
        self.comb_opc.addItems(opcoes_consulta)
        self.comb_opc.setCurrentText("Nome / Razão Social")
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

        self.edit_label_pesq = criar_lineedit_padrao()
        self.edit_label_pesq.setMinimumWidth(810)
        self.edit_label_pesq.textChanged.connect(self.acao_buscar_cliente)

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
        label_ativo.setText('Status')
        label_ativo.setContentsMargins(2, 0, 0, 0)
        label_ativo.setFixedSize(label_ativo.sizeHint())

        self.combo_ativo = criar_combobox_padrao()
        self.combo_ativo.addItems(["Ativos", "Excluídos", "Todos"])
        self.combo_ativo.setFixedWidth(220)

        self.btn_pesq = criar_botao()
        self.btn_pesq.setText("F8 - Pesquisa")
        self.btn_pesq.clicked.connect(self.acao_buscar_cliente)

        hbox_linha2 = QHBoxLayout()
        hbox_linha2.addWidget(self.combo_ativo, alignment=Qt.AlignmentFlag.AlignLeft)
        hbox_linha2.addWidget(self.btn_pesq)

        vbox_linha2 = QVBoxLayout()
        vbox_linha2.addWidget(label_ativo, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_linha2.addLayout(hbox_linha2)

        self.tabela_resultado = QTableWidget()
        self.tabela_resultado.setColumnCount(6)
        self.tabela_resultado.setHorizontalHeaderLabels([
            "Código",
            "Nome / Razão Social",
            "CPF / CNPJ",
            "WhatsApp",
            "E-mail",
            "Status"
        ])
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
        self.tabela_resultado.verticalHeader().setVisible(False)
        self.tabela_resultado.itemDoubleClicked.connect(self.abrir_cliente_selecionado)

        self.tabela_resultado.setColumnWidth(0, 70)
        self.tabela_resultado.setColumnWidth(1, 360)
        self.tabela_resultado.setColumnWidth(2, 170)
        self.tabela_resultado.setColumnWidth(3, 140)
        self.tabela_resultado.setColumnWidth(4, 220)
        self.tabela_resultado.setColumnWidth(5, 100)

        self.botao_novo = criar_botao()
        self.botao_novo.setText('F5 - Novo')
        self.botao_novo.clicked.connect(self.novo_cliente)

        self.botao_relat = criar_botao()
        self.botao_relat.setText('Relatórios')

        hbox_botoes_rodape = QHBoxLayout()
        hbox_botoes_rodape.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        self.table_cliente = criar_tab_widget()

        # ----------- SUBABA DADOS ------------
        aba_dados = QWidget()

        # linha 1
        cod_cli = criar_label_padrao()
        cod_cli.setText('Código')
        cod_cli.setContentsMargins(2, 0, 0, 0)
        cod_cli.setFixedSize(cod_cli.sizeHint())

        self.edit_cod_cli = criar_lineedit_padrao()
        self.edit_cod_cli.setFixedWidth(90)
        self.edit_cod_cli.setReadOnly(True)

        vbox_cod_cli = QVBoxLayout()
        vbox_cod_cli.addWidget(cod_cli)
        vbox_cod_cli.addWidget(self.edit_cod_cli)

        raz_social = criar_label_padrao()
        raz_social.setText('Razão Social/Nome')
        raz_social.setContentsMargins(2, 0, 0, 0)
        raz_social.setFixedSize(raz_social.sizeHint())

        self.check_jur = QCheckBox('Jurídica')
        self.check_jur.stateChanged.connect(self.atualiza_form)

        self.check_fis = QCheckBox('Física')
        self.check_fis.stateChanged.connect(self.atualiza_form)

        self.grupo_tipo_pessoa = QButtonGroup(self)
        self.grupo_tipo_pessoa.setExclusive(True)
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

        fant_cli = criar_label_padrao()
        fant_cli.setText('Nome Fantasia/Apelido')
        fant_cli.setContentsMargins(2, 0, 0, 0)
        fant_cli.setFixedSize(fant_cli.sizeHint())

        self.edit_fant_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_fant_cli.setMinimumWidth(390)

        vbox_fant_cli = QVBoxLayout()
        vbox_fant_cli.addWidget(fant_cli)
        vbox_fant_cli.addWidget(self.edit_fant_cli)

        cont_cli = criar_label_padrao()
        cont_cli.setText('Nome Contato')
        cont_cli.setContentsMargins(2, 0, 0, 0)
        cont_cli.setFixedSize(cont_cli.sizeHint())

        self.edit_cont_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cont_cli.setMinimumWidth(180)

        vbox_cont_cli = QVBoxLayout()
        vbox_cont_cli.addWidget(cont_cli)
        vbox_cont_cli.addWidget(self.edit_cont_cli)

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

        dados_cli_linha1 = QHBoxLayout()
        dados_cli_linha1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dados_cli_linha1.addLayout(vbox_cod_cli)
        dados_cli_linha1.addLayout(vbox_raz_social)
        dados_cli_linha1.addLayout(vbox_fant_cli)
        dados_cli_linha1.addLayout(vbox_cont_cli)
        dados_cli_linha1.addLayout(vbox_zap_cli)

        # linha 2
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

        end_cli = criar_label_padrao()
        end_cli.setText('Endereço')
        end_cli.setContentsMargins(2, 0, 0, 0)
        end_cli.setFixedSize(end_cli.sizeHint())

        self.edit_end_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_end_cli.setMinimumWidth(250)

        vbox_end_cli = QVBoxLayout()
        vbox_end_cli.addWidget(end_cli)
        vbox_end_cli.addWidget(self.edit_end_cli)

        num_cli = criar_label_padrao()
        num_cli.setText('Número')
        num_cli.setContentsMargins(2, 0, 0, 0)
        num_cli.setFixedSize(num_cli.sizeHint())

        self.edit_num_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_num_cli.setFixedWidth(80)

        vbox_num_cli = QVBoxLayout()
        vbox_num_cli.addWidget(num_cli)
        vbox_num_cli.addWidget(self.edit_num_cli)

        bairro_cli = criar_label_padrao()
        bairro_cli.setText('Bairro')
        bairro_cli.setContentsMargins(2, 0, 0, 0)
        bairro_cli.setFixedSize(bairro_cli.sizeHint())

        self.edit_bairro_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bairro_cli.setMinimumWidth(205)

        vbox_bairro_cli = QVBoxLayout()
        vbox_bairro_cli.addWidget(bairro_cli)
        vbox_bairro_cli.addWidget(self.edit_bairro_cli)

        cid_cli = criar_label_padrao()
        cid_cli.setText('Cidade')
        cid_cli.setContentsMargins(2, 0, 0, 0)
        cid_cli.setFixedSize(cid_cli.sizeHint())

        self.edit_cid_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cid_cli.setMinimumWidth(220)

        vbox_cid_cli = QVBoxLayout()
        vbox_cid_cli.addWidget(cid_cli)
        vbox_cid_cli.addWidget(self.edit_cid_cli)

        est_cli = criar_label_padrao()
        est_cli.setText('UF')
        est_cli.setContentsMargins(2, 0, 0, 0)
        est_cli.setFixedSize(est_cli.sizeHint())

        self.edit_est_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_est_cli.setFixedWidth(60)

        vbox_est_cli = QVBoxLayout()
        vbox_est_cli.addWidget(est_cli)
        vbox_est_cli.addWidget(self.edit_est_cli)

        email_cli = criar_label_padrao()
        email_cli.setText('E-mail')
        email_cli.setContentsMargins(2, 0, 0, 0)
        email_cli.setFixedSize(email_cli.sizeHint())

        self.edit_email_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_email_cli.setFixedWidth(310)

        vbox_email_cli = QVBoxLayout()
        vbox_email_cli.addWidget(email_cli)
        vbox_email_cli.addWidget(self.edit_email_cli)

        dados_cli_linha2 = QHBoxLayout()
        dados_cli_linha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dados_cli_linha2.addLayout(vbox_cep_cli)
        dados_cli_linha2.addLayout(vbox_end_cli)
        dados_cli_linha2.addLayout(vbox_num_cli)
        dados_cli_linha2.addLayout(vbox_bairro_cli)
        dados_cli_linha2.addLayout(vbox_cid_cli)
        dados_cli_linha2.addLayout(vbox_est_cli)
        dados_cli_linha2.addLayout(vbox_email_cli)

        # linha 3
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

        self.cnpj_cli = criar_label_padrao()

        self.edit_cnpj_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cnpj_cli.setFixedWidth(150)
        self.edit_cnpj_cli.editingFinished.connect(self.validar_documento)

        vbox_cnpj_cli = QVBoxLayout()
        vbox_cnpj_cli.addWidget(self.cnpj_cli)
        vbox_cnpj_cli.addWidget(self.edit_cnpj_cli)

        self.insc_cli = criar_label_padrao()

        self.edit_insc_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_insc_cli.setFixedWidth(150)

        vbox_insc_cli = QVBoxLayout()
        vbox_insc_cli.addWidget(self.insc_cli)
        vbox_insc_cli.addWidget(self.edit_insc_cli)

        insc_mun_cli = criar_label_padrao()
        insc_mun_cli.setText('Insc. Municipal')
        insc_mun_cli.setContentsMargins(2, 0, 0, 0)
        insc_mun_cli.setFixedSize(insc_mun_cli.sizeHint())

        self.edit_insc_mun_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_insc_mun_cli.setFixedWidth(150)

        vbox_insc_mun_cli = QVBoxLayout()
        vbox_insc_mun_cli.addWidget(insc_mun_cli)
        vbox_insc_mun_cli.addWidget(self.edit_insc_mun_cli)

        self.dt_nasc_cli = criar_label_padrao()

        self.edit_dt_nasc_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_dt_nasc_cli.setFixedWidth(100)
        self.edit_dt_nasc_cli.setInputMask('00/00/0000;_')

        vbox_dt_nasc_cli = QVBoxLayout()
        vbox_dt_nasc_cli.addWidget(self.dt_nasc_cli)
        vbox_dt_nasc_cli.addWidget(self.edit_dt_nasc_cli)

        sexo_cli = criar_label_padrao()
        sexo_cli.setText('Sexo')
        sexo_cli.setContentsMargins(2, 0, 0, 0)
        sexo_cli.setFixedSize(sexo_cli.sizeHint())

        self.comb_sexo_cli = criar_combobox_padrao()
        self.comb_sexo_cli.setFixedWidth(100)
        self.comb_sexo_cli.addItem('Selecione')
        self.comb_sexo_cli.addItem('Masculino')
        self.comb_sexo_cli.addItem('Feminino')
        self.comb_sexo_cli.model().item(0).setEnabled(False)

        vbox_sexo_cli = QVBoxLayout()
        vbox_sexo_cli.addWidget(sexo_cli)
        vbox_sexo_cli.addWidget(self.comb_sexo_cli)

        nacion_cli = criar_label_padrao()
        nacion_cli.setText('Cidade Nascimento')
        nacion_cli.setContentsMargins(2, 0, 0, 0)
        nacion_cli.setFixedSize(nacion_cli.sizeHint())

        self.edit_nacion_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nacion_cli.setMinimumWidth(215)

        vbox_nacion_cli = QVBoxLayout()
        vbox_nacion_cli.addWidget(nacion_cli)
        vbox_nacion_cli.addWidget(self.edit_nacion_cli)

        natur_cli = criar_label_padrao()
        natur_cli.setText('País Nascimento')
        natur_cli.setContentsMargins(2, 0, 0, 0)
        natur_cli.setFixedSize(natur_cli.sizeHint())

        self.edit_natur_cli = criar_lineedit_padrao(LineEditComEnter)
        self.edit_natur_cli.setMinimumWidth(212)

        vbox_natur_cli = QVBoxLayout()
        vbox_natur_cli.addWidget(natur_cli)
        vbox_natur_cli.addWidget(self.edit_natur_cli)

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

        # linha 4
        nome_mae = criar_label_padrao()
        nome_mae.setText('Nome Mãe')
        nome_mae.setContentsMargins(2, 0, 0, 0)
        nome_mae.setFixedSize(nome_mae.sizeHint())

        self.edit_nome_mae = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_mae.setFixedWidth(270)

        vbox_nome_mae = QVBoxLayout()
        vbox_nome_mae.addWidget(nome_mae)
        vbox_nome_mae.addWidget(self.edit_nome_mae)

        nome_pai = criar_label_padrao()
        nome_pai.setText('Nome Pai')
        nome_pai.setContentsMargins(2, 0, 0, 0)
        nome_pai.setFixedSize(nome_pai.sizeHint())

        self.edit_nome_pai = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_pai.setFixedWidth(270)

        vbox_nome_pai = QVBoxLayout()
        vbox_nome_pai.addWidget(nome_pai)
        vbox_nome_pai.addWidget(self.edit_nome_pai)

        dados_cli_linha4 = QHBoxLayout()
        dados_cli_linha4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dados_cli_linha4.addLayout(vbox_nome_mae)
        dados_cli_linha4.addLayout(vbox_nome_pai)

        # linha 5
        inf_add_cli = criar_label_padrao()
        inf_add_cli.setText('Informações adicionais')
        inf_add_cli.setContentsMargins(2, 0, 0, 0)
        inf_add_cli.setFixedSize(inf_add_cli.sizeHint())

        self.text_inf_add_cli = QTextEdit()
        self.text_inf_add_cli.setMinimumWidth(875)
        self.text_inf_add_cli.setMinimumHeight(70)
        self.text_inf_add_cli.setStyleSheet('background-color: white; font-size: 14px')

        vbox_inf_add_cli = QVBoxLayout()
        vbox_inf_add_cli.addWidget(inf_add_cli)
        vbox_inf_add_cli.addWidget(self.text_inf_add_cli)

        dados_cli_linha5 = QHBoxLayout()
        dados_cli_linha5.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dados_cli_linha5.addLayout(vbox_inf_add_cli)

        self.botao_novo_cli = criar_botao()
        self.botao_novo_cli.setText('F5 - Novo')
        self.botao_novo_cli.clicked.connect(self.novo_cliente)

        self.botao_canc_cli = criar_botao()
        self.botao_canc_cli.setText('Cancelar')
        self.botao_canc_cli.clicked.connect(self.cancelar)

        self.botao_excl_cli = criar_botao()
        self.botao_excl_cli.setText('Excluir / Ativar')
        self.botao_excl_cli.clicked.connect(self.alterar_status_cliente)

        hbox_botoes_dados = QHBoxLayout()
        hbox_botoes_dados.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox_botoes_dados.addWidget(self.botao_novo_cli)
        hbox_botoes_dados.addSpacing(5)
        hbox_botoes_dados.addWidget(self.botao_canc_cli)
        hbox_botoes_dados.addSpacing(5)
        hbox_botoes_dados.addWidget(self.botao_excl_cli)
        hbox_botoes_dados.addStretch()

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

        aba_dados.setLayout(vbox_geral_aba_dados)

        # ----------- SUBABA REFERÊNCIAS ------------
        aba_ref = QWidget()

        # dados profissionais
        dad_prof = criar_label_padrao()
        dad_prof.setText('Dados Profissionais')
        dad_prof.setStyleSheet('font: bold;')
        dad_prof.setContentsMargins(2, 0, 0, 0)
        dad_prof.setFixedSize(dad_prof.sizeHint())

        vbox_dad_prof = QVBoxLayout()
        vbox_dad_prof.addWidget(dad_prof, alignment=Qt.AlignmentFlag.AlignLeft)

        hbox_ref_linha1 = QHBoxLayout()
        hbox_ref_linha1.addLayout(vbox_dad_prof)

        loc_trab = criar_label_padrao()
        loc_trab.setText('Local Trabalho')
        loc_trab.setContentsMargins(2, 0, 0, 0)
        loc_trab.setFixedSize(loc_trab.sizeHint())

        self.edit_loc_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_loc_trab.setMinimumWidth(180)

        vbox_loc_trab = QVBoxLayout()
        vbox_loc_trab.addWidget(loc_trab)
        vbox_loc_trab.addWidget(self.edit_loc_trab)

        carg_trab = criar_label_padrao()
        carg_trab.setText('Cargo')
        carg_trab.setContentsMargins(2, 0, 0, 0)
        carg_trab.setFixedSize(carg_trab.sizeHint())

        self.edit_carg_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_carg_trab.setMinimumWidth(180)

        vbox_carg_trab = QVBoxLayout()
        vbox_carg_trab.addWidget(carg_trab)
        vbox_carg_trab.addWidget(self.edit_carg_trab)

        temp_serv = criar_label_padrao()
        temp_serv.setText('Tempo Serv.')
        temp_serv.setContentsMargins(2, 0, 0, 0)
        temp_serv.setFixedSize(temp_serv.sizeHint())

        self.edit_temp_serv = criar_lineedit_padrao(LineEditComEnter)
        self.edit_temp_serv.setFixedWidth(160)

        vbox_temp_serv = QVBoxLayout()
        vbox_temp_serv.addWidget(temp_serv)
        vbox_temp_serv.addWidget(self.edit_temp_serv)

        salario = criar_label_padrao()
        salario.setText('Salário')
        salario.setContentsMargins(2, 0, 0, 0)
        salario.setFixedSize(salario.sizeHint())

        self.edit_salario = criar_lineedit_padrao(LineEditComEnter)
        self.edit_salario.setFixedWidth(100)

        vbox_salario = QVBoxLayout()
        vbox_salario.addWidget(salario)
        vbox_salario.addWidget(self.edit_salario)

        tel_trab = criar_label_padrao()
        tel_trab.setText('Telefone')
        tel_trab.setContentsMargins(2, 0, 0, 0)
        tel_trab.setFixedSize(tel_trab.sizeHint())

        self.edit_tel_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_trab.setFixedWidth(130)
        self.edit_tel_trab.setInputMask('(00)00000-0000;_')

        vbox_tel_trab = QVBoxLayout()
        vbox_tel_trab.addWidget(tel_trab)
        vbox_tel_trab.addWidget(self.edit_tel_trab)

        hbox_ref_linha2 = QHBoxLayout()
        hbox_ref_linha2.addLayout(vbox_loc_trab)
        hbox_ref_linha2.addLayout(vbox_carg_trab)
        hbox_ref_linha2.addLayout(vbox_temp_serv)
        hbox_ref_linha2.addLayout(vbox_salario)
        hbox_ref_linha2.addLayout(vbox_tel_trab)

        # endereço trabalho
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

        end_trab = criar_label_padrao()
        end_trab.setText('Endereço')
        end_trab.setContentsMargins(2, 0, 0, 0)
        end_trab.setFixedSize(end_trab.sizeHint())

        self.edit_end_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_end_trab.setMinimumWidth(335)

        vbox_end_trab = QVBoxLayout()
        vbox_end_trab.addWidget(end_trab)
        vbox_end_trab.addWidget(self.edit_end_trab)

        num_trab = criar_label_padrao()
        num_trab.setText('Número')
        num_trab.setContentsMargins(2, 0, 0, 0)
        num_trab.setFixedSize(num_trab.sizeHint())

        self.edit_num_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_num_trab.setFixedWidth(80)

        vbox_num_trab = QVBoxLayout()
        vbox_num_trab.addWidget(num_trab)
        vbox_num_trab.addWidget(self.edit_num_trab)

        bairro_trab = criar_label_padrao()
        bairro_trab.setText('Bairro')
        bairro_trab.setContentsMargins(2, 0, 0, 0)
        bairro_trab.setFixedSize(bairro_trab.sizeHint())

        self.edit_bairro_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bairro_trab.setMinimumWidth(205)

        vbox_bairro_trab = QVBoxLayout()
        vbox_bairro_trab.addWidget(bairro_trab)
        vbox_bairro_trab.addWidget(self.edit_bairro_trab)

        cid_trab = criar_label_padrao()
        cid_trab.setText('Cidade')
        cid_trab.setContentsMargins(2, 0, 0, 0)
        cid_trab.setFixedSize(cid_trab.sizeHint())

        self.edit_cid_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cid_trab.setMinimumWidth(220)

        vbox_cid_trab = QVBoxLayout()
        vbox_cid_trab.addWidget(cid_trab)
        vbox_cid_trab.addWidget(self.edit_cid_trab)

        est_trab = criar_label_padrao()
        est_trab.setText('UF')
        est_trab.setContentsMargins(2, 0, 0, 0)
        est_trab.setFixedSize(est_trab.sizeHint())

        self.edit_est_trab = criar_lineedit_padrao(LineEditComEnter)
        self.edit_est_trab.setFixedWidth(60)

        vbox_est_trab = QVBoxLayout()
        vbox_est_trab.addWidget(est_trab)
        vbox_est_trab.addWidget(self.edit_est_trab)

        hbox_ref_linha3 = QHBoxLayout()
        hbox_ref_linha3.addLayout(vbox_cep_trab)
        hbox_ref_linha3.addLayout(vbox_end_trab)
        hbox_ref_linha3.addLayout(vbox_num_trab)
        hbox_ref_linha3.addLayout(vbox_bairro_trab)
        hbox_ref_linha3.addLayout(vbox_cid_trab)
        hbox_ref_linha3.addLayout(vbox_est_trab)

        # referências pessoais
        ref_pessoais = criar_label_padrao()
        ref_pessoais.setText('Referências Pessoais')
        ref_pessoais.setStyleSheet('font: bold;')
        ref_pessoais.setContentsMargins(2, 0, 0, 0)
        ref_pessoais.setFixedSize(ref_pessoais.sizeHint())

        vbox_ref_pess = QVBoxLayout()
        vbox_ref_pess.addWidget(ref_pessoais, alignment=Qt.AlignmentFlag.AlignLeft)

        nome_ref_pess = criar_label_padrao()
        nome_ref_pess.setText('Nome')
        nome_ref_pess.setContentsMargins(2, 0, 0, 0)
        nome_ref_pess.setFixedSize(nome_ref_pess.sizeHint())

        self.edit_nome_ref_pess1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_ref_pess1.setFixedWidth(350)
        self.edit_nome_ref_pess2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_ref_pess2.setFixedWidth(350)
        self.edit_nome_ref_pess3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_nome_ref_pess3.setFixedWidth(350)

        tel_ref_pess = criar_label_padrao()
        tel_ref_pess.setText('Telefone')
        tel_ref_pess.setContentsMargins(2, 0, 0, 0)
        tel_ref_pess.setFixedSize(tel_ref_pess.sizeHint())

        self.edit_tel_ref_pess1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_ref_pess1.setFixedWidth(130)
        self.edit_tel_ref_pess1.setInputMask('(00)00000-0000;_')
        self.edit_tel_ref_pess2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_ref_pess2.setFixedWidth(130)
        self.edit_tel_ref_pess2.setInputMask('(00)00000-0000;_')
        self.edit_tel_ref_pess3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_ref_pess3.setFixedWidth(130)
        self.edit_tel_ref_pess3.setInputMask('(00)00000-0000;_')

        inf_ref_pess = criar_label_padrao()
        inf_ref_pess.setText('Informação')
        inf_ref_pess.setContentsMargins(2, 0, 0, 0)
        inf_ref_pess.setFixedSize(inf_ref_pess.sizeHint())

        self.edit_inf_pess1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_inf_pess1.setMinimumWidth(550)
        self.edit_inf_pess2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_inf_pess2.setMinimumWidth(550)
        self.edit_inf_pess3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_inf_pess3.setMinimumWidth(550)

        vbox_nome_ref_pess = QVBoxLayout()
        vbox_nome_ref_pess.addWidget(nome_ref_pess)
        vbox_nome_ref_pess.addWidget(self.edit_nome_ref_pess1)

        vbox_tel_ref_pess = QVBoxLayout()
        vbox_tel_ref_pess.addWidget(tel_ref_pess)
        vbox_tel_ref_pess.addWidget(self.edit_tel_ref_pess1)

        vbox_inf_ref_pess = QVBoxLayout()
        vbox_inf_ref_pess.addWidget(inf_ref_pess)
        vbox_inf_ref_pess.addWidget(self.edit_inf_pess1)

        hbox_ref_pess_linha1 = QHBoxLayout()
        hbox_ref_pess_linha1.addLayout(vbox_nome_ref_pess)
        hbox_ref_pess_linha1.addLayout(vbox_tel_ref_pess)
        hbox_ref_pess_linha1.addLayout(vbox_inf_ref_pess)

        hbox_ref_pess_linha2 = QHBoxLayout()
        hbox_ref_pess_linha2.addWidget(self.edit_nome_ref_pess2)
        hbox_ref_pess_linha2.addWidget(self.edit_tel_ref_pess2)
        hbox_ref_pess_linha2.addWidget(self.edit_inf_pess2)

        hbox_ref_pess_linha3 = QHBoxLayout()
        hbox_ref_pess_linha3.addWidget(self.edit_nome_ref_pess3)
        hbox_ref_pess_linha3.addWidget(self.edit_tel_ref_pess3)
        hbox_ref_pess_linha3.addWidget(self.edit_inf_pess3)

        # referências comerciais
        ref_comerc = criar_label_padrao()
        ref_comerc.setText('Referências Comerciais')
        ref_comerc.setStyleSheet('font: bold;')
        ref_comerc.setContentsMargins(2, 0, 0, 0)
        ref_comerc.setFixedSize(ref_comerc.sizeHint())

        vbox_ref_comerc = QVBoxLayout()
        vbox_ref_comerc.addWidget(ref_comerc, alignment=Qt.AlignmentFlag.AlignLeft)

        loja_ref_comerc = criar_label_padrao()
        loja_ref_comerc.setText('Loja')
        loja_ref_comerc.setContentsMargins(2, 0, 0, 0)
        loja_ref_comerc.setFixedSize(loja_ref_comerc.sizeHint())

        self.edit_loja_ref_comerc1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_loja_ref_comerc1.setFixedWidth(350)
        self.edit_loja_ref_comerc2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_loja_ref_comerc2.setFixedWidth(350)
        self.edit_loja_ref_comerc3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_loja_ref_comerc3.setFixedWidth(350)

        tel_ref_comerc = criar_label_padrao()
        tel_ref_comerc.setText('Telefone')
        tel_ref_comerc.setContentsMargins(2, 0, 0, 0)
        tel_ref_comerc.setFixedSize(tel_ref_comerc.sizeHint())

        self.edit_tel_ref_comerc1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_ref_comerc1.setFixedWidth(130)
        self.edit_tel_ref_comerc1.setInputMask('(00)00000-0000;_')
        self.edit_tel_ref_comerc2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_ref_comerc2.setFixedWidth(130)
        self.edit_tel_ref_comerc2.setInputMask('(00)00000-0000;_')
        self.edit_tel_ref_comerc3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_tel_ref_comerc3.setFixedWidth(130)
        self.edit_tel_ref_comerc3.setInputMask('(00)00000-0000;_')

        inic_comp_comerc = criar_label_padrao()
        inic_comp_comerc.setText('Cliente desde')
        inic_comp_comerc.setContentsMargins(2, 0, 0, 0)
        inic_comp_comerc.setFixedSize(inic_comp_comerc.sizeHint())

        self.edit_inic_comp_comerc1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_inic_comp_comerc1.setFixedWidth(100)
        self.edit_inic_comp_comerc1.setInputMask('00/00/0000;_')
        self.edit_inic_comp_comerc2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_inic_comp_comerc2.setFixedWidth(100)
        self.edit_inic_comp_comerc2.setInputMask('00/00/0000;_')
        self.edit_inic_comp_comerc3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_inic_comp_comerc3.setFixedWidth(100)
        self.edit_inic_comp_comerc3.setInputMask('00/00/0000;_')

        val_ult_comp = criar_label_padrao()
        val_ult_comp.setText('V. ult. comp.')
        val_ult_comp.setContentsMargins(2, 0, 0, 0)
        val_ult_comp.setFixedSize(val_ult_comp.sizeHint())

        self.edit_val_ult_comp1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_val_ult_comp1.setFixedWidth(110)
        self.edit_val_ult_comp2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_val_ult_comp2.setFixedWidth(110)
        self.edit_val_ult_comp3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_val_ult_comp3.setFixedWidth(110)

        data_ult_comp = criar_label_padrao()
        data_ult_comp.setText('D. ult. comp.')
        data_ult_comp.setContentsMargins(2, 0, 0, 0)
        data_ult_comp.setFixedSize(data_ult_comp.sizeHint())

        self.edit_data_ult_comp1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_data_ult_comp1.setFixedWidth(100)
        self.edit_data_ult_comp1.setInputMask('00/00/0000;_')
        self.edit_data_ult_comp2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_data_ult_comp2.setFixedWidth(100)
        self.edit_data_ult_comp2.setInputMask('00/00/0000;_')
        self.edit_data_ult_comp3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_data_ult_comp3.setFixedWidth(100)
        self.edit_data_ult_comp3.setInputMask('00/00/0000;_')

        val_maior_comp = criar_label_padrao()
        val_maior_comp.setText('V. maior comp.')
        val_maior_comp.setContentsMargins(2, 0, 0, 0)
        val_maior_comp.setFixedSize(val_maior_comp.sizeHint())

        self.edit_val_maior_comp1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_val_maior_comp1.setFixedWidth(110)
        self.edit_val_maior_comp2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_val_maior_comp2.setFixedWidth(110)
        self.edit_val_maior_comp3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_val_maior_comp3.setFixedWidth(110)

        data_maior_comp = criar_label_padrao()
        data_maior_comp.setText('D. maior comp.')
        data_maior_comp.setContentsMargins(2, 0, 0, 0)
        data_maior_comp.setFixedSize(data_maior_comp.sizeHint())

        self.edit_data_maior_comp1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_data_maior_comp1.setFixedWidth(100)
        self.edit_data_maior_comp1.setInputMask('00/00/0000;_')
        self.edit_data_maior_comp2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_data_maior_comp2.setFixedWidth(100)
        self.edit_data_maior_comp2.setInputMask('00/00/0000;_')
        self.edit_data_maior_comp3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_data_maior_comp3.setFixedWidth(100)
        self.edit_data_maior_comp3.setInputMask('00/00/0000;_')

        inf_comercial = criar_label_padrao()
        inf_comercial.setText('Informação')
        inf_comercial.setContentsMargins(2, 0, 0, 0)
        inf_comercial.setFixedSize(inf_comercial.sizeHint())

        self.edit_inf_comercial1 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_inf_comercial1.setMinimumWidth(200)
        self.edit_inf_comercial2 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_inf_comercial2.setMinimumWidth(200)
        self.edit_inf_comercial3 = criar_lineedit_padrao(LineEditComEnter)
        self.edit_inf_comercial3.setMinimumWidth(200)

        vbox_loja_ref_comerc = QVBoxLayout()
        vbox_loja_ref_comerc.addWidget(loja_ref_comerc)
        vbox_loja_ref_comerc.addWidget(self.edit_loja_ref_comerc1)

        vbox_tel_ref_comerc = QVBoxLayout()
        vbox_tel_ref_comerc.addWidget(tel_ref_comerc)
        vbox_tel_ref_comerc.addWidget(self.edit_tel_ref_comerc1)

        vbox_inic_comp_comerc = QVBoxLayout()
        vbox_inic_comp_comerc.addWidget(inic_comp_comerc)
        vbox_inic_comp_comerc.addWidget(self.edit_inic_comp_comerc1)

        vbox_val_ult_comp = QVBoxLayout()
        vbox_val_ult_comp.addWidget(val_ult_comp)
        vbox_val_ult_comp.addWidget(self.edit_val_ult_comp1)

        vbox_data_ult_comp = QVBoxLayout()
        vbox_data_ult_comp.addWidget(data_ult_comp)
        vbox_data_ult_comp.addWidget(self.edit_data_ult_comp1)

        vbox_val_maior_comp = QVBoxLayout()
        vbox_val_maior_comp.addWidget(val_maior_comp)
        vbox_val_maior_comp.addWidget(self.edit_val_maior_comp1)

        vbox_data_maior_comp = QVBoxLayout()
        vbox_data_maior_comp.addWidget(data_maior_comp)
        vbox_data_maior_comp.addWidget(self.edit_data_maior_comp1)

        vbox_inf_comerc = QVBoxLayout()
        vbox_inf_comerc.addWidget(inf_comercial)
        vbox_inf_comerc.addWidget(self.edit_inf_comercial1)

        hbox_ref_comerc_linha1 = QHBoxLayout()
        hbox_ref_comerc_linha1.addLayout(vbox_loja_ref_comerc)
        hbox_ref_comerc_linha1.addLayout(vbox_tel_ref_comerc)
        hbox_ref_comerc_linha1.addLayout(vbox_inic_comp_comerc)
        hbox_ref_comerc_linha1.addLayout(vbox_val_ult_comp)
        hbox_ref_comerc_linha1.addLayout(vbox_data_ult_comp)
        hbox_ref_comerc_linha1.addLayout(vbox_val_maior_comp)
        hbox_ref_comerc_linha1.addLayout(vbox_data_maior_comp)
        hbox_ref_comerc_linha1.addLayout(vbox_inf_comerc)

        hbox_ref_comerc_linha2 = QHBoxLayout()
        hbox_ref_comerc_linha2.addWidget(self.edit_loja_ref_comerc2)
        hbox_ref_comerc_linha2.addWidget(self.edit_tel_ref_comerc2)
        hbox_ref_comerc_linha2.addWidget(self.edit_inic_comp_comerc2)
        hbox_ref_comerc_linha2.addWidget(self.edit_val_ult_comp2)
        hbox_ref_comerc_linha2.addWidget(self.edit_data_ult_comp2)
        hbox_ref_comerc_linha2.addWidget(self.edit_val_maior_comp2)
        hbox_ref_comerc_linha2.addWidget(self.edit_data_maior_comp2)
        hbox_ref_comerc_linha2.addWidget(self.edit_inf_comercial2)

        hbox_ref_comerc_linha3 = QHBoxLayout()
        hbox_ref_comerc_linha3.addWidget(self.edit_loja_ref_comerc3)
        hbox_ref_comerc_linha3.addWidget(self.edit_tel_ref_comerc3)
        hbox_ref_comerc_linha3.addWidget(self.edit_inic_comp_comerc3)
        hbox_ref_comerc_linha3.addWidget(self.edit_val_ult_comp3)
        hbox_ref_comerc_linha3.addWidget(self.edit_data_ult_comp3)
        hbox_ref_comerc_linha3.addWidget(self.edit_val_maior_comp3)
        hbox_ref_comerc_linha3.addWidget(self.edit_data_maior_comp3)
        hbox_ref_comerc_linha3.addWidget(self.edit_inf_comercial3)

        vbox_geral_aba_ref = QVBoxLayout()
        vbox_geral_aba_ref.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        vbox_geral_aba_ref.addLayout(hbox_ref_linha1)
        vbox_geral_aba_ref.addLayout(hbox_ref_linha2)
        vbox_geral_aba_ref.addLayout(hbox_ref_linha3)
        vbox_geral_aba_ref.addLayout(vbox_ref_pess)
        vbox_geral_aba_ref.addLayout(hbox_ref_pess_linha1)
        vbox_geral_aba_ref.addLayout(hbox_ref_pess_linha2)
        vbox_geral_aba_ref.addLayout(hbox_ref_pess_linha3)
        vbox_geral_aba_ref.addLayout(vbox_ref_comerc)
        vbox_geral_aba_ref.addLayout(hbox_ref_comerc_linha1)
        vbox_geral_aba_ref.addLayout(hbox_ref_comerc_linha2)
        vbox_geral_aba_ref.addLayout(hbox_ref_comerc_linha3)

        aba_ref.setLayout(vbox_geral_aba_ref)

        self.table_cliente.addTab(aba_dados, "Dados")
        self.table_cliente.addTab(aba_ref, 'Referências')

        self.table_cliente.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #444444;
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
        vbox_tabs_cliente.addWidget(self.table_cliente)
        vbox_tabs_cliente.setContentsMargins(20, 20, 20, 20)

        aba2.setLayout(vbox_tabs_cliente)

        self.tab.addTab(aba1, "Consulta")
        self.tab.addTab(aba2, "Cadastro")

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
        vbox.addWidget(self.tab)
        vbox.addLayout(hbox_botoes)
        vbox.setContentsMargins(20, 20, 20, 20)

        self.setLayout(vbox)
        
    def salvar(self):
        dados = self.coletar_dados_formulario()
        if dados["codigo"]:
            resultado = self.service.atualizar_cliente(dados)
        else:
            resultado = self.service.salvar_cliente(dados)

        if resultado["sucesso"]:
            QMessageBox.information(self, "Sucesso", resultado["mensagem"])
            self.limpar_campos()
            self.tab.setCurrentIndex(0)
            self.acao_buscar_cliente()
            return

        QMessageBox.warning(self, "Aviso", resultado["mensagem"])
        if "Razao" in resultado["mensagem"]:
            self.edit_raz_social.setFocus()
        elif any(texto in resultado["mensagem"] for texto in ("CPF", "CNPJ", "cadastrado", "documento")):
            self.edit_cnpj_cli.setFocus()
            self.edit_cnpj_cli.selectAll()


    def coletar_dados_formulario(self):
        if self.check_jur.isChecked():
            tipo_pessoa = "J"
        elif self.check_fis.isChecked():
            tipo_pessoa = "F"
        else:
            tipo_pessoa = ""

        return {
            "codigo": self.edit_cod_cli.text().strip(),
            "tipo_pessoa": tipo_pessoa,
            "razao_social": self.edit_raz_social.text().strip(),
            "nome_fantasia": self.edit_fant_cli.text().strip(),
            "contato": self.edit_cont_cli.text().strip(),
            "whatsapp": self.edit_zap_cli.text().strip(),
            "telefone": self.edit_tel_cli.text().strip(),
            "email": self.edit_email_cli.text().strip(),
            "cep": self.edit_cep_cli.text().strip(),
            "endereco": self.edit_end_cli.text().strip(),
            "numero": self.edit_num_cli.text().strip(),
            "bairro": self.edit_bairro_cli.text().strip(),
            "cidade": self.edit_cid_cli.text().strip(),
            "uf": self.edit_est_cli.text().strip(),
            "cpf_cnpj": self.edit_cnpj_cli.text().strip(),
            "inscricao_estadual": self.edit_insc_cli.text().strip(),
            "inscricao_municipal": self.edit_insc_mun_cli.text().strip(),
            "data_referencia": self.edit_dt_nasc_cli.text().strip(),
            "sexo": self.comb_sexo_cli.currentText() if self.comb_sexo_cli.currentText() != "Selecione" else "",

            "nome_mae": self.edit_nome_mae.text().strip(),
            "nome_pai": self.edit_nome_pai.text().strip(),
            "cidade_nascimento": self.edit_nacion_cli.text().strip(),
            "pais_nascimento": self.edit_natur_cli.text().strip(),

            "local_trabalho": self.edit_loc_trab.text().strip(),
            "cargo": self.edit_carg_trab.text().strip(),
            "tempo_servico": self.edit_temp_serv.text().strip(),
            "salario": self.edit_salario.text().strip(),
            "telefone_trabalho": self.edit_tel_trab.text().strip(),

            "cep_trabalho": self.edit_cep_trab.text().strip(),
            "endereco_trabalho": self.edit_end_trab.text().strip(),
            "numero_trabalho": self.edit_num_trab.text().strip(),
            "bairro_trabalho": self.edit_bairro_trab.text().strip(),
            "cidade_trabalho": self.edit_cid_trab.text().strip(),
            "uf_trabalho": self.edit_est_trab.text().strip(),

            "info_adicional": self.text_inf_add_cli.toPlainText().strip(),
            "status": self.status_atual,
        }

    def limpar_campos(self):
        self.status_atual = "A"
        campos = [
            self.edit_cod_cli, self.edit_raz_social, self.edit_fant_cli, self.edit_cont_cli, self.edit_zap_cli,
            self.edit_tel_cli, self.edit_email_cli, self.edit_cep_cli, self.edit_end_cli, self.edit_num_cli,
            self.edit_bairro_cli, self.edit_cid_cli, self.edit_est_cli, self.edit_cnpj_cli, self.edit_insc_cli,
            self.edit_insc_mun_cli, self.edit_dt_nasc_cli, self.edit_nacion_cli, self.edit_natur_cli,
            self.edit_nome_mae, self.edit_nome_pai, self.edit_loc_trab, self.edit_carg_trab, self.edit_temp_serv,
            self.edit_salario, self.edit_tel_trab, self.edit_cep_trab, self.edit_end_trab, self.edit_num_trab,
            self.edit_bairro_trab, self.edit_cid_trab, self.edit_est_trab, self.edit_nome_ref_pess1,
            self.edit_nome_ref_pess2, self.edit_nome_ref_pess3, self.edit_tel_ref_pess1, self.edit_tel_ref_pess2,
            self.edit_tel_ref_pess3, self.edit_inf_pess1, self.edit_inf_pess2, self.edit_inf_pess3,
            self.edit_loja_ref_comerc1, self.edit_loja_ref_comerc2, self.edit_loja_ref_comerc3,
            self.edit_tel_ref_comerc1, self.edit_tel_ref_comerc2, self.edit_tel_ref_comerc3,
            self.edit_inic_comp_comerc1, self.edit_inic_comp_comerc2, self.edit_inic_comp_comerc3,
            self.edit_val_ult_comp1, self.edit_val_ult_comp2, self.edit_val_ult_comp3,
            self.edit_data_ult_comp1, self.edit_data_ult_comp2, self.edit_data_ult_comp3,
            self.edit_val_maior_comp1, self.edit_val_maior_comp2, self.edit_val_maior_comp3,
            self.edit_data_maior_comp1, self.edit_data_maior_comp2, self.edit_data_maior_comp3,
            self.edit_inf_comercial1, self.edit_inf_comercial2, self.edit_inf_comercial3,
        ]
        for campo in campos:
            campo.clear()

        self.text_inf_add_cli.clear()
        self.comb_sexo_cli.setCurrentIndex(0)
        self.check_jur.setChecked(False)
        self.check_fis.setChecked(False)
        self.table_cliente.setCurrentIndex(0)
        self.edit_raz_social.setFocus()

    def acao_buscar_cliente(self, *args):
        texto = self.edit_label_pesq.text().strip()
        opcao = self.comb_opc.currentText()
        status = self.combo_ativo.currentText()
        buscar_todos = self.check_todos.isChecked()

        if not texto and not buscar_todos:
            self.tabela_resultado.setRowCount(0)
            return

        resultados = self.service.buscar_cliente(opcao, texto, status, buscar_todos)
        self.tabela_resultado.setRowCount(len(resultados))
        for linha, cliente in enumerate(resultados):
            for coluna, valor in enumerate(cliente):
                item = QTableWidgetItem(str(valor) if valor is not None else "")
                if coluna == 5:
                    if valor == "A":
                        item.setText("Ativo")
                    elif valor == "E":
                        item.setText("Excluido")
                        item.setForeground(Qt.GlobalColor.red)
                self.tabela_resultado.setItem(linha, coluna, item)

    def abrir_cliente_selecionado(self):
        linha = self.tabela_resultado.currentRow()
        if linha == -1:
            return
        codigo_item = self.tabela_resultado.item(linha, 0)
        if codigo_item is None:
            return
        cliente = self.service.buscar_por_codigo(codigo_item.text())
        if not cliente:
            return
        self.carregar_cliente_no_formulario(cliente)
        self.tab.setCurrentIndex(1)


    def carregar_cliente_no_formulario(self, cliente):
        self.edit_cod_cli.setText(str(cliente[1]) if cliente[1] is not None else "")
        self.edit_raz_social.setText(cliente[3] or "")
        self.edit_fant_cli.setText(cliente[4] or "")
        self.edit_cont_cli.setText(cliente[5] or "")
        self.edit_zap_cli.setText(cliente[6] or "")
        self.edit_tel_cli.setText(cliente[7] or "")
        self.edit_email_cli.setText(cliente[8] or "")
        self.edit_cep_cli.setText(cliente[9] or "")
        self.edit_end_cli.setText(cliente[10] or "")
        self.edit_num_cli.setText(cliente[11] or "")
        self.edit_bairro_cli.setText(cliente[12] or "")
        self.edit_cid_cli.setText(cliente[13] or "")
        self.edit_est_cli.setText(cliente[14] or "")
        self.edit_cnpj_cli.setText(cliente[15] or "")
        self.edit_insc_cli.setText(cliente[16] or "")
        self.edit_insc_mun_cli.setText(cliente[17] or "")

        data = cliente[18]
        if data:
            texto_data = str(data)
            if "-" in texto_data:
                ano, mes, dia = texto_data.split("-")
                self.edit_dt_nasc_cli.setText(f"{dia}/{mes}/{ano}")
            else:
                self.edit_dt_nasc_cli.setText(texto_data)
        else:
            self.edit_dt_nasc_cli.clear()

        sexo = cliente[19] or ""
        indice_sexo = self.comb_sexo_cli.findText(sexo)
        self.comb_sexo_cli.setCurrentIndex(indice_sexo if indice_sexo >= 0 else 0)

        self.text_inf_add_cli.setPlainText(cliente[20] or "")
        self.status_atual = cliente[21] or "A"

        self.edit_nome_mae.setText(cliente[22] or "")
        self.edit_loc_trab.setText(cliente[23] or "")
        self.edit_carg_trab.setText(cliente[24] or "")
        self.edit_salario.setText(cliente[25] or "")
        self.edit_tel_trab.setText(cliente[26] or "")

        self.edit_nome_pai.setText(cliente[27] or "")
        self.edit_nacion_cli.setText(cliente[28] or "")
        self.edit_natur_cli.setText(cliente[29] or "")
        self.edit_temp_serv.setText(cliente[30] or "")
        self.edit_cep_trab.setText(cliente[31] or "")
        self.edit_end_trab.setText(cliente[32] or "")
        self.edit_num_trab.setText(cliente[33] or "")
        self.edit_bairro_trab.setText(cliente[34] or "")
        self.edit_cid_trab.setText(cliente[35] or "")
        self.edit_est_trab.setText(cliente[36] or "")

        tipo_pessoa = cliente[2] or ""
        if tipo_pessoa == "J":
            self.check_jur.setChecked(True)
        elif tipo_pessoa == "F":
            self.check_fis.setChecked(True)
        else:
            self.check_jur.setChecked(False)
            self.check_fis.setChecked(False)

            
    def sair(self):
        from entidades.tela_ent import TelaEntidades
        self.janela = TelaEntidades()
        self.janela.show()
        self.close()

    def atualiza_form(self):
        if self.check_jur.isChecked():
            self.cnpj_cli.setText("CNPJ")
            self.edit_cnpj_cli.setInputMask("00.000.000/0000-00;_")
            self.insc_cli.setText("Insc. Estadual")
            self.dt_nasc_cli.setText("Abertura")
        elif self.check_fis.isChecked():
            self.cnpj_cli.setText("CPF")
            self.edit_cnpj_cli.setInputMask("000.000.000-00;_")
            self.insc_cli.setText("RG")
            self.dt_nasc_cli.setText("Nascimento")

        for label in (self.cnpj_cli, self.insc_cli, self.dt_nasc_cli):
            label.setContentsMargins(2, 0, 0, 0)
            label.setFixedSize(label.sizeHint())
    def buscar_cep(self):
        origem = self.sender()
        if origem is None:
            return

        dados = consulta_cep(origem.text())
        if origem is self.edit_cep_cli:
            destino_end, destino_bairro, destino_cidade, destino_uf = (
                self.edit_end_cli,
                self.edit_bairro_cli,
                self.edit_cid_cli,
                self.edit_est_cli,
            )
        elif origem is self.edit_cep_trab:
            destino_end, destino_bairro, destino_cidade, destino_uf = (
                self.edit_end_trab,
                self.edit_bairro_trab,
                self.edit_cid_trab,
                self.edit_est_trab,
            )
        else:
            return

        if dados is None:
            QMessageBox.warning(self, "CEP invalido", "CEP Inválido.")
            return

        if dados:
            destino_end.setText(dados.get("logradouro", "").upper())
            destino_bairro.setText(dados.get("bairro", "").upper())
            destino_cidade.setText(dados.get("localidade", "").upper())
            destino_uf.setText(dados.get("uf", "").upper())

    def ao_trocar_aba(self, index):
        if index == 1:
            self.edit_raz_social.setFocus()
            if not self.check_jur.isChecked() and not self.check_fis.isChecked():
                self.check_jur.setChecked(True)

    def alterar_status_cliente(self):
        codigo = self.edit_cod_cli.text().strip()
        if not codigo:
            QMessageBox.warning(self, "Aviso", "Nenhum cliente selecionado.")
            return

        cliente = self.service.buscar_por_codigo(codigo)
        if not cliente:
            QMessageBox.warning(self, "Erro", "Cliente nao encontrado.")
            return

        if cliente[21] == "A":
            novo_status = "E"
            mensagem = "Deseja EXCLUIR este cliente?"
            acao = "excluido"
        else:
            novo_status = "A"
            mensagem = "Deseja ATIVAR este cliente?"
            acao = "ativado"

        confirmacao = QMessageBox.question(
            self,
            "Confirmacao",
            mensagem,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirmacao != QMessageBox.StandardButton.Yes:
            return

        resultado = self.service.alterar_status(codigo, novo_status)
        if resultado["sucesso"]:
            QMessageBox.information(self, "Sucesso", f"Cliente {acao} com sucesso!")
            self.limpar_campos()
            self.tab.setCurrentIndex(0)
            self.acao_buscar_cliente()
        else:
            QMessageBox.warning(self, "Erro", resultado["mensagem"])

    def novo_cliente(self):
        self.limpar_campos()
        self.tab.setCurrentIndex(1)
        self.check_jur.setChecked(True)
        self.edit_raz_social.setFocus()

    def cancelar(self):
        self.limpar_campos()
        self.tab.setCurrentIndex(0)

    def validar_documento(self):
        documento = self.edit_cnpj_cli.text().strip()
        if not documento:
            return

        if self.check_jur.isChecked():
            tipo_pessoa = "J"
        elif self.check_fis.isChecked():
            tipo_pessoa = "F"
        else:
            QMessageBox.warning(self, "Aviso", "Selecione Juridica ou Fisica.")
            self.check_jur.setFocus()
            return

        resultado = self.service.validar_documento(tipo_pessoa, documento)
        if not resultado["sucesso"]:
            QMessageBox.warning(self, "Aviso", resultado["mensagem"])
            self.edit_cnpj_cli.setFocus()
            self.edit_cnpj_cli.selectAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = CadCliente()
    janela.show()
    sys.exit(app.exec())
