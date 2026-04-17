from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTabWidget,
    QFileDialog
)
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence, QPixmap
from PyQt6.QtCore import Qt
from util.estilo import gerar_estilo
from util.padrao import (
    criar_botao,
    criar_botao_sair,
    criar_combobox_padrao,
    criar_label_padrao,
    criar_lineedit_padrao,
    criar_tab_widget,
)
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TelaDadosAdicionaisProd(QWidget):
    def __init__(self, tela_origem=None):
        super().__init__()

        self.tela_origem = tela_origem
        self.setWindowTitle("Dados Adicionais")
        self.setFixedSize(900, 650)

        self.componentes()

    def componentes(self):

        titulo = QLabel("Dados Adicionais")
        titulo.setStyleSheet("color: orange; font-size: 26px; font: bold;")

        tab_superior = criar_tab_widget()

        aba_imagens = QWidget()
        aba_imagens.setStyleSheet('background-color: #cbcdce;')
        tab_superior.addTab(aba_imagens, "Imagens")

        tab_imagens = criar_tab_widget()
        aba_img_1 = QWidget()
        aba_img_2 = QWidget()
        aba_img_3 = QWidget()

        tab_imagens.addTab(aba_img_1, "Foto 1")
        tab_imagens.addTab(aba_img_2, "Foto 2")
        tab_imagens.addTab(aba_img_3, "Foto 3")

        layout_img_1 = QVBoxLayout(aba_img_1)

        self.label_foto_1 = QLabel("Sem imagem")
        self.label_foto_1.setFixedSize(320, 240)
        self.label_foto_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_foto_1.setStyleSheet("""
            QLabel {
                border: 1px solid #70818C;
                background-color: #364959;
                color: white;
            }
        """)

        self.edit_caminho_1 = criar_lineedit_padrao()
        self.edit_caminho_1.setPlaceholderText("Caminho da imagem 1")
        self.edit_caminho_1.editingFinished.connect(self.carregar_imagem_1)

        self.botao_explorar_1 = criar_botao()
        self.botao_explorar_1.setText("Explorar")
        self.botao_explorar_1.clicked.connect(self.procurar_imagem_1)

        hbox_caminho = QHBoxLayout()
        hbox_caminho.addWidget(self.edit_caminho_1)
        hbox_caminho.addWidget(self.botao_explorar_1)

        layout_img_1.addWidget(
            self.label_foto_1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_img_1.addLayout(hbox_caminho)

        layout_aba_imagens = QVBoxLayout(aba_imagens)
        layout_aba_imagens.addWidget(tab_imagens)

        layout_img_2 = QVBoxLayout(aba_img_2)

        self.label_foto_2 = QLabel("Sem imagem")
        self.label_foto_2.setFixedSize(320, 240)
        self.label_foto_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_foto_2.setStyleSheet("""
            QLabel {
                border: 1px solid #70818C;
                background-color: #364959;
                color: white;
            }
        """)

        self.edit_caminho_2 = criar_lineedit_padrao()
        self.edit_caminho_2.setPlaceholderText("Caminho da imagem 2")
        self.edit_caminho_2.editingFinished.connect(self.carregar_imagem_2)

        self.botao_explorar_2 = criar_botao()
        self.botao_explorar_2.setText("Explorar")
        self.botao_explorar_2.clicked.connect(self.procurar_imagem_2)

        hbox_caminho_2 = QHBoxLayout()
        hbox_caminho_2.addWidget(self.edit_caminho_2)
        hbox_caminho_2.addWidget(self.botao_explorar_2)

        layout_img_2.addWidget(
            self.label_foto_2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_img_2.addLayout(hbox_caminho_2)

        layout_img_3 = QVBoxLayout(aba_img_3)

        self.label_foto_3 = QLabel("Sem imagem")
        self.label_foto_3.setFixedSize(320, 240)
        self.label_foto_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_foto_3.setStyleSheet("""
            QLabel {
                border: 1px solid #70818C;
                background-color: #364959;
                color: white;
            }
        """)

        self.edit_caminho_3 = criar_lineedit_padrao()
        self.edit_caminho_3.setPlaceholderText("Caminho da imagem 3")
        self.edit_caminho_3.editingFinished.connect(self.carregar_imagem_3)

        self.botao_explorar_3 = criar_botao()
        self.botao_explorar_3.setText("Explorar")
        self.botao_explorar_3.clicked.connect(self.procurar_imagem_3)

        hbox_caminho_3 = QHBoxLayout()
        hbox_caminho_3.addWidget(self.edit_caminho_3)
        hbox_caminho_3.addWidget(self.botao_explorar_3)

        layout_img_3.addWidget(
            self.label_foto_3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_img_3.addLayout(hbox_caminho_3)

        aba_inf_tecnicas = QWidget()
        aba_inf_tecnicas.setStyleSheet('background-color: #cbcdce;')
        tab_superior.addTab(aba_inf_tecnicas, "Inf. Técnicas")

        self.botao_retornar = criar_botao()
        self.botao_retornar.setText("F12 - Retornar")
        self.botao_retornar.clicked.connect(self.retornar_dados)

        hbox_botao = QHBoxLayout()
        hbox_botao.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox_botao.addWidget(self.botao_retornar)

        # layout geral
        layout_geral = QVBoxLayout()
        layout_geral.setContentsMargins(20, 20, 20, 20)
        layout_geral.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_geral.addWidget(tab_superior)
        layout_geral.addLayout(hbox_botao)

        self.setLayout(layout_geral)

    def procurar_imagem_1(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )

        if caminho:
            self.edit_caminho_1.setText(caminho)

    def procurar_imagem_1(self):
        pasta_inicial = os.path.join("imagens", "produtos")

        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar imagem",
            pasta_inicial,
            "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )

        if caminho:
            caminho_relativo = os.path.relpath(caminho)
            self.edit_caminho_1.setText(caminho_relativo)

            self.carregar_imagem_1()

    def carregar_imagem_1(self):
        caminho = self.edit_caminho_1.text().strip()

        if not caminho:
            self.label_foto_1.clear()
            self.label_foto_1.setText("Sem imagem")
            return

        if not os.path.exists(caminho):
            self.label_foto_1.clear()
            self.label_foto_1.setText("Imagem não encontrada")
            return

        pixmap = QPixmap(caminho)
        pixmap = pixmap.scaled(
            320,
            240,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label_foto_1.setPixmap(pixmap)

    def procurar_imagem_2(self):
        pasta_inicial = os.path.join("imagens", "produtos")

        caminho, _ = QFileDialog.getOpenFileName(
            self, "Selecionar imagem", pasta_inicial,
            "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )

        if caminho:
            self.edit_caminho_2.setText(os.path.relpath(caminho))
            self.carregar_imagem_2()

    def carregar_imagem_2(self):
        caminho = self.edit_caminho_2.text().strip()

        if not os.path.exists(caminho):
            self.label_foto_2.setText("Imagem não encontrada")
            return

        pixmap = QPixmap(caminho).scaled(
            320, 240,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label_foto_2.setPixmap(pixmap)

    def procurar_imagem_3(self):
        pasta_inicial = os.path.join("imagens", "produtos")

        caminho, _ = QFileDialog.getOpenFileName(
            self, "Selecionar imagem", pasta_inicial,
            "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )

        if caminho:
            self.edit_caminho_3.setText(os.path.relpath(caminho))
            self.carregar_imagem_3()

    def carregar_imagem_3(self):
        caminho = self.edit_caminho_3.text().strip()

        if not os.path.exists(caminho):
            self.label_foto_3.setText("Imagem não encontrada")
            return

        pixmap = QPixmap(caminho).scaled(
            320, 240,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label_foto_3.setPixmap(pixmap)

    def retornar_dados(self):
        foto_1 = self.edit_caminho_1.text().strip()
        foto_2 = self.edit_caminho_2.text().strip()
        foto_3 = self.edit_caminho_3.text().strip()

        if self.tela_origem and hasattr(self.tela_origem, "receber_dados_adicionais"):
            self.tela_origem.receber_dados_adicionais(foto_1, foto_2, foto_3)

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    estilo = gerar_estilo()
    app.setStyleSheet(estilo)
    janela = TelaDadosAdicionaisProd()
    janela.show()
    sys.exit(app.exec())
