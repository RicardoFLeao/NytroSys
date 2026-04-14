from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from bd import conectar
import os


class DialogSenhaFuncionario(QDialog):
    def __init__(self, codigo):
        super().__init__()
        self.codigo = codigo

        self.setWindowTitle("Cadastrar Senha")
        self.setFixedSize(380, 320)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "imagens", "icone.png")
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"[ERRO] Icone nao encontrado: {icon_path}")

        self.setStyleSheet("""
            QDialog {
                background-color: #cbcdce;
            }

            QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
            }

            QLineEdit {
                background-color: white;
                color: black;
                font-size: 14px;
                border: 1px solid #777;
                border-radius: 5px;
                padding: 6px;
                min-height: 28px;
            }

            QPushButton {
                background-color: #031740;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #031740;
                border-radius: 8px;
                padding: 8px;
                min-height: 22px;
            }

            QPushButton:hover {
                border: 1px solid orange;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        label_user = QLabel("Usuario")
        self.edit_user = QLineEdit()

        label_senha = QLabel("Senha")
        self.edit_senha = QLineEdit()
        self.edit_senha.setEchoMode(QLineEdit.EchoMode.Password)

        label_conf = QLabel("Confirmar Senha")
        self.edit_conf = QLineEdit()
        self.edit_conf.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar)

        layout.addWidget(label_user)
        layout.addWidget(self.edit_user)
        layout.addSpacing(3)
        layout.addWidget(label_senha)
        layout.addWidget(self.edit_senha)
        layout.addSpacing(3)
        layout.addWidget(label_conf)
        layout.addWidget(self.edit_conf)
        layout.addSpacing(5)
        layout.addWidget(self.btn_salvar)

        self.setLayout(layout)

        self.edit_user.setFocus()
        self.edit_conf.returnPressed.connect(self.salvar)

    def salvar(self):
        usuario = self.edit_user.text().strip()
        senha = self.edit_senha.text().strip()
        confirmar = self.edit_conf.text().strip()

        if not usuario:
            QMessageBox.warning(self, "Aviso", "Informe o usuário.")
            self.edit_user.setFocus()
            return

        if not senha:
            QMessageBox.warning(self, "Aviso", "Informe a senha.")
            self.edit_senha.setFocus()
            return

        if senha != confirmar:
            QMessageBox.warning(self, "Aviso", "As senhas estão diferentes.")
            self.edit_conf.setFocus()
            self.edit_conf.selectAll()
            return

        try:
            conexao = conectar()
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE funcionarios
                    SET usuario = %s, senha = %s
                    WHERE codigo = %s
                    """,
                    (usuario, senha, self.codigo),
                )

            conexao.commit()

            QMessageBox.information(self, "Sucesso", "Usuário e senha SALVOS.")
            self.accept()

        except Exception as erro:
            print("ERRO AO SALVAR SENHA:", erro)
            QMessageBox.warning(self, "Erro", "Erro ao salvar usuário e senha.")