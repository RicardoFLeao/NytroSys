
def tela_ent(self):
    from entidades.tela_ent import TelaEntidades
    self.janela = TelaEntidades()
    self.janela.show()
    self.close()


def tela_cad_fun(self):
    from entidades.cad_fun import CadFuncionarios
    self.janela = CadFuncionarios()
    self.janela.show()
    self.close()


def tela_cad_cli(self):
    from entidades.cad_cli import CadCliente
    self.janela = CadCliente()
    self.janela.show()
    self.close()


def tela_cad_for(self):
    from entidades.cad_for import CadFornecedor
    self.janela = CadFornecedor()
    self.janela.show()
    self.close()


def tela_cad_prod(self):
    from adm_prod.cad_prod import CadProd
    self.janela = CadProd()
    self.janela.show()
    self.close()


def tela_acerto_estoque(self):
    from estoque.tela_acerto_estoque import TelaAcertoEstoque
    self.janela = TelaAcertoEstoque()
    self.janela.showMaximized()
    self.close()


def tela_movimentacao(self):
    from movimentacao.tela_movimentacao import TelaMovimentacao
    self.janela = TelaMovimentacao()
    self.janela.show()
    self.close()
