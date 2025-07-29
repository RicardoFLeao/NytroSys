
cores = {
    "cor1": "#01050D",
    "cor2": "#030C26",
    "cor3": "#031740",
    "cor4": "#364959",
    "cor5": "#70818C",
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
    """
