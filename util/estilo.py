
cores = {
    "cor1": "#01050D",
    "cor2": "#030C26",
    "cor3": "#031740",
    "cor4": "#364959",
    "cor5": "#70818C",
    "cor6": "#cbdae4",
    "branco": "#FFFFFF"
}
def gerar_estilo():
    return f"""
    QMainWindow {{
        background-color: {cores['cor1']};
    }}

    QWidget {{
        background-color: #01050D;
    }}

    QPushButton {{
        background-color: {cores['cor3']};
        color: {cores['branco']};
        border: 2px solid {cores['cor4']};
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }}

    QPushButton:hover {{
        background-color: {cores['cor2']};
        border: 2px solid {cores['cor5']};
    }}

    QMenuBar {{
        background-color: {cores['cor3']};
        color: {cores['branco']};
    }}

    QMenuBar::item:selected {{
        background-color: {cores['cor4']};
    }}

    QMenu {{
        background-color: {cores['cor3']};
        color: {cores['branco']};
    }}

    QMenu::item:selected {{
        background-color: {cores['cor4']};
    }}

    QMessageBox {{
    background-color: #f4f0ea;
    }}

    QMessageBox QLabel#qt_msgbox_label {{
        color: #111111;
        background-color: transparent;
        font-size: 14px;
        min-width: 220px;
    }}

    QMessageBox QLabel#qt_msgboxex_icon_label {{
        background-color: transparent;
    }}

    QMessageBox QPushButton {{
        background-color: #031740;
        color: #FFFFFF;
        min-width: 90px;
        min-height: 35px;
        padding: 4px 12px;
        border: 2px solid #364959;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
    }}

    QMessageBox QPushButton:hover {{
        background-color: #030C26;
    }}
    """
