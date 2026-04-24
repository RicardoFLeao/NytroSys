import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtGui import QRegularExpressionValidator, QShortcut, QKeySequence, QPixmap
from PyQt6.QtCore import Qt, QRegularExpression, QTimer
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem

from util.padrao import criar_botao

class TelaPagamento(QDialog):
    def __init__(self, tela_saida=None):
        super().__init__()
        self.tela_saida = tela_saida
        self.valor_total_venda = 0.0

        if self.tela_saida:
            texto_total = self.tela_saida.label_total_venda.text().replace("R$", "").strip()
            self.valor_total_venda = float(texto_total.replace(".", "").replace(",", "."))



        self.setFixedSize(700, 400)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        self.componentes()

    def componentes(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #031740;
                border: 1px solid #70818C;
                border-radius: 6px;
            }
        """)

        titulo = QLabel('Pagamento')
        titulo.setStyleSheet(
            "color: orange; font-size: 28px; font: bold; background-color: #031740;")

        hbox_titulo = QHBoxLayout()
        hbox_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox_titulo.addWidget(titulo)

        quadro_cinza = QWidget()
        quadro_cinza.setFixedSize(670, 330)
        quadro_cinza.setStyleSheet("""
                background-color: #d9d9d9;
                border-radius: 10px;
        """)

        layout_quadro = QVBoxLayout()

        form_pag = QLabel("Formas de pagamento:")
        form_pag.setStyleSheet("""
                font-size: 15px;
                font-weight: bold;
        """)

        hbox_form_pag = QHBoxLayout()
        hbox_form_pag.addWidget(form_pag)

        opc_form_pag = QLabel("1 - À vista / 2 - A prazo:")
        opc_form_pag.setStyleSheet("""
                font-size: 15px;
                font-weight: bold;
        """)
        opc_form_pag.setFixedSize(opc_form_pag.sizeHint())

        self.edit_opc_form_pag = QLineEdit()
        validador = QRegularExpressionValidator(QRegularExpression("[12]"))
        self.edit_opc_form_pag.setValidator(validador)
        self.edit_opc_form_pag.setMaxLength(1)
        self.edit_opc_form_pag.setMaximumWidth(20)
        self.edit_opc_form_pag.setStyleSheet("""
                font-weight: bold;
                border: 1px solid black;
                border-radius: 3px;
        """)
        self.edit_opc_form_pag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_opc_form_pag.textChanged.connect(self.atualizar_conficoes)
        self.edit_opc_form_pag.textChanged.connect(self.ir_para_cond_pag)

        hbox_opc_form_pag = QHBoxLayout()
        hbox_opc_form_pag.addWidget(opc_form_pag)
        hbox_opc_form_pag.addWidget(self.edit_opc_form_pag)

        hbox_linha_form_pag = QHBoxLayout()
        hbox_linha_form_pag.setAlignment(Qt.AlignmentFlag.AlignTop)
        hbox_linha_form_pag.addLayout(hbox_form_pag)
        hbox_linha_form_pag.addStretch()
        hbox_linha_form_pag.addLayout(hbox_opc_form_pag)

        label_cond_pag = QLabel("Condições de pagamento:")
        label_cond_pag.setStyleSheet("""
                font-size: 15px;
                font-weight: bold;
        """)
        label_cond_pag.setFixedSize(label_cond_pag.sizeHint())

        hbox_cond_pag = QHBoxLayout()
        hbox_cond_pag.addWidget(label_cond_pag)

        self.opcoes_cond_pag = QLabel(
            "1 - Dinh. / 2 - Pix / 3 - Cartão / 4 - Cheque:")
        self.opcoes_cond_pag.setStyleSheet("""
                font-size: 15px;
                font-weight: bold;
        """)
        self.opcoes_cond_pag.setFixedWidth(380)
        self.opcoes_cond_pag.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.edit_opc_cond_pag = QLineEdit()
        self.edit_opc_cond_pag.setMaxLength(1)
        self.edit_opc_cond_pag.setMaximumWidth(20)
        self.edit_opc_cond_pag.setStyleSheet("""
                font-weight: bold;
                border: 1px solid black;
                border-radius: 3px;
        """)
        self.edit_opc_cond_pag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_opc_cond_pag.textChanged.connect(self.verificar_fluxo_pagamento)

        hbox_opc_cond_pag = QHBoxLayout()
        hbox_opc_cond_pag.addWidget(self.opcoes_cond_pag)
        hbox_opc_cond_pag.addWidget(self.edit_opc_cond_pag)

        hbox_linha_cond_pag = QHBoxLayout()
        hbox_linha_cond_pag.setAlignment(Qt.AlignmentFlag.AlignTop)
        hbox_linha_cond_pag.addLayout(hbox_cond_pag)
        hbox_linha_cond_pag.addStretch()
        hbox_linha_cond_pag.addLayout(hbox_opc_cond_pag)


        self.tabela_parcelas = QTableWidget()
        self.tabela_parcelas.setRowCount(0)
        self.tabela_parcelas.setColumnCount(6)
        self.tabela_parcelas.setHorizontalHeaderLabels(["Parc.", "Dias", "Data", "%", "Valor", "OBS."])
        self.adicionar_linha_parcela()
        self.tabela_parcelas.itemChanged.connect(self.verificar_ultima_linha)
        self.tabela_parcelas.itemChanged.connect(self.preencher_data_parcela)
        self.tabela_parcelas.itemChanged.connect(self.preencher_dias_pela_data)
        self.tabela_parcelas.itemChanged.connect(self.preencher_valor_pelo_percentual)
        self.tabela_parcelas.itemChanged.connect(self.preencher_percentual_pelo_valor)



        self.tabela_parcelas.verticalHeader().setVisible(False)
        self.tabela_parcelas.setShowGrid(True)
        self.tabela_parcelas.setSelectionBehavior(self.tabela_parcelas.SelectionBehavior.SelectRows)
        self.tabela_parcelas.setSelectionMode(self.tabela_parcelas.SelectionMode.SingleSelection) 
        self.tabela_parcelas.setAlternatingRowColors(True)      

        header = self.tabela_parcelas.horizontalHeader()
        header.setStretchLastSection(True)

        self.tabela_parcelas.setColumnWidth(0, 60)
        self.tabela_parcelas.setColumnWidth(1, 70)
        self.tabela_parcelas.setColumnWidth(2, 120)
        self.tabela_parcelas.setColumnWidth(3, 60)


        self.tabela_parcelas.setFixedHeight(175)
        self.tabela_parcelas.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #70818C;
                border-radius: 6px;
                font-size: 13px;
                selection-background-color: #031740;
                selection-color: white;
                gridline-color: #70818C;
            }

            QHeaderView::section {
                background-color: #031740;
                color: orange;
                font-weight: bold;
                border: none;
                padding: 2px;
            }

            QTableWidget::item {
                padding: 6px;
                border: none;
                color: #000000;
            }

            QTableWidget::item:selected {
                background-color: #cbdae4;
                color: black;
            }
        """)

        self.atalho_enter_tabela = QShortcut(QKeySequence(Qt.Key.Key_Return), self.tabela_parcelas)
        self.atalho_enter_tabela.activated.connect(self.avancar_tabela)

        self.atalho_enter_tabela2 = QShortcut(QKeySequence(Qt.Key.Key_Enter), self.tabela_parcelas)
        self.atalho_enter_tabela2.activated.connect(self.avancar_tabela)



        label_obs = QLabel('OBS:')
        label_obs.setStyleSheet("""
            font: bold;
        """)
        label_obs.setFixedSize(label_obs.sizeHint())

        self.edit_obs = QLineEdit()
        self.edit_obs.setStyleSheet("""
                background-color: white;
                border: 1px solid black;
                border-radius: 3px;
        """)
        self.edit_obs.setFixedHeight(25)

        hbox_obs = QHBoxLayout()
        hbox_obs.addWidget(label_obs)
        hbox_obs.addWidget(self.edit_obs)

        self.btn_imprimir = criar_botao()
        self.btn_imprimir.setText("F12 - Grava/Imp.")

        self.btn_grava = criar_botao()
        self.btn_grava.setText("F11 - Grava")
        self.btn_grava.clicked.connect(self.salvar)


        self.btn_retornar = criar_botao()
        self.btn_retornar.setText('Esc - Retornar')
        self.btn_retornar.clicked.connect(self.fechar)


        hbox_botoes = QHBoxLayout()
        hbox_botoes.addWidget(self.btn_imprimir)
        hbox_botoes.addSpacing(10)
        hbox_botoes.addWidget(self.btn_grava)
        hbox_botoes.addSpacing(10)
        hbox_botoes.addWidget(self.btn_retornar)




        layout_quadro.addLayout(hbox_linha_form_pag)
        layout_quadro.addLayout(hbox_linha_cond_pag)
        layout_quadro.addSpacing(10)
        layout_quadro.addWidget(self.tabela_parcelas)
        layout_quadro.addSpacing(10)
        layout_quadro.addLayout(hbox_obs)
        layout_quadro.addSpacing(10)
        layout_quadro.addLayout(hbox_botoes)
        layout_quadro.addStretch()

        quadro_cinza.setLayout(layout_quadro)

        vbox_geral = QVBoxLayout()
        vbox_geral.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox_geral.addLayout(hbox_titulo)
        vbox_geral.addWidget(quadro_cinza)
        vbox_geral.addStretch()

        self.setLayout(vbox_geral)

        QTimer.singleShot(0, self.edit_opc_form_pag.setFocus)

    def atualizar_conficoes(self, texto):
        self.edit_opc_cond_pag.clear()

        if texto == "1":
            self.opcoes_cond_pag.setText(
                "1 - Dinh. / 2 - Pix / 3 - Cartão / 4 - Cheque:")
            validador = QRegularExpressionValidator(QRegularExpression("[1234]"))
            self.edit_opc_cond_pag.setValidator(validador)
        
        elif texto == "2":
            self.opcoes_cond_pag.setText(
                "1 - Duplic. / 2 - Requis. / 3 - Cartão / 4 - Cheque:")
            validador = QRegularExpressionValidator(QRegularExpression("[1234]"))
            self.edit_opc_cond_pag.setValidator(validador)
        
        else:
            self.opcoes_cond_pag.setText("Escolha uma forma de pagamento")

    def ir_para_cond_pag(self, texto):
        if texto in ["1", "2"]:
            self.edit_opc_cond_pag.setFocus()
            self.edit_opc_cond_pag.selectAll()


    def adicionar_linha_parcela(self):
        linha = self.tabela_parcelas.rowCount()
        self.tabela_parcelas.insertRow(linha)

        item = QTableWidgetItem(str(linha + 1))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tabela_parcelas.setItem(linha, 0, item)

        self.tabela_parcelas.setItem(linha, 1, QTableWidgetItem(""))
        self.tabela_parcelas.setItem(linha, 2, QTableWidgetItem(""))
        self.tabela_parcelas.setItem(linha, 3, QTableWidgetItem(""))
        self.tabela_parcelas.setItem(linha, 4, QTableWidgetItem(""))
        self.tabela_parcelas.setItem(linha, 5, QTableWidgetItem(""))



    def verificar_ultima_linha(self, item):
        pass

    def linha_esta_vazia(self, linha):
        for coluna in range(1, 6):  # Dias até OBS.
            item = self.tabela_parcelas.item(linha, coluna)
            if item and item.text().strip() != "":
                return False
        return True


    def finalizar_tabela(self):
        ultima_linha = self.tabela_parcelas.rowCount() - 1

        if ultima_linha >= 0 and self.linha_esta_vazia(ultima_linha):
            self.tabela_parcelas.removeRow(ultima_linha)

        self.edit_obs.setFocus()
        self.edit_obs.selectAll()

    def verificar_fluxo_pagamento(self, texto):
        forma = self.edit_opc_form_pag.text()

        # À vista → vai para OBS
        if forma == "1" and texto in ["1", "2", "3", "4"]:
            self.edit_obs.setFocus()
            self.edit_obs.selectAll()

        # A prazo → vai para tabela (coluna Dias)
        elif forma == "2" and texto in ["1", "2", "3", "4"]:
            self.tabela_parcelas.setFocus()
            self.tabela_parcelas.setCurrentCell(0, 1)
            self.tabela_parcelas.editItem(self.tabela_parcelas.item(0, 1))

    def preencher_data_parcela(self, item):
        coluna = item.column()
        linha = item.row()

        # Só funciona na coluna Dias
        if coluna != 1:
            return

        texto_dias = item.text().strip()

        if not texto_dias.isdigit():
            return

        dias = int(texto_dias)

        from datetime import date, timedelta
        data_vencimento = date.today() + timedelta(days=dias)
        data_formatada = data_vencimento.strftime("%d/%m/%Y")

        self.tabela_parcelas.blockSignals(True)
        self.tabela_parcelas.setItem(linha, 2, QTableWidgetItem(data_formatada))
        self.tabela_parcelas.blockSignals(False)

    def avancar_tabela(self):
        linha = self.tabela_parcelas.currentRow()
        coluna = self.tabela_parcelas.currentColumn()

        # Dias -> Data
        if coluna == 1:
            self.tabela_parcelas.setCurrentCell(linha, 2)
            self.tabela_parcelas.editItem(self.tabela_parcelas.item(linha, 2))

        # Data -> %
        elif coluna == 2:
            self.tabela_parcelas.setCurrentCell(linha, 3)
            self.tabela_parcelas.editItem(self.tabela_parcelas.item(linha, 3))

        # % -> Valor
        elif coluna == 3:
            self.tabela_parcelas.setCurrentCell(linha, 4)
            self.tabela_parcelas.editItem(self.tabela_parcelas.item(linha, 4))

        # Valor -> OBS.
        elif coluna == 4:
            self.tabela_parcelas.setCurrentCell(linha, 5)
            self.tabela_parcelas.editItem(self.tabela_parcelas.item(linha, 5))

        # OBS. -> decide se cria nova ou finaliza
        elif coluna == 5:
            if self.linha_esta_vazia(linha):
                self.finalizar_tabela()
            else:
                if linha == self.tabela_parcelas.rowCount() - 1:
                    self.adicionar_linha_parcela()

                self.tabela_parcelas.setCurrentCell(linha + 1, 1)
                self.tabela_parcelas.editItem(self.tabela_parcelas.item(linha + 1, 1))

    def preencher_dias_pela_data(self, item):
        from datetime import datetime, date

        linha = item.row()
        coluna = item.column()

        # só funciona na coluna Data
        if coluna != 2:
            return

        texto_data = item.text().strip()

        if not texto_data:
            return

        data_formatada = self.formatar_data_digitada(texto_data)
        if not data_formatada:
            return

        try:
            data_digitada = datetime.strptime(data_formatada, "%d/%m/%Y").date()
        except ValueError:
            return

        dias = (data_digitada - date.today()).days

        self.tabela_parcelas.blockSignals(True)

        item_data = self.tabela_parcelas.item(linha, 2)
        if item_data is None:
            item_data = QTableWidgetItem("")
            item_data.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabela_parcelas.setItem(linha, 2, item_data)

        item_data.setText(data_formatada)

        item_dias = self.tabela_parcelas.item(linha, 1)
        if item_dias is None:
            item_dias = QTableWidgetItem("")
            item_dias.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabela_parcelas.setItem(linha, 1, item_dias)

        item_dias.setText(str(dias))

        self.tabela_parcelas.blockSignals(False)

    def formatar_data_digitada(self, texto):
        from datetime import date

        texto = texto.strip().replace("/", "")

        if not texto.isdigit():
            return None

        ano_atual = date.today().year

        # ddmm -> usa ano atual
        if len(texto) == 4:
            dia = texto[:2]
            mes = texto[2:4]
            ano = str(ano_atual)

        # ddmmaa -> assume ano 20xx
        elif len(texto) == 6:
            dia = texto[:2]
            mes = texto[2:4]
            ano = "20" + texto[4:6]

        # ddmmaaaa -> ano completo
        elif len(texto) == 8:
            dia = texto[:2]
            mes = texto[2:4]
            ano = texto[4:8]

        else:
            return None

        data_formatada = f"{dia}/{mes}/{ano}"

        return data_formatada



    def preencher_valor_pelo_percentual(self, item):
        linha = item.row()
        coluna = item.column()

        if coluna != 3:
            return

        texto_percentual = item.text().strip().replace(",", ".")

        if not texto_percentual:
            return

        try:
            percentual = float(texto_percentual)
        except ValueError:
            return

        valor_total_venda = self.valor_total_venda
        valor_parcela = (percentual / 100) * valor_total_venda

        percentual_formatado = f"{percentual:.2f}".replace(".", ",")
        valor_formatado = f"{valor_parcela:.2f}".replace(".", ",")

        self.tabela_parcelas.blockSignals(True)

        # atualiza %
        item_percent = self.tabela_parcelas.item(linha, 3)
        if item_percent:
            item_percent.setText(percentual_formatado)

        # atualiza valor
        item_valor = self.tabela_parcelas.item(linha, 4)
        if item_valor is None:
            item_valor = QTableWidgetItem("")
            item_valor.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.tabela_parcelas.setItem(linha, 4, item_valor)

        item_valor.setText(valor_formatado)

        self.tabela_parcelas.blockSignals(False)



    def preencher_percentual_pelo_valor(self, item):
        linha = item.row()
        coluna = item.column()

        # só funciona na coluna Valor
        if coluna != 4:
            return

        texto_valor = item.text().strip().replace(",", ".")

        if not texto_valor:
            return

        try:
            valor = float(texto_valor)
        except ValueError:
            return

        valor_total_venda = self.valor_total_venda

        if valor_total_venda == 0:
            return

        percentual = (valor / valor_total_venda) * 100

        percentual_formatado = f"{percentual:.2f}".replace(".", ",")
        valor_formatado = f"{valor:.2f}".replace(".", ",")

        self.tabela_parcelas.blockSignals(True)

        # atualiza valor formatado
        item_valor = self.tabela_parcelas.item(linha, 4)
        if item_valor:
            item_valor.setText(valor_formatado)

        # atualiza %
        item_percent = self.tabela_parcelas.item(linha, 3)
        if item_percent is None:
            item_percent = QTableWidgetItem("")
            item_percent.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabela_parcelas.setItem(linha, 3, item_percent)

        item_percent.setText(percentual_formatado)

        self.tabela_parcelas.blockSignals(False)


    def fechar(self):
        self.close()



    def salvar(self):
        if not self.tela_saida:
            print("TelaSaida não recebida")
            return

        from bd import conectar
        from datetime import datetime
        from PyQt6.QtWidgets import QMessageBox

        forma = self.edit_opc_form_pag.text().strip()
        condicao = self.edit_opc_cond_pag.text().strip()

        if not forma:
            msg = QMessageBox(self)
            msg.setWindowTitle("Aviso")
            msg.setText("Informe a forma de pagamento.")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QLabel {
                    color: black;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #031740;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 4px;
                    min-width: 80px;
                }
            """)
            msg.exec()
            self.edit_opc_form_pag.setFocus()
            return

        if not condicao:
            msg = QMessageBox(self)
            msg.setWindowTitle("Aviso")
            msg.setText("Informe a condição de pagamento.")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QLabel {
                    color: black;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #031740;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 4px;
                    min-width: 80px;
                }
            """)
            msg.exec()
            self.edit_opc_cond_pag.setFocus()
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            tipo = "ORCAMENTO"

            cod_cliente = self.tela_saida.cod_cliente.text().strip() or None
            nome_cliente = self.tela_saida.edit_cliente.text().strip()
            cpf_cliente = self.tela_saida.edit_cpf_cliente.text().strip()

            cod_vendedor = self.tela_saida.cod_vendedor.text().strip() or None
            nome_vendedor = self.tela_saida.edit_vendedor.text().strip()

            desconto = self.texto_para_float(self.tela_saida.edit_desconto.text())

            total_produtos = self.texto_para_float(
                self.tela_saida.label_total_produtos.text().replace("R$", "").strip()
            )

            total_venda = self.texto_para_float(
                self.tela_saida.label_total_venda.text().replace("R$", "").strip()
            )

            cursor.execute("""
                INSERT INTO orcamento (
                    data_hora, tipo,
                    cod_cliente, nome_cliente, cpf_cliente,
                    cod_vendedor, nome_vendedor,
                    desconto, total_produtos, total_venda
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                datetime.now(),
                tipo,
                cod_cliente,
                nome_cliente,
                cpf_cliente,
                cod_vendedor,
                nome_vendedor,
                desconto,
                total_produtos,
                total_venda
            ))

            id_orcamento = cursor.lastrowid

            self.salvar_itens_orcamento(cursor, id_orcamento)
            self.salvar_pagamento(cursor, id_orcamento)

            conn.commit()

            msg = QMessageBox(self)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"Orçamento {id_orcamento} salvo com sucesso!")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QLabel {
                    color: black;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #031740;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
            """)
            msg.exec()

            cursor.close()
            conn.close()

            self.close()
            self.tela_saida.novo()

        except Exception as e:
            msg = QMessageBox(self)
            msg.setWindowTitle("Erro")
            msg.setText(f"Erro ao salvar:\n{e}")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QLabel {
                    color: black;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #031740;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 4px;
                    min-width: 80px;
                }
            """)
            msg.exec()



    def texto_para_float(self, texto):
        texto = str(texto).strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            return 0.0   


    def salvar_itens_orcamento(self, cursor, id_orcamento):
        for linha in range(self.tela_saida.tabela.rowCount()):
            item = linha + 1

            cod_produto = self.tela_saida.tabela.item(linha, 1).text()
            descricao = self.tela_saida.tabela.item(linha, 2).text()
            unidade = self.tela_saida.tabela.item(linha, 3).text()

            quantidade = self.texto_para_float(
                self.tela_saida.tabela.item(linha, 4).text()
            )
            preco = self.texto_para_float(
                self.tela_saida.tabela.item(linha, 5).text()
            )
            preco_desc = self.texto_para_float(
                self.tela_saida.tabela.item(linha, 6).text()
            )
            total = self.texto_para_float(
                self.tela_saida.tabela.item(linha, 7).text()
            )

            cursor.execute("""
                INSERT INTO orcamento_itens (
                    id_orcamento, item, cod_produto, descricao, unidade,
                    quantidade, preco_unitario, preco_com_desconto, total
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id_orcamento,
                item,
                cod_produto,
                descricao,
                unidade,
                quantidade,
                preco,
                preco_desc,
                total
            ))



    def salvar_pagamento(self, cursor, id_orcamento):
        forma = self.edit_opc_form_pag.text().strip()
        condicao = self.edit_opc_cond_pag.text().strip()
        obs_geral = self.edit_obs.text().strip()

        # -------- À VISTA --------
        if forma == "1":
            valor_total = self.valor_total_venda

            cursor.execute("""
                INSERT INTO orcamento_pagamento (
                    id_orcamento, forma_pagamento, condicao_pagamento,
                    parcela, dias, data_vencimento,
                    percentual, valor, obs, obs_geral
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id_orcamento,
                forma,
                condicao,
                1,
                0,
                None,
                100,
                valor_total,
                "",
                obs_geral
            ))

        # -------- A PRAZO --------
        elif forma == "2":
            from datetime import datetime

            for linha in range(self.tabela_parcelas.rowCount()):
                item_dias = self.tabela_parcelas.item(linha, 1)
                item_data = self.tabela_parcelas.item(linha, 2)
                item_percent = self.tabela_parcelas.item(linha, 3)
                item_valor = self.tabela_parcelas.item(linha, 4)
                item_obs = self.tabela_parcelas.item(linha, 5)

                # ignora linha vazia
                if not item_dias or not item_dias.text().strip():
                    continue

                dias = int(item_dias.text())
                data_str = item_data.text().strip() if item_data else None

                data_vencimento = None
                if data_str:
                    try:
                        data_vencimento = datetime.strptime(data_str, "%d/%m/%Y").date()
                    except:
                        pass

                percentual = self.texto_para_float(item_percent.text()) if item_percent else 0
                valor = self.texto_para_float(item_valor.text()) if item_valor else 0
                obs = item_obs.text().strip() if item_obs else ""

                cursor.execute("""
                    INSERT INTO orcamento_pagamento (
                        id_orcamento, forma_pagamento, condicao_pagamento,
                        parcela, dias, data_vencimento,
                        percentual, valor, obs, obs_geral
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    id_orcamento,
                    forma,
                    condicao,
                    linha + 1,
                    dias,
                    data_vencimento,
                    percentual,
                    valor,
                    obs,
                    obs_geral
                ))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = TelaPagamento()
    janela.exec()
