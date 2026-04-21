import sys
import os

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'
)))

from util.estilo import gerar_estilo
from util.padrao import criar_lineedit_padrao, criar_botao
from util.fun_basicas import LineEditComEnter, consulta_cep
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)



class TelaClienteRapido(QDialog):
    def __init__(self, tela_origem=None, nome_inicial=""):
        super().__init__()
        self.tela_origem = tela_origem
        self.setWindowTitle("Cliente Rápido")
        self.setFixedSize(900, 400)
        self.setModal(True)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog
        )

        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'imagens', 'icone.png')
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.componentes()

        self.edit_nome.setText(nome_inicial)
        QTimer.singleShot(0, self.posicionar_cursor_nome)

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.reject)
        self.edit_cep.editingFinished.connect(self.buscar_cep)


    def componentes(self):
        cor_fundo = "#364959"
        cor_borda = "#70818C"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {cor_fundo};
                border: 1px solid {cor_borda};
                border-radius: 6px;
            }}
        """)

        def criar_label(texto):
            label = QLabel(texto)
            label.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    background-color: {cor_fundo};
                }}
            """)
            return label

        titulo = QLabel("Cliente Rápido")
        titulo.setStyleSheet(f"""
            color: orange;
            font-size: 34px;
            font-weight: bold;
            background-color: {cor_fundo};
        """)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.edit_nome = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cpf = criar_lineedit_padrao(LineEditComEnter)
        self.edit_telefone = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cep = criar_lineedit_padrao(LineEditComEnter)
        self.edit_endereco = criar_lineedit_padrao(LineEditComEnter)
        self.edit_numero = criar_lineedit_padrao(LineEditComEnter)
        self.edit_bairro = criar_lineedit_padrao(LineEditComEnter)
        self.edit_cidade = criar_lineedit_padrao(LineEditComEnter)
        self.edit_uf = criar_lineedit_padrao(LineEditComEnter)

        self.edit_nome.setPlaceholderText("Nome do cliente")
        self.edit_cpf.setPlaceholderText("CPF")
        self.edit_telefone.setPlaceholderText("Telefone")
        self.edit_cep.setPlaceholderText("CEP")
        self.edit_endereco.setPlaceholderText("Rua / Avenida")
        self.edit_numero.setPlaceholderText("Número")
        self.edit_bairro.setPlaceholderText("Bairro")
        self.edit_cidade.setPlaceholderText("Cidade")
        self.edit_uf.setPlaceholderText("UF")

        self.edit_cpf.setFixedWidth(180)
        self.edit_telefone.setFixedWidth(180)
        self.edit_cep.setFixedWidth(140)
        self.edit_numero.setFixedWidth(120)
        self.edit_cidade.setFixedWidth(240)
        self.edit_uf.setFixedWidth(90)

        # Nome
        vbox_nome = QVBoxLayout()
        vbox_nome.setSpacing(4)
        vbox_nome.addWidget(criar_label("Nome"))
        vbox_nome.addWidget(self.edit_nome)

        # CPF
        vbox_cpf = QVBoxLayout()
        vbox_cpf.setSpacing(4)
        vbox_cpf.addWidget(criar_label("CPF"))
        vbox_cpf.addWidget(self.edit_cpf)

        # Telefone
        vbox_tel = QVBoxLayout()
        vbox_tel.setSpacing(4)
        vbox_tel.addWidget(criar_label("Telefone"))
        vbox_tel.addWidget(self.edit_telefone)

        # CEP
        vbox_cep = QVBoxLayout()
        vbox_cep.setSpacing(4)
        vbox_cep.addWidget(criar_label("CEP"))
        vbox_cep.addWidget(self.edit_cep)

        linha_cpf_tel_cep = QHBoxLayout()
        linha_cpf_tel_cep.setSpacing(16)
        linha_cpf_tel_cep.addLayout(vbox_cpf)
        linha_cpf_tel_cep.addLayout(vbox_tel)
        linha_cpf_tel_cep.addLayout(vbox_cep)
        linha_cpf_tel_cep.addStretch()

        # Endereço
        vbox_endereco = QVBoxLayout()
        vbox_endereco.setSpacing(4)
        vbox_endereco.addWidget(criar_label("Endereço"))
        vbox_endereco.addWidget(self.edit_endereco)

        # Número
        vbox_numero = QVBoxLayout()
        vbox_numero.setSpacing(4)
        vbox_numero.addWidget(criar_label("Número"))
        vbox_numero.addWidget(self.edit_numero)

        linha_endereco = QHBoxLayout()
        linha_endereco.setSpacing(16)
        linha_endereco.addLayout(vbox_endereco, 1)
        linha_endereco.addLayout(vbox_numero)

        # Bairro
        vbox_bairro = QVBoxLayout()
        vbox_bairro.setSpacing(4)
        vbox_bairro.addWidget(criar_label("Bairro"))
        vbox_bairro.addWidget(self.edit_bairro)

        # Cidade
        vbox_cidade = QVBoxLayout()
        vbox_cidade.setSpacing(4)
        vbox_cidade.addWidget(criar_label("Cidade"))
        vbox_cidade.addWidget(self.edit_cidade)

        # UF
        vbox_uf = QVBoxLayout()
        vbox_uf.setSpacing(4)
        vbox_uf.addWidget(criar_label("UF"))
        vbox_uf.addWidget(self.edit_uf)

        linha_bairro_cidade_uf = QHBoxLayout()
        linha_bairro_cidade_uf.setSpacing(16)
        linha_bairro_cidade_uf.addLayout(vbox_bairro, 1)
        linha_bairro_cidade_uf.addLayout(vbox_cidade)
        linha_bairro_cidade_uf.addLayout(vbox_uf)

        self.btn_confirmar = criar_botao()
        self.btn_confirmar.setText("F12 - Confirmar")
        self.btn_confirmar.setAutoDefault(False)
        self.btn_confirmar.setDefault(False)

        self.btn_sair = criar_botao()
        self.btn_sair.setText("Esc - Sair")
        self.btn_sair.clicked.connect(self.reject)
        self.btn_sair.setAutoDefault(False)
        self.btn_sair.setDefault(False)

        linha_botoes = QHBoxLayout()
        linha_botoes.addWidget(self.btn_confirmar)
        linha_botoes.addStretch()
        linha_botoes.addWidget(self.btn_sair)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.addWidget(titulo)
        layout.addLayout(vbox_nome)
        layout.addLayout(linha_cpf_tel_cep)
        layout.addLayout(linha_endereco)
        layout.addLayout(linha_bairro_cidade_uf)
        layout.addStretch()
        layout.addLayout(linha_botoes)

        self.setLayout(layout)

    def buscar_cep(self):
        cep = self.edit_cep.text().strip()

        if not cep:
            return

        dados = consulta_cep(cep)

        if dados is None:
            return

        if dados == {}:
            return

        self.edit_endereco.setText(dados.get("logradouro", ""))
        self.edit_bairro.setText(dados.get("bairro", ""))
        self.edit_cidade.setText(dados.get("localidade", ""))
        self.edit_uf.setText(dados.get("uf", ""))

        self.edit_numero.setFocus()
        self.edit_numero.selectAll()

    def posicionar_cursor_nome(self):
        self.edit_nome.setFocus()
        self.edit_nome.setSelection(0, 0)
        self.edit_nome.setCursorPosition(len(self.edit_nome.text()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(gerar_estilo())
    janela = TelaClienteRapido(nome_inicial="CLIENTE TESTE")
    janela.exec()