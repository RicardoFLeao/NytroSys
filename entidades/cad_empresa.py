import sys
import os

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'
)))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QPushButton,
    QFileDialog,
    QMessageBox
)

from util.estilo import gerar_estilo
from util.padrao import criar_lineedit_padrao
from util.fun_basicas import consulta_cep


class CadEmpresa(QWidget):
    def __init__(self):
        super().__init__()
        self.logo_path = ""

        self.setWindowTitle("Cadastro da Empresa")
        self.setWindowIcon(QIcon("imagens/icone.png"))

        self.componentes()
        self.showMaximized()

        QShortcut(QKeySequence("Esc"), self).activated.connect(self.sair)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.novo)
        QShortcut(QKeySequence("F2"), self).activated.connect(self.salvar)

        self.edit_cep.editingFinished.connect(self.buscar_cep)

    def componentes(self):
        titulo = QLabel("Empresa")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                color: orange;
                font-size: 40px;
                font-weight: bold;
            }
        """)
        titulo.setFixedHeight(55)

        self.quadro = QFrame()
        self.quadro.setStyleSheet("""
            QFrame {
                background-color: #d9d9d9;
                border-radius: 10px;
            }
        """)

        def criar_label(texto):
            label = QLabel(texto)
            label.setStyleSheet("""
                QLabel {
                    color: #031740;
                    font-size: 14px;
                    font-weight: bold;
                    background: transparent;
                }
            """)
            return label

        # Campos
        self.edit_razao_social = criar_lineedit_padrao()
        self.edit_nome_fantasia = criar_lineedit_padrao()
        self.edit_cnpj = criar_lineedit_padrao()
        self.edit_ie = criar_lineedit_padrao()
        self.edit_telefone = criar_lineedit_padrao()
        self.edit_celular = criar_lineedit_padrao()
        self.edit_email = criar_lineedit_padrao()
        self.edit_cep = criar_lineedit_padrao()
        self.edit_endereco = criar_lineedit_padrao()
        self.edit_numero = criar_lineedit_padrao()
        self.edit_bairro = criar_lineedit_padrao()
        self.edit_cidade = criar_lineedit_padrao()
        self.edit_uf = criar_lineedit_padrao()
        self.edit_observacao = criar_lineedit_padrao()

        self.edit_razao_social.setPlaceholderText("Razão social")
        self.edit_nome_fantasia.setPlaceholderText("Nome fantasia")
        self.edit_cnpj.setPlaceholderText("CNPJ")
        self.edit_ie.setPlaceholderText("Inscrição estadual")
        self.edit_telefone.setPlaceholderText("Telefone")
        self.edit_celular.setPlaceholderText("Celular")
        self.edit_email.setPlaceholderText("E-mail")
        self.edit_cep.setPlaceholderText("CEP")
        self.edit_endereco.setPlaceholderText("Endereço")
        self.edit_numero.setPlaceholderText("Número")
        self.edit_bairro.setPlaceholderText("Bairro")
        self.edit_cidade.setPlaceholderText("Cidade")
        self.edit_uf.setPlaceholderText("UF")
        self.edit_observacao.setPlaceholderText("Observação")

        self.edit_cnpj.setFixedWidth(180)
        self.edit_ie.setFixedWidth(180)
        self.edit_telefone.setFixedWidth(180)
        self.edit_celular.setFixedWidth(180)
        self.edit_cep.setFixedWidth(140)
        self.edit_numero.setFixedWidth(120)
        self.edit_uf.setFixedWidth(80)

        # Logo
        self.label_logo = QLabel("Sem logo")
        self.label_logo.setFixedSize(220, 180)
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_logo.setStyleSheet("""
            QLabel {
                background: white;
                border: 1px solid #bfc7cf;
                color: #444;
            }
        """)

        self.btn_logo = QPushButton("Selecionar Logo")
        self.btn_logo.setFixedHeight(40)
        self.btn_logo.clicked.connect(self.selecionar_logo)
        self.btn_logo.setStyleSheet("""
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

        bloco_logo = QVBoxLayout()
        bloco_logo.setSpacing(10)
        bloco_logo.addWidget(self.label_logo)
        bloco_logo.addWidget(self.btn_logo)
        bloco_logo.addStretch()

        # Botões
        def criar_botao(texto):
            botao = QPushButton(texto)
            botao.setFixedHeight(42)
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
        self.btn_salvar = criar_botao("F2 - Salvar")
        self.btn_cancelar = criar_botao("Cancelar")
        self.btn_sair = criar_botao("ESC - Sair")

        self.btn_novo.clicked.connect(self.novo)
        self.btn_salvar.clicked.connect(self.salvar)
        self.btn_cancelar.clicked.connect(self.novo)
        self.btn_sair.clicked.connect(self.sair)

        linha_botoes = QHBoxLayout()
        linha_botoes.setSpacing(10)
        linha_botoes.addWidget(self.btn_novo)
        linha_botoes.addWidget(self.btn_salvar)
        linha_botoes.addWidget(self.btn_cancelar)
        linha_botoes.addWidget(self.btn_sair)
        linha_botoes.addStretch()

        # Formulário
        grid = QGridLayout()
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(10)

        grid.addWidget(criar_label("Razão Social"), 0, 0)
        grid.addWidget(self.edit_razao_social, 1, 0, 1, 4)

        grid.addWidget(criar_label("Nome Fantasia"), 2, 0)
        grid.addWidget(self.edit_nome_fantasia, 3, 0, 1, 4)

        grid.addWidget(criar_label("CNPJ"), 4, 0)
        grid.addWidget(self.edit_cnpj, 5, 0)

        grid.addWidget(criar_label("IE"), 4, 1)
        grid.addWidget(self.edit_ie, 5, 1)

        grid.addWidget(criar_label("Telefone"), 4, 2)
        grid.addWidget(self.edit_telefone, 5, 2)

        grid.addWidget(criar_label("Celular"), 4, 3)
        grid.addWidget(self.edit_celular, 5, 3)

        grid.addWidget(criar_label("E-mail"), 6, 0)
        grid.addWidget(self.edit_email, 7, 0, 1, 4)

        grid.addWidget(criar_label("CEP"), 8, 0)
        grid.addWidget(self.edit_cep, 9, 0)

        grid.addWidget(criar_label("Endereço"), 8, 1)
        grid.addWidget(self.edit_endereco, 9, 1, 1, 2)

        grid.addWidget(criar_label("Número"), 8, 3)
        grid.addWidget(self.edit_numero, 9, 3)

        grid.addWidget(criar_label("Bairro"), 10, 0)
        grid.addWidget(self.edit_bairro, 11, 0, 1, 2)

        grid.addWidget(criar_label("Cidade"), 10, 2)
        grid.addWidget(self.edit_cidade, 11, 2)

        grid.addWidget(criar_label("UF"), 10, 3)
        grid.addWidget(self.edit_uf, 11, 3)

        grid.addWidget(criar_label("Observação"), 12, 0)
        grid.addWidget(self.edit_observacao, 13, 0, 1, 4)

        bloco_form = QVBoxLayout()
        bloco_form.setSpacing(15)
        bloco_form.addLayout(grid)
        bloco_form.addStretch()
        bloco_form.addLayout(linha_botoes)

        conteudo = QHBoxLayout()
        conteudo.setContentsMargins(20, 20, 20, 20)
        conteudo.setSpacing(20)
        conteudo.addLayout(bloco_form, 1)
        conteudo.addLayout(bloco_logo)

        self.quadro.setLayout(conteudo)

        layout_geral = QVBoxLayout()
        layout_geral.addWidget(titulo)
        layout_geral.addWidget(self.quadro)

        self.setLayout(layout_geral)

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

    def selecionar_logo(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Logo",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )

        if not caminho:
            return

        self.logo_path = caminho

        pixmap = QPixmap(caminho)
        pixmap = pixmap.scaled(
            self.label_logo.width(),
            self.label_logo.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label_logo.setPixmap(pixmap)
        self.label_logo.setText("")

    def novo(self):
        self.edit_razao_social.clear()
        self.edit_nome_fantasia.clear()
        self.edit_cnpj.clear()
        self.edit_ie.clear()
        self.edit_telefone.clear()
        self.edit_celular.clear()
        self.edit_email.clear()
        self.edit_cep.clear()
        self.edit_endereco.clear()
        self.edit_numero.clear()
        self.edit_bairro.clear()
        self.edit_cidade.clear()
        self.edit_uf.clear()
        self.edit_observacao.clear()

        self.logo_path = ""
        self.label_logo.clear()
        self.label_logo.setText("Sem logo")

        self.edit_razao_social.setFocus()

    def salvar(self):
        QMessageBox.information(
            self,
            "Salvar",
            "Tela pronta.\nLigaremos o banco no próximo passo."
        )

    def sair(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(gerar_estilo())
    janela = CadEmpresa()
    janela.show()
    sys.exit(app.exec())