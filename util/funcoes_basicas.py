from PyQt6.QtWidgets import QApplication


def centralizar_tela(widget):
    widget.move(QApplication.primaryScreen(
    ).availableGeometry().center() - widget.rect().center())
