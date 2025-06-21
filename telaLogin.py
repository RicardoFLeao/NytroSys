from PyQt6 import QtCore, QtGui, QtWidgets
from telaMain import telaPrincipal
from bd import verificar_login


class WorkerThread(QtCore.QThread):
    login_result = QtCore.pyqtSignal(object)

    def __init__(self, usuario, senha):
        super().__init__()
        self.usuario = usuario
        self.senha = senha

    def run(self):
        print(
            f">>> [Thread] Verificando login para: {self.usuario} / {self.senha}")
        resultado = verificar_login(self.usuario, self.senha)
        print(f">>> [Thread] Resultado: {resultado}")
        self.login_result.emit(resultado)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(618, 810)

        with open("estilo.css", "r", encoding="utf-8") as f:
            Form.setStyleSheet(f.read())

        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(50, 60, 501, 691))
        self.label.setStyleSheet(
            "border-image: url(imagens/fundo_1.png); border-radius: 15px; border: none;")

        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(100, 100, 401, 601))
        self.label_3.setStyleSheet(
            "background-color: rgba(227, 227, 227, 100); border-radius: 15px;")

        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(122, 164, 361, 90))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setText(
            '<span style="font-size: 50px; font-weight: bold; color: #031740;">Nitro </span><span style="font-size:50px; font-weight: bold; color: #FFA500;">Sys</span>')

        self.lineEdit = QtWidgets.QLineEdit(parent=Form)
        self.lineEdit.setGeometry(QtCore.QRect(150, 269, 301, 61))
        self.lineEdit.setFont(QtGui.QFont("Segoe UI", 12))
        self.lineEdit.setPlaceholderText("Nome de Usuário")

        self.lineEdit_2 = QtWidgets.QLineEdit(parent=Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 373, 301, 61))
        self.lineEdit_2.setFont(QtGui.QFont("Segoe UI", 12))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_2.setPlaceholderText("Senha")

        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(222, 483, 181, 51))
        self.pushButton.setFont(QtGui.QFont(
            "Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.pushButton.setText("Entrar")
        self.pushButton.clicked.connect(lambda: self.validar_login(Form))

        self.pushButton_2 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 573, 181, 51))
        self.pushButton_2.setFont(QtGui.QFont(
            "Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.pushButton_2.setText("Sair")
        self.pushButton_2.clicked.connect(QtWidgets.QApplication.quit)

        Form.move(QtWidgets.QApplication.primaryScreen(
        ).availableGeometry().center() - Form.rect().center())

    def validar_login(self, login_window):
        usuario = self.lineEdit.text().strip()
        senha = self.lineEdit_2.text().strip()

        self.thread = WorkerThread(usuario, senha)
        self.thread.login_result.connect(
            lambda resultado: self.processar_login(resultado, login_window))
        self.thread.start()

    def processar_login(self, resultado, login_window):
        if resultado:
            self.janela = telaPrincipal()
            self.janela.show()
            login_window.close()
        else:
            QtWidgets.QMessageBox.warning(
                None, "Erro", "Usuário ou senha inválidos!")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    Form.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
