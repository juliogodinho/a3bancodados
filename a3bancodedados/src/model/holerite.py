from datetime import date
from model.funcionario import Funcionario
from model.empresa import Empresa

class Holerite:
    def __init__(self, 
                 codigo:int=None,
                 salariobruto:str=None,
                 fgts:str=None,
                 irpf:str=None,
                 salarioliquido:str=None,    
                 funcionario:Funcionario= None,
                 empresa:Empresa=None
                 ):
        self.set_codigo(codigo)
        self.set_funcionario(funcionario)
        self.set_empresa(empresa)


    def set_codigo(self, codigo:int):
        self.codigo = codigo

    def set_funcionario(self, funcionario:Funcionario):
        self.funcionario = funcionario

    def set_empresa(self, empresa:Empresa):
        self.empresa = empresa

    def get_codigo(self) -> int:
        return self.codigo

    def get_funcionario(self) -> Funcionario:
        return self.funcionario

    def get_empresa(self) -> Empresa:
        return self.empresa

    def to_string(self) -> str:
        return f"Holerite: {self.get_codigo()} | Funcionario: {self.get_funcionario().get_nome()} | Empresa: {self.get_empresa().get_nome_fantasia()}"