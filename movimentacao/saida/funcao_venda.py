import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QTableWidgetItem, QMessageBox


def abrir_pesquisa_produto(self, texto_inicial=""):
    from consulta.tela_pesq_prod_mov import TelaConsProd

    self.tela_pesquisa = TelaConsProd(self)
    self.tela_pesquisa.show()

    if texto_inicial:
        self.tela_pesquisa.edit_buscar.setText(texto_inicial)
        self.tela_pesquisa.buscar_produtos()


def abrir_pesquisa_ao_digitar(self, texto):
    texto = texto.strip()

    if not texto:
        return

    self.edit_busca_produto.blockSignals(True)
    self.edit_busca_produto.clear()
    self.edit_busca_produto.blockSignals(False)

    self.abrir_pesquisa_produto(texto)


def receber_produto_pesquisa(self, produto):
    codigo = str(produto.get("codigo") or "").strip()

    for linha in range(self.tabela.rowCount()):
        item_codigo = self.tabela.item(linha, 1)

        if item_codigo and item_codigo.text().strip() == codigo:
            msg = QMessageBox(self)
            msg.setWindowTitle("Produto repetido")
            msg.setText("Item já sel. Alterar a quantidade?")
            msg.setIcon(QMessageBox.Icon.Question)

            botao_sim = msg.addButton("Sim", QMessageBox.ButtonRole.YesRole)
            botao_nao = msg.addButton("Não", QMessageBox.ButtonRole.NoRole)

            msg.setDefaultButton(botao_sim)
            msg.exec()

            resposta = botao_sim if msg.clickedButton() == botao_sim else botao_nao

            if resposta == botao_sim:
                self.tabela.setFocus()
                self.tabela.setCurrentCell(linha, 4)
                self.produto_atual = None
                return True
            else:
                self.produto_atual = None
                return False

    self.produto_atual = produto

    self.edit_busca_produto.setText(str(produto.get("descricao") or ""))
    self.edit_unitario_item.setText(str(produto.get("preco_venda") or "0,00"))

    self.valor_rua.setText(str(produto.get("rua") or ""))
    self.valor_bloco.setText(str(produto.get("bloco") or ""))
    self.valor_prateleira.setText(str(produto.get("prateleira") or ""))
    self.valor_gaveta.setText(str(produto.get("gaveta") or ""))
    self.valor_aplicacao.setText(str(produto.get("aplicacao") or ""))

    caminho_foto = str(produto.get("foto_1") or "").strip()

    if caminho_foto and os.path.exists(caminho_foto):
        pixmap = QPixmap(caminho_foto)
        pixmap = pixmap.scaled(
            self.label_foto.width(),
            self.label_foto.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label_foto.setPixmap(pixmap)
        self.label_foto.setText("")
    else:
        self.label_foto.clear()
        self.label_foto.setText("Sem foto")

    self.edit_quantidade_item.setFocus()
    self.edit_quantidade_item.selectAll()


def ir_para_unitario(self):
    self.edit_unitario_item.setFocus()
    self.edit_unitario_item.selectAll()


def criar_item(self, texto=""):
    return QTableWidgetItem(str(texto))


def limpar_info_produto(self):
    self.valor_rua.clear()
    self.valor_bloco.clear()
    self.valor_prateleira.clear()
    self.valor_gaveta.clear()
    self.valor_aplicacao.clear()
    self.label_foto.clear()
    self.label_foto.setText("Sem foto")


def adicionar_produto_tabela(self):
    if not self.produto_atual:
        return

    codigo = str(self.produto_atual.get("codigo") or "")

    linha = self.tabela.rowCount()
    self.tabela.insertRow(linha)

    descricao = str(self.produto_atual.get("descricao") or "")
    unidade = str(self.produto_atual.get("un_venda") or "")
    quantidade = self.edit_quantidade_item.text().strip() or "0,00"
    preco = self.edit_unitario_item.text().strip() or "0,00"

    quantidade_float = self.texto_para_float(quantidade)
    preco_float = self.texto_para_float(preco)
    total_float = quantidade_float * preco_float

    item_num = self.criar_item(linha + 1)
    item_num.setData(Qt.ItemDataRole.UserRole, self.produto_atual)
    self.tabela.setItem(linha, 0, item_num)

    self.tabela.setItem(linha, 1, self.criar_item(codigo))
    self.tabela.setItem(linha, 2, self.criar_item(descricao))
    self.tabela.setItem(linha, 3, self.criar_item(unidade))
    self.tabela.setItem(linha, 4, self.criar_item(
        self.formatar_valor(quantidade_float)))
    self.tabela.setItem(linha, 5, self.criar_item(
        self.formatar_valor(preco_float)))
    self.tabela.setItem(linha, 6, self.criar_item(
        self.formatar_valor(preco_float)))
    self.tabela.setItem(linha, 7, self.criar_item(
        self.formatar_valor(total_float)))

    self.destacar_linha_atual(linha, 4, -1, -1)

    self.edit_busca_produto.clear()
    self.edit_quantidade_item.setText("0,00")
    self.edit_unitario_item.setText("0,00")
    self.produto_atual = None

    self.limpar_info_produto()
    self.edit_busca_produto.setFocus()
    self.atualizar_totais()


def ir_para_tabela_quantidade(self):
    for linha in range(self.tabela.rowCount()):
        item_descricao = self.tabela.item(linha, 2)
        item_quantidade = self.tabela.item(linha, 4)

        if item_descricao and item_descricao.text().strip() and item_quantidade:
            self.tabela.setFocus()
            self.tabela.setCurrentCell(linha, 4)
            return


def event_filter_tabela(self, obj, event):
    if obj == self.tabela and event.type() == event.Type.KeyPress:
        linha = self.tabela.currentRow()
        coluna = self.tabela.currentColumn()

        if linha < 0:
            return super(type(self), self).eventFilter(obj, event)

        if coluna not in (4, 5):
            self.tabela.setCurrentCell(linha, 4)
            coluna = 4

        if event.key() == Qt.Key.Key_Left:
            self.tabela.setCurrentCell(linha, 4)
            return True

        if event.key() == Qt.Key.Key_Right:
            self.tabela.setCurrentCell(linha, 5)
            return True

        texto = event.text()

        if texto and (texto.isdigit() or texto in ",."):
            item = self.tabela.item(linha, coluna)
            if item:
                self.tabela.editItem(item)

                editor = self.tabela.findChild(QLineEdit)
                if editor:
                    editor.setStyleSheet("""
                        QLineEdit {
                            background-color: white;
                            color: black;
                            border: 1px solid #031740;
                            selection-background-color: #dbe7f0;
                            selection-color: black;
                        }
                    """)
                    editor.setText(texto)
                    editor.setCursorPosition(len(texto))

            return True

    return super(type(self), self).eventFilter(obj, event)


def tratar_edicao_tabela(self, item):
    if not item:
        return

    linha = item.row()
    coluna = item.column()

    if coluna not in (4, 5):
        return

    item_qtd = self.tabela.item(linha, 4)
    item_preco = self.tabela.item(linha, 5)

    if not item_qtd or not item_preco:
        return

    quantidade = self.texto_para_float(item_qtd.text())
    preco = self.texto_para_float(item_preco.text())

    if quantidade == 0:
        self.tabela.blockSignals(True)
        self.tabela.removeRow(linha)
        self.tabela.blockSignals(False)

        self.renumerar_itens_tabela()

        if self.tabela.rowCount() == 0:
            self.edit_busca_produto.setFocus()

        self.atualizar_totais()
        return

    total = quantidade * preco

    self.tabela.blockSignals(True)

    item_qtd.setText(self.formatar_valor(quantidade))
    item_preco.setText(self.formatar_valor(preco))

    item_preco_desc = self.tabela.item(linha, 6)
    if item_preco_desc:
        item_preco_desc.setText(self.formatar_valor(preco))

    item_total = self.tabela.item(linha, 7)
    if item_total:
        item_total.setText(self.formatar_valor(total))

    self.tabela.blockSignals(False)
    self.atualizar_totais()


def destacar_linha_atual(self, linha_atual, coluna_atual, linha_anterior, coluna_anterior):
    for linha in range(self.tabela.rowCount()):
        item_base = self.tabela.item(linha, 0)

        estoque = 0
        if item_base:
            produto = item_base.data(Qt.ItemDataRole.UserRole)
            if produto:
                try:
                    estoque = float(produto.get("quantidade") or 0)
                except (ValueError, TypeError):
                    estoque = 0

        for coluna in range(self.tabela.columnCount()):
            item = self.tabela.item(linha, coluna)
            if not item:
                continue

            fonte = item.font()
            fonte.setBold(False)
            item.setFont(fonte)

            if estoque <= 0:
                item.setForeground(Qt.GlobalColor.red)
            else:
                item.setForeground(Qt.GlobalColor.black)

    if linha_atual < 0:
        return

    item_base = self.tabela.item(linha_atual, 0)

    estoque = 0
    if item_base:
        produto = item_base.data(Qt.ItemDataRole.UserRole)
        if produto:
            try:
                estoque = float(produto.get("quantidade") or 0)
            except (ValueError, TypeError):
                estoque = 0

    for coluna in range(self.tabela.columnCount()):
        item = self.tabela.item(linha_atual, coluna)
        if not item:
            continue

        fonte = item.font()
        fonte.setBold(True)
        item.setFont(fonte)

        if estoque <= 0:
            item.setForeground(Qt.GlobalColor.red)
        else:
            item.setForeground(Qt.GlobalColor.black)


def texto_para_float(self, texto):
    texto = str(texto).strip().replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return 0.0


def formatar_valor(self, valor):
    return f"{valor:.2f}".replace(".", ",")


def atualizar_info_produto_tabela(self, linha_atual, coluna_atual, linha_anterior, coluna_anterior):
    if linha_atual < 0:
        return

    item_base = self.tabela.item(linha_atual, 0)
    if not item_base:
        return

    produto = item_base.data(Qt.ItemDataRole.UserRole)
    if not produto:
        return

    self.valor_rua.setText(str(produto.get("rua") or ""))
    self.valor_bloco.setText(str(produto.get("bloco") or ""))
    self.valor_prateleira.setText(str(produto.get("prateleira") or ""))
    self.valor_gaveta.setText(str(produto.get("gaveta") or ""))
    self.valor_aplicacao.setText(str(produto.get("aplicacao") or ""))

    caminho_foto = str(produto.get("foto_1") or "").strip()

    if caminho_foto and os.path.exists(caminho_foto):
        pixmap = QPixmap(caminho_foto)
        pixmap = pixmap.scaled(
            self.label_foto.width(),
            self.label_foto.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label_foto.setPixmap(pixmap)
        self.label_foto.setText("")
    else:
        self.label_foto.clear()
        self.label_foto.setText("Sem foto")


def atualizar_totais(self):
    total_produtos = 0
    total_venda = 0
    desconto = self.texto_para_float(self.edit_desconto.text())

    for linha in range(self.tabela.rowCount()):
        item_preco = self.tabela.item(linha, 5)
        item_quant = self.tabela.item(linha, 4)
        item_preco_desc = self.tabela.item(linha, 6)
        item_total = self.tabela.item(linha, 7)

        if not item_preco or not item_quant:
            continue

        preco = self.texto_para_float(item_preco.text())
        quantidade = self.texto_para_float(item_quant.text())

        preco_com_desconto = preco - (preco * (desconto / 100))
        total_linha_sem_desconto = quantidade * preco
        total_linha_com_desconto = quantidade * preco_com_desconto

        if item_preco_desc:
            item_preco_desc.setText(self.formatar_valor(preco_com_desconto))

        if item_total:
            item_total.setText(self.formatar_valor(total_linha_com_desconto))

        total_produtos += total_linha_sem_desconto
        total_venda += total_linha_com_desconto

    self.label_total_produtos.setText(
        f"R$ {self.formatar_valor(total_produtos)}")
    self.label_total_venda.setText(
        f"R$ {self.formatar_valor(total_venda)}")


def renumerar_itens_tabela(self):
    for linha in range(self.tabela.rowCount()):
        item = self.tabela.item(linha, 0)
        if item:
            item.setText(str(linha + 1))


def novo(self):
    self.cod_cliente.clear()
    self.edit_cliente.clear()
    self.edit_cpf_cliente.clear()

    self.cod_vendedor.clear()
    self.edit_vendedor.clear()

    self.edit_desconto.clear()

    self.edit_busca_produto.clear()
    self.edit_quantidade_item.setText("0,00")
    self.edit_unitario_item.setText("0,00")

    self.tabela.setRowCount(0)

    self.limpar_info_produto()

    self.label_total_produtos.setText("R$ 0,00")
    self.label_total_venda.setText("R$ 0,00")

    self.produto_atual = None

    self.edit_busca_produto.setFocus()

    self.carregar_proximo_numero_orcamento()

def controlar_tipo_venda(self, checkbox):
    if checkbox == self.check_orc and self.check_orc.isChecked():
        self.check_cfe.setChecked(False)
        self.check_nfe.setChecked(False)

    elif checkbox == self.check_cfe and self.check_cfe.isChecked():
        self.check_orc.setChecked(False)
        self.check_nfe.setChecked(False)

    elif checkbox == self.check_nfe and self.check_nfe.isChecked():
        self.check_orc.setChecked(False)
        self.check_cfe.setChecked(False)

    # garante pelo menos um marcado
    if (
        not self.check_orc.isChecked()
        and not self.check_cfe.isChecked()
        and not self.check_nfe.isChecked()
    ):
        self.check_orc.setChecked(True)


def salvar_orcamento(self):
    from bd import conectar
    from PyQt6.QtWidgets import QMessageBox
    from datetime import datetime

    try:
        conn = conectar()
        cursor = conn.cursor()

        if self.check_orc.isChecked():
            tipo = "ORCAMENTO"
        elif self.check_cfe.isChecked():
            tipo = "CFE"
        else:
            tipo = "NFE"

        cod_cliente = self.cod_cliente.text().strip() or None
        nome_cliente = self.edit_cliente.text().strip()
        cpf_cliente = self.edit_cpf_cliente.text().strip()

        cod_vendedor = self.cod_vendedor.text().strip() or None
        nome_vendedor = self.edit_vendedor.text().strip()

        desconto = self.texto_para_float(self.edit_desconto.text())

        total_produtos = self.texto_para_float(
            self.label_total_produtos.text().replace("R$", "").strip()
        )

        total_venda = self.texto_para_float(
            self.label_total_venda.text().replace("R$", "").strip()
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
        self.edit_num.setText(str(id_orcamento).zfill(4))

        self.salvar_itens_orcamento(cursor, id_orcamento)

        conn.commit()

        QMessageBox.information(self, "Sucesso", "Orçamento salvo!")

        self.novo()

        cursor.close()
        conn.close()

    except Exception as e:
        QMessageBox.critical(self, "Erro", f"Erro ao salvar:\n{e}")




def salvar_itens_orcamento(self, cursor, id_orcamento):
    for linha in range(self.tabela.rowCount()):
        item = linha + 1

        cod_produto = self.tabela.item(linha, 1).text()
        descricao = self.tabela.item(linha, 2).text()
        unidade = self.tabela.item(linha, 3).text()

        quantidade = self.texto_para_float(
            self.tabela.item(linha, 4).text()
        )
        preco = self.texto_para_float(
            self.tabela.item(linha, 5).text()
        )
        preco_desc = self.texto_para_float(
            self.tabela.item(linha, 6).text()
        )
        total = self.texto_para_float(
            self.tabela.item(linha, 7).text()
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

def carregar_proximo_numero_orcamento(self):
    from bd import conectar

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(id) AS ultimo_id FROM orcamento")
        resultado = cursor.fetchone()

        ultimo_id = resultado["ultimo_id"] if resultado and resultado["ultimo_id"] else 0
        proximo = ultimo_id + 1

        self.edit_num.setText(str(proximo).zfill(4))

        cursor.close()
        conn.close()

    except Exception as e:
        print("ERRO AO CARREGAR NUMERO:", e)
        self.edit_num.setText("0001")