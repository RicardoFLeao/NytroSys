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
        QShortcut(QKeySequence('Esc'), self).activated.connect(self.sair)

    def componentes(self):
        nometela = QLabel("Cadastro Funcionários")
        nometela.setStyleSheet("color: orange; font-size:38px; font: bold")

        tab = criar_tab_widget()

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
        lnedit_pesq.setFixedWidth(950)

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
        self.tabela_resultado.setFixedHeight(300)

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
        layout_geral_aba1.addLayout(hbox_botoes_rodape)

        aba1.setLayout(layout_geral_aba1)

        # ----------- ABA 2 (Cadastro) ------------
        aba2 = QWidget()
        aba2.setStyleSheet('background-color: #cbcdce;')

        # linha 1 -- inicio -- 
        #nome funcionario
        nome_func = criar_label_padrao()
        nome_func.setText('Nome do Funcionário')
        nome_func.setContentsMargins(2, 0, 0, 0)
        nome_func.setFixedSize(nome_func.sizeHint())

        edit_nome_func = criar_lineedit_padrao()
        edit_nome_func.setFixedWidth(550)

        vbox_nome_func = QVBoxLayout()
        vbox_nome_func.addWidget(nome_func, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_nome_func.addWidget(edit_nome_func)

        #apelido funcionario
        apelido_fun = criar_label_padrao()
        apelido_fun.setText('Apelido')
        apelido_fun.setContentsMargins(2, 0, 0, 0)
        apelido_fun.setFixedSize(apelido_fun.sizeHint())

        edit_apelido = criar_lineedit_padrao()
        edit_apelido.setFixedWidth(200)

        vbox_apelido_func = QVBoxLayout()
        vbox_apelido_func.addWidget(apelido_fun, alignment=Qt.AlignmentFlag.AlignLeft)
        vbox_apelido_func.addWidget(edit_apelido)

        #cpf do funcionario
        cpf_func = criar_label_padrao()
        cpf_func.setText('CPF')
        cpf_func.setContentsMargins(2, 0, 0, 0)
        cpf_func.setFixedSize(cpf_func.sizeHint())

        edit_cpf_func = criar_lineedit_padrao()
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

        edit_rg_func = criar_lineedit_padrao()
        edit_rg_func.setFixedWidth(200)

        vbox_rg_func = QVBoxLayout()
        vbox_rg_func.addWidget(rg_func)
        vbox_rg_func.addWidget(edit_rg_func)

        #data de nascimento

        dt_nasc_func = criar_label_padrao()
        dt_nasc_func.setText('Nascimento')
        dt_nasc_func.setFixedSize(dt_nasc_func.sizeHint())

        edit_dt_nasc_func = criar_lineedit_padrao()
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
        cad_linha1.addLayout(vbox_nome_func)
        cad_linha1.addLayout(vbox_apelido_func)
        cad_linha1.addLayout(vbox_cpf_func)
        cad_linha1.addLayout(vbox_rg_func)
        cad_linha1.addLayout(vbox_dt_nasc_func)
        cad_linha1.addLayout(vbox_sexo_func)

        # linha 1 -- fim --
        # linha 2 -- inicio --

        #endereço funcionário 
        end_func = criar_label_padrao()
        end_func.setText('Endereço')
        end_func.setContentsMargins(2, 0, 0, 0)
        end_func.setFixedSize(end_func.sizeHint())

        edit_end_func = criar_lineedit_padrao()
        edit_end_func.setFixedWidth(380)

        vbox_end_func = QVBoxLayout()
        vbox_end_func.addWidget(end_func)
        vbox_end_func.addWidget(edit_end_func)


        #bairro funcionário
        bairro_func = criar_label_padrao()
        bairro_func.setText('Bairro')
        bairro_func.setContentsMargins(2, 0, 0, 0)
        bairro_func.setFixedSize(bairro_func.sizeHint())

        edit_bairro_func = criar_lineedit_padrao()
        edit_bairro_func.setFixedWidth(210)

        vbox_bairro_func = QVBoxLayout()
        vbox_bairro_func.addWidget(bairro_func)
        vbox_bairro_func.addWidget(edit_bairro_func)

        #cep funcionário
        cep_func = criar_label_padrao()
        cep_func.setText('CEP')
        cep_func.setContentsMargins(2, 0, 0, 0)
        cep_func.setFixedSize(cep_func.sizeHint())

        edit_cep_func = criar_lineedit_padrao()
        edit_cep_func.setFixedWidth(90)
        edit_cep_func.setInputMask('00.000-000;_')

        vbox_cep_func = QVBoxLayout()
        vbox_cep_func.addWidget(cep_func)
        vbox_cep_func.addWidget(edit_cep_func)

        #cidade funcionário
        cid_func = criar_label_padrao()
        cid_func.setText('Cidade')
        cid_func.setContentsMargins(2, 0, 0, 0)
        cid_func.setFixedSize(cid_func.sizeHint())

        edit_cid_func = criar_lineedit_padrao()
        edit_cid_func.setFixedWidth(255)

        vbox_cid_func = QVBoxLayout()
        vbox_cid_func.addWidget(cid_func)
        vbox_cid_func.addWidget(edit_cid_func)

        #estado funcionario
        est_func = criar_label_padrao()
        est_func.setText('UF')
        est_func.setContentsMargins(2, 0, 0, 0)
        est_func.setFixedSize(est_func.sizeHint())

        comb_est_func = criar_combobox_padrao()
        comb_est_func.setFixedWidth(60)

        vbox_est_func = QVBoxLayout()
        vbox_est_func.addWidget(est_func)
        vbox_est_func.addWidget(comb_est_func)

        #WhatsApp
        zap_func = criar_label_padrao()
        zap_func.setText('WhatsApp')
        zap_func.setContentsMargins(2, 0, 0, 0)
        zap_func.setFixedSize(zap_func.sizeHint())

        edit_zap_func = criar_lineedit_padrao()
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

        edit_tel_func = criar_lineedit_padrao()
        edit_tel_func.setFixedWidth(130)
        edit_tel_func.setInputMask('(00)00000-0000;_')

        vbox_tel_func = QVBoxLayout()
        vbox_tel_func.addWidget(tel_func)
        vbox_tel_func.addWidget(edit_tel_func)

        #layout linha 2
        cad_linha2 = QHBoxLayout()
        cad_linha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cad_linha2.addLayout(vbox_end_func)
        cad_linha2.addLayout(vbox_bairro_func)
        cad_linha2.addLayout(vbox_cep_func)
        cad_linha2.addLayout(vbox_cid_func)
        cad_linha2.addLayout(vbox_est_func)
        cad_linha2.addLayout(vbox_zap_func)
        cad_linha2.addLayout(vbox_tel_func)

        #layout geral apresentação na tela aba2

        layout_geral_aba2 = QVBoxLayout()
        layout_geral_aba2.setContentsMargins(20, 20, 20, 0)
        layout_geral_aba2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_geral_aba2.addLayout(cad_linha1)
        layout_geral_aba2.addLayout(cad_linha2)

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
        vbox.setContentsMargins(30, 50, 30, 50)

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
        from entidades import TelaEntidades
        self.janela = TelaEntidades()
        self.janela.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = CadFuncionarios()
    janela.show()
    sys.exit(app.exec())
